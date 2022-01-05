from __future__ import annotations
from src.struct.space import Space
from src.struct.star import Star


class Sequence:
    space: list[Star] = []

    def run(self, generate_space=True, do_print=True):
        if generate_space:
            self.space = Space.generate_space(5)
        for star in self.space:
            star.calc_force(self.space)
            if do_print:
                star.force.print()
