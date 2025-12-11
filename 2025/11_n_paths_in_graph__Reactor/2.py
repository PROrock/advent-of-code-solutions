from functools import lru_cache
from collections import defaultdict
from pathlib import Path


def load_lines():
    # file = "./1b.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

lines = load_lines()
ig = defaultdict(list)
for line in lines:
    from_, *tos = line.split(" ")
    from_ = from_[:-1]
    # print(from_, tos)

    for to in tos:
        ig[to].append(from_)
# pprint(ig)

@lru_cache
def sum_combs(start_node: str, node: str) -> int:
    if node == start_node:
        return 1

    s=0
    for parent in ig[node]:
        s+=sum_combs(start_node, parent)
    return s

a=sum_combs("dac", "out")
b=sum_combs("fft", "dac")
c=sum_combs("svr", "fft")
print(a*b*c)
