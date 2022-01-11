from __future__ import annotations

import sys
from mpi4py import MPI
import mpi4py.MPI

from src.simulation.simulation import Simulation
from src.struct.space import Space
from src.utils.utils import Measure

star_count: int = int(sys.argv[1])
comm: mpi4py.MPI.Intracomm = MPI.COMM_WORLD
process_id: int = comm.Get_rank()
process_count: int = comm.Get_size()

if process_id == 0:
    global_space = Space.generate_space(16)
    Space.to_json(global_space)
comm.Barrier()
global_space = Space.load_json()
parallel_ring = Simulation(4, global_space, 3000)
parallel_ring.run()

# measure = Measure()
# measure.start()
# parallel_ring = Simulation(int(star_count / process_count))
# parallel_ring.run()
# measure.stop()
