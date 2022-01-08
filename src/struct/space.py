from __future__ import annotations

import json
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

    @staticmethod
    def to_json(space: list[Star]):
        content = []
        for star in space:
            content.append({
                "position": {
                    "x": star.position.x,
                    "y": star.position.y,
                    "z": star.position.z,
                },
                "mass": star.mass
            })
        with open('space.json', 'w') as file:
            file.write(json.dumps(content))

    @staticmethod
    def load_json() -> list[Star]:
        content = []
        with open('space.json', 'r') as file:
            json_content = json.loads(file.read())
        for json_star in json_content:
            content.append(
                Star(
                    Point3d(json_star["position"]["x"], json_star["position"]["y"], json_star["position"]["z"]),
                    json_star["mass"]
                )
            )
        return content
