from __future__ import annotations

import math

from mpi4py import MPI
import mpi4py.MPI

from src.struct.space import Space
from src.struct.star import Star
from src.struct.vector_3d import Vec3d


class FastParallelRing:
    comm: mpi4py.MPI.Intracomm = MPI.COMM_WORLD
    process_id: int = comm.Get_rank()
    process_count: int = comm.Get_size()

    local_space: list[Star] = []
    received_space: list[Star] = []
    distance_vectors_sum_buffer: Vec3d = Vec3d()

    def __init__(self, current_space_size=5, space: list[Star] = None):
        if space:
            current_space_size = int(len(space) / self.process_count)
            self.local_space = space[self.process_id * current_space_size:self.process_id * (current_space_size + 1)]
        else:
            self.local_space = Space.generate_space(current_space_size)

    def run(self):
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
        source = (self.process_id + interaction_count) % self.process_count
        self.comm.send(self.received_space, dest=destination)
        self.received_space = self.comm.recv(source=source)
        for i in range(len(self.local_space)):
            self.local_space[i].distance_vector_sum_buffer.add(
                self.received_space[i].distance_vector_sum_buffer
            )

        for star in self.local_space:
            star.update_distance_vector_sum_buffer(self.local_space)
            star.calc_force_from_buffer()
