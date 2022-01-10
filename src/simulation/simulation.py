from __future__ import annotations

import json
import math

from mpi4py import MPI
import mpi4py.MPI

from src.struct.space import Space
from src.struct.star import Star
from src.struct.vector_3d import Vec3d


class Simulation:
    comm: mpi4py.MPI.Intracomm = MPI.COMM_WORLD
    process_id: int = comm.Get_rank()
    process_count: int = comm.Get_size()

    local_space: list[Star] = []
    received_space: list[Star] = []
    distance_vectors_sum_buffer: Vec3d = Vec3d()
    iteration_count: int = 5
    current_iteration: int = 0
    d_time: float = 0.5

    simulation_buffer = []

    def __init__(self, current_space_size=5, space: list[Star] = None, iteration_count: int = 1000):
        if space:
            start = (self.process_id + 1) * current_space_size - current_space_size
            stop = (self.process_id + 2) * current_space_size - current_space_size
            self.local_space = space[start:stop]
        else:
            self.local_space = Space.generate_space(current_space_size)
        self.iteration_count = iteration_count

    def run(self):
        for i in range(self.iteration_count):
            self.dump_data()
            self.iteration()
            self.update_position()
            self.clear_local_space()
            self.current_iteration = i
        self.dump_data(True)

    def clear_local_space(self):
        for star in self.local_space:
            star.reset()

    def update_position(self):
        for star in self.local_space:
            star.calc_new_position(self.d_time)

    def dump_data(self, flush: bool = False):
        for index, star in enumerate(self.local_space):
            self.simulation_buffer.append({
                "id": (self.process_id, index),
                "iteration": self.current_iteration,
                "star": {
                    "x": star.position.x,
                    "y": star.position.y,
                    "z": star.position.z,
                }
            })
        if flush:
            with open(f'simulation_data/proc_{self.process_id}_dump.json', 'w') as file:
                file.write(json.dumps(self.simulation_buffer))

    def iteration(self):
        self.received_space = self.local_space
        interaction_count = math.ceil(self.process_count / 2)
        for i in range(1, interaction_count):
            destination = (self.process_id + i) % self.process_count
            source = self.process_id - i \
                if self.process_id - i > -1 \
                else self.process_count + self.process_id - i
            self.comm.send(self.received_space, dest=destination)
            self.received_space = self.comm.recv(source=source)
            for star in self.received_space:
                star.update_distance_vector_sum_buffer(self.local_space)
            for star in self.local_space:
                star.update_distance_vector_sum_buffer(self.received_space)

        destination = (self.process_id - interaction_count) \
            if (self.process_id - interaction_count) > -1 \
            else self.process_id - interaction_count + self.process_count
        source = (self.process_id - interaction_count) % self.process_count
        self.comm.send(self.received_space, dest=destination)
        self.received_space = self.comm.recv(source=source)
        for i in range(len(self.local_space)):
            self.local_space[i].distance_vector_sum_buffer.add(self.received_space[i].distance_vector_sum_buffer)

        for star in self.local_space:
            star.update_distance_vector_sum_buffer(self.local_space)
            star.calc_force_from_buffer()
            star.force.print()
