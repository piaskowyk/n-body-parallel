from __future__ import annotations
from src.algorythm.parallel_ring import ParallelRing
from src.algorythm.sequence import Sequence
from src.struct.space import Space
from src.struct.star import Star

global_space = Space.generate_space(16)

parallel_ring = ParallelRing(4, global_space)
parallel_ring.run()

sequence = Sequence()
sequence.space = global_space
sequence.run(False, False)


def is_same_star(star_a: Star, star_b: Star) -> bool:
    return star_a.position.x == star_b.position.x \
        and star_a.position.y == star_b.position.y \
        and star_a.position.z == star_b.position.z \
        and star_a.mass == star_b.mass


for parallel_star in parallel_ring.local_space:
    for global_star in global_space:
        if is_same_star(parallel_star, global_star):
            if parallel_star.force != global_star.force:
                print("ERROR")
