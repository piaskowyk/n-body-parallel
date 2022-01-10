from __future__ import annotations
from src.struct.space import Space
from src.struct.star import Star


class Sequence:
    space: list[Star] = []

    def __init__(self, space: list[Star] = None):
        self.space = space

    def run(self, do_print=True):
        for star in self.space:
            star.calc_force(self.space)
            if do_print:
                star.force.print()
