from __future__ import annotations
import math


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

    def add(self, point: Point3d):
        self.x += point.x
        self.y += point.y
        self.z += point.z
