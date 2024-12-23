from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Dict, Set


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

@dataclass
class UnoGraph:
    d: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))

    def add_edge(self, a, b):
        self.d[a].add(b)
        self.d[b].add(a)

    def get_neighbours(self, v):
        return self.d.get(v, set())

    def get_vert_degrees(self):
        return {v: len(ns) for v, ns in self.d.items()}


def all_triangles(ts):
    triangles = set()
    for t in ts:
        ns = g.get_neighbours(t)
        pairs = combinations(ns, r=2)
        for a, b in pairs:
            if b in g.get_neighbours(a):
                triangles.add(tuple(sorted((t, a, b))))
    return triangles


lines = load_lines()
g = UnoGraph()
ts = set()
for line in lines:
    a,b = line.split("-")
    g.add_edge(a,b)
    for v in [a,b]:
        if v.startswith("t"):
            ts.add(v)

#a
# print(len(all_triangles(ts)))
#b

v2d = g.get_vert_degrees()
# print(v2d)
# print(sorted(v2d.items(), key=lambda t:t[1]))
# all the same!

def max_fcc():
    md = max(v2d.values())
    # search for fcc of size md+1
    for i in range(md, 2, -1):
        for v in g.d:
            cands = combinations(g.get_neighbours(v), r=i)
            for c in cands:
                c = set(c) | {v}
                if check_c(c):
                    return c

def check_c(c):
    for cv in c:
        if not (c-{cv}) <= g.get_neighbours(cv):
            return False
    return True

c = max_fcc()
print(",".join(sorted(list(c))))
