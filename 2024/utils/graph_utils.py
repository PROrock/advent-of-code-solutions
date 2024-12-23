# ideas to add:
# UnoGraph - and make it somehow subclass of dict so we can skip the g.get_neighbours()
# UnoGraph - make it typed? (not necessarily str nodes?)
# add algorithm for searching fccs - fully-connected components? (add logic at the beginning for checking for max degree and serach in only those nodes) - if degrees equal, use alg 2024-23
# add at least 1 algorithm for spanning tree
# add alg for connected components (see CG python/medium/the-lost-files/main.py)
# add directed graph

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Set, Iterable


@dataclass
class UnoGraph:
    d: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))

    @staticmethod
    def create_from_lines(lines: Iterable[str], sep=","):
        g = UnoGraph()
        for line in lines:
            g.add_edge(*line.split(sep))
        return g

    def add_edge(self, a, b):
        self.d[a].add(b)
        self.d[b].add(a)

    def get_neighbours(self, v):
        return self.d.get(v, set())

    def v_degrees(self):
        return {v: len(ns) for v, ns in self.d.items()}

