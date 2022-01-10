from __future__ import annotations

import sys
from mpi4py import MPI
import mpi4py.MPI

from src.algorythm.sequence import Sequence
from src.struct.space import Space
from src.utils.utils import Measure

star_count: int = int(sys.argv[1])
comm: mpi4py.MPI.Intracomm = MPI.COMM_WORLD
process_count: int = comm.Get_size()

measure = Measure()
measure.start()
sequence = Sequence(Space.generate_space(star_count))
sequence.run(False)
measure.stop()
