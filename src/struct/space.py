from __future__ import annotations
from random import randint

from src.struct.point_3d import Point3d
from src.struct.star import Star


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
