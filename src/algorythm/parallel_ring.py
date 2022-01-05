from __future__ import annotations
from mpi4py import MPI
import mpi4py.MPI

from src.struct.space import Space
from src.struct.star import Star
from src.struct.vector_3d import Vec3d


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
