from itertools import product
from pathlib import Path

from utils.grid_utils import transpose
from utils.utils import split_lines_by_empty_lines_general


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

def load(lines):
    locks = []
    keys = []
    for object in split_lines_by_empty_lines_general(lines):
        l = locks if object[0][0] == "#" else keys
        transposed = transpose(object[1:-1])
        height = len(transposed[0])
        heights = [c.count("#") for c in transposed]
        # print(heights)
        l.append(heights)
    return locks, keys, height

def fit(l, k):
    for a,b in zip(l, k):
        if a + b > height:
            return False
    return True

lines = load_lines()
locks, keys, height = load(lines)
s = 0
for l, k in product(locks, keys):
    number = int(fit(l, k))
    s += number
print(s)
