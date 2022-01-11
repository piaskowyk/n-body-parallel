from __future__ import annotations
from src.struct.point_3d import Point3d
from src.struct.vector_3d import Vec3d

G = 6.6743015e-3


class Star:
    position: Point3d
    mass: float
    force: Vec3d = Vec3d()
    velocity: Vec3d = Vec3d()
    distance_vector_sum_buffer: Vec3d = Vec3d()
    star_id: str = None

    def __init__(self, position: Point3d, mass: float, star_id: str):
        self.position = position
        self.mass = mass
        self.star_id = star_id

    def get_distance_vector_sum(self, space: list[Star]) -> Vec3d:
        vector_sum = Vec3d()
        for star in space:
            if star.star_id == self.star_id:
                continue
            distance = self.position.distance_to_point(star.position)
            distance_vector = Vec3d.from_points(star.position, self.position)
            distance_factor = distance ** 3
            if distance_factor == 0:  # i ignore collision etc
                continue
            distance_vector.multiple_by_scalar(star.mass / distance_factor)
            vector_sum.add(distance_vector)
        return vector_sum

    def calc_force(self, space: list[Star]):
        distance = self.get_distance_vector_sum(space)
        distance.multiple_by_scalar(G * self.mass)
        self.force = distance

    def update_distance_vector_sum_buffer(self, space: list[Star]):
        self.distance_vector_sum_buffer.add(self.get_distance_vector_sum(space))

    def calc_force_from_buffer(self):
        vector = self.distance_vector_sum_buffer.copy()
        vector.multiple_by_scalar(G * self.mass)
        self.force = vector

    def reset(self):
        self.distance_vector_sum_buffer = Vec3d()

    def calc_new_position(self, d_time: float):
        d_velocity = self.force.copy()
        d_velocity.neg()
        d_velocity.multiple_by_scalar((1 / self.mass))
        self.velocity.add(d_velocity)
        d_position = self.velocity.copy()
        d_position.multiple_by_scalar(d_time)
        self.position.add(d_position)
