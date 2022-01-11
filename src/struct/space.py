from __future__ import annotations

import json
from random import randint

from mpi4py import MPI
import mpi4py.MPI

from src.struct.point_3d import Point3d
from src.struct.star import Star

comm: mpi4py.MPI.Intracomm = MPI.COMM_WORLD
process_id: int = comm.Get_rank()


class Space:
    @staticmethod
    def generate_space(size: int) -> list[Star]:
        return [
            Star(
                Point3d(randint(-100, 100), randint(-100, 100), randint(-100, 100)),
                randint(10, 10000) / 100,
                f'{process_id}_{index}'
            )
            for index in range(size)
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
        for index, json_star in enumerate(json_content):
            content.append(
                Star(
                    Point3d(json_star["position"]["x"], json_star["position"]["y"], json_star["position"]["z"]),
                    json_star["mass"],
                    f'{process_id}_{index}'
                )
            )
        return content
