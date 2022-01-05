from __future__ import annotations
from random import randint
import math
from mpi4py import MPI
import mpi4py.MPI

G = 6.6743015E-11


class Point3d:
    x: float
    y: float
    z: float

    def __init__(self, x=.0, y=.0, z=.0):
        self.x = x
        self.y = y
        self.z = z

    def print(self):
        print(f'(x: {self.x}, y: {self.y}, z: {self.z})')

    def distance_to_point(self, point: Point3d) -> float:
        return math.sqrt(
            (self.x - point.x) ** 2
            + (self.y - point.y) ** 2
            + (self.z - point.z) ** 2
        )

    def copy(self) -> Point3d:
        return Point3d(self.x, self.y, self.z)


class Vec3d(Point3d):
    def multiple_by_scalar(self, scalar: float):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar

    def add(self, vector: Vec3d):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z

    @staticmethod
    def from_points(point_a: Point3d, point_b: Point3d):
        return Vec3d(
            point_b.x - point_a.x,
            point_b.y - point_a.y,
            point_b.z - point_a.z
        )

    def copy(self) -> Vec3d:
        return Vec3d(self.x, self.y, self.z)


class Star:
    position: Point3d
    mass: float
    force: Vec3d = Vec3d()
    distance_vector_sum_buffer: Vec3d = Vec3d()

    def __init__(self, position: Point3d, mass: float):
        self.position = position
        self.mass = mass

    def get_distance_vector_sum(self, space: list[Star]) -> Vec3d:
        vector_sum = Vec3d()
        for star in space:
            if star == self:
                continue
            distance = self.position.distance_to_point(star.position)
            distance_vector = Vec3d.from_points(star.position, self.position)
            distance_vector.multiple_by_scalar(star.mass / distance ** 3)
            vector_sum.add(distance_vector)
        return vector_sum

    def calc_force(self, space: list[Star]):
        distance = self.get_distance_vector_sum(space)
        distance.multiple_by_scalar(G * self.mass)
        self.force = distance

    def update_distance_vector_sum_buffer(self, space: list[Star]):
        self.distance_vector_sum_buffer.add(self.get_distance_vector_sum(space))

    def calc_force_from_buffer(self):
        distance = self.distance_vector_sum_buffer.copy()
        distance.multiple_by_scalar(G * self.mass)
        self.force = distance


class Space:
    @staticmethod
    def generate_space(size: int) -> list[Star]:
        return [
            Star(
                Point3d(randint(0, 100), randint(0, 100), randint(0, 100)),
                randint(0, 10000) / 100
            )
            for _ in range(size)
        ]


class Sequence:
    space: list[Star] = []

    def run(self, generate_space=True, do_print=True):
        if generate_space:
            self.space = Space.generate_space(5)
        for star in self.space:
            star.calc_force(self.space)
            if do_print:
                star.force.print()


class ParallelRing:
    comm: mpi4py.MPI.Intracomm = MPI.COMM_WORLD
    process_id: int = comm.Get_rank()
    process_count: int = comm.Get_size()

    local_space: list[Star] = []
    received_space: list[Star] = []
    distance_vectors_sum_buffer: Vec3d = Vec3d()

    def __init__(self, current_space_size=5, space: list[Star] = None):
        if space:
            self.local_space = space[self.process_id * current_space_size:self.process_id * (current_space_size + 1)]
        else:
            self.local_space = Space.generate_space(current_space_size)

    def run(self):
        for star in self.local_space:
            star.update_distance_vector_sum_buffer(self.local_space)

        for i in range(1, self.process_count):
            destination = (self.process_id + i) % self.process_count
            source = self.process_id - i \
                if self.process_id - i > -1 \
                else self.process_count + self.process_id - i
            self.comm.send(self.local_space, dest=destination)
            self.received_space = self.comm.recv(source=source)
            for star in self.local_space:
                star.update_distance_vector_sum_buffer(self.received_space)

        for star in self.local_space:
            star.calc_force_from_buffer()
            star.force.print()


global_space = Space.generate_space(16)

parallel_ring = ParallelRing(4, global_space)
parallel_ring.run()

sequence = Sequence()
sequence.space = global_space
sequence.run(False, False)


def is_same_star(star_a: Star, star_b: Star) -> bool:
    return star_a.position.x == star_b.position.x \
        and star_a.position.y == star_b.position.y \
        and star_a.position.z == star_b.position.z \
        and star_a.mass == star_b.mass


for star in parallel_ring.local_space:
    for global_star in global_space:
        if is_same_star(star, global_star):
            if star.force != global_star.force:
                print("ERROR")
