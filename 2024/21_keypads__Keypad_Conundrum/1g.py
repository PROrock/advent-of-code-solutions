import itertools
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

# commented and copied, so I can time it
# from utils.grid_utils import Vect, ARR_TO_VECT

class Vect(NamedTuple):
    x: int
    y: int

    def invert(self):
        return Vect(-self.x, -self.y)

    def __add__(self, other):
        return Vect(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vect(self.x - other.x, self.y - other.y)

    def __mul__(self, multiplier):
        return Vect(self.x * multiplier, self.y * multiplier)

    def l1_dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

KEYPAD = {c: Vect(x,y) for y, line in enumerate(["789", "456", "123", "X0A"]) for x, c in enumerate(line)}
DIRPAD = {c: Vect(x,y) for y, line in enumerate(["X^A", "<v>"]) for x, c in enumerate(line)}


# N_ROBOTS = 2
N_ROBOTS = 25

def signum(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

def to_arr(diff, pos, keypad, c):
    arrs=[]
    for dim, d_arrs in zip(diff, ["<>", "^v"]):
        s = signum(dim)
        sym = "" if s == 0 else d_arrs[(s+1)//2]
        arrs.append(sym*abs(dim))
    # prefer x first
    # target_pos = keypad[c]
    if (pos.y == keypad["X"].y and keypad[c].x == keypad["X"].x) or (
            ">" in arrs[0] and pos.x != keypad["X"].x):
        arrs = arrs[::-1]  # y first
    return list(itertools.chain.from_iterable(arrs))


@lru_cache(maxsize=None)
def spath(code, is_dirpad):
    keypad = DIRPAD if is_dirpad else KEYPAD
    pos = keypad["A"]
    arrs = []
    for c in code:
        arr, pos = arrs_from_pos_to_c(pos, c, keypad)
        arrs.extend(arr)
        arrs.append("A")  # press the button labeled c
    return tuple(arrs)

def arr_split(arr, sep):
    prev_i = 0
    for i,c in enumerate(arr):
        if c==sep:
            yield arr[prev_i:i+1]
            prev_i = i+1

    # yield arr[prev_i:i+1]  # commented, so I don't have to forget last yield (because A is always the last letter)

@lru_cache(maxsize=None)
def spath_dir_rec_len(code, n) -> int:
    if n == 0:
        return len(code)

    segments = arr_split(code, "A")
    l = 0
    for s in segments:
        next_level_code = spath(s, is_dirpad=True)
        l += spath_dir_rec_len(next_level_code, n-1)
    return l

def arrs_from_pos_to_c(pos, c, keypad):
    diff = (keypad[c] - pos)
    arr = to_arr(diff, pos, keypad, c)
    return arr, keypad[c]

def process_line_a(line):
    arrs = spath(line, is_dirpad=False)
    arrs2 = spath(arrs, is_dirpad=True)
    arrs3 = spath(arrs2, is_dirpad=True)
    # print(line, len(arrs3), int(line[:-1]), "".join(arrs3))
    return len(arrs3)*int(line[:-1])

def process_line_b(line):
    arrs = spath(line, is_dirpad=False)
    l = spath_dir_rec_len(arrs, N_ROBOTS)
    return l*int(line[:-1])


lines = load_lines()
s = 0
for line in lines:
    print(line)
    # number = process_line_a(line)
    number = process_line_b(line)
    s += number
print(s)
