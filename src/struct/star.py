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

    def reset(self):
        self.distance_vector_sum_buffer = Vec3d()

    def calc_new_position(self, d_time: float):
        d_velocity = self.force.copy()
        d_velocity.multiple_by_scalar((1 / self.mass) * d_time)
        self.velocity.add(d_velocity)
        d_position = self.velocity.copy()
        d_position.multiple_by_scalar(d_time)
        self.position.add(d_position)
