from __future__ import annotations
from src.struct.point_3d import Point3d


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
