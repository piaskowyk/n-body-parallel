from __future__ import annotations
from timeit import default_timer as timer

from src.algorythm.parallel_ring import ParallelRing
from src.algorythm.sequence import Sequence
from src.simulation.simulation import Simulation
from src.struct.space import Space
from src.struct.star import Star
from src.utils.utils import Measure

from mpi4py import MPI
import mpi4py.MPI

comm: mpi4py.MPI.Intracomm = MPI.COMM_WORLD
process_id: int = comm.Get_rank()
process_count: int = comm.Get_size()
# # global_space = []
# # if process_id == 0:
# #     global_space = Space.generate_space(16)
# #     Space.to_json(global_space)
# global_space = Space.load_json()
#
# parallel_ring = Simulation(4, global_space)
# parallel_ring.run()
#
# sequence = Sequence()
# sequence.space = global_space
# sequence.run(False, False)


measure = Measure()
measure.start()
parallel_ring = ParallelRing(1000)
parallel_ring.run()
if process_id == 0:
    measure.stop()
#
# sequence = Sequence()
# sequence.space = global_space
# sequence.run(False, False)

def is_same_star(star_a: Star, star_b: Star) -> bool:
    return star_a.position.x == star_b.position.x \
        and star_a.position.y == star_b.position.y \
        and star_a.position.z == star_b.position.z \
        and star_a.mass == star_b.mass


def is_same_force(star_a: Star, star_b: Star) -> bool:
    return star_a.force.x == star_b.force.x \
        and star_a.force.y == star_b.force.y \
        and star_a.force.z == star_b.force.z


# for parallel_star in parallel_ring.local_space:
#     exists = False
#     for global_star in global_space:
#         if is_same_star(parallel_star, global_star):
#             exists = True
#             if not is_same_force(parallel_star, global_star):
#                 print("ERROR")
#     if not exists:
#         print("ERROR NOT EXISTS")
