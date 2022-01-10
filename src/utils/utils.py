from __future__ import annotations
from timeit import default_timer as timer

from mpi4py import MPI
import mpi4py.MPI


class Measure:
    comm: mpi4py.MPI.Intracomm = MPI.COMM_WORLD
    process_id: int = comm.Get_rank()
    process_count: int = comm.Get_size()

    start_timestamp: float = 0
    stop_timestamp: float = 0

    def start(self):
        self.start_timestamp = timer()

    def stop(self):
        if self.process_id == 0:
            self.stop_timestamp = timer()
            print(f'{self.stop_timestamp - self.start_timestamp}')
