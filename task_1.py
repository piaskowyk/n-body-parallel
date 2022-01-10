from __future__ import annotations

import sys
from mpi4py import MPI
import mpi4py.MPI

from src.algorythm.parallel_ring import ParallelRing
from src.utils.utils import Measure

star_count: int = int(sys.argv[1])
comm: mpi4py.MPI.Intracomm = MPI.COMM_WORLD
process_count: int = comm.Get_size()

measure = Measure()
measure.start()
parallel_ring = ParallelRing(int(star_count / process_count))
parallel_ring.run()
measure.stop()
