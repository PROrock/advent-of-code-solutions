import itertools
import string
from collections import defaultdict

from pathlib import Path
from typing import NamedTuple

FREQS = set(string.ascii_letters + string.digits)

def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

def elem_at_coor(grid, coor):
    return grid[coor.y][coor.x]


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

    def compute_antinodes(self, other):
        ab_vect = other - self
        return other + ab_vect, self - ab_vect


def coor_inbounds(coor: Vect):
    return 0 <= coor.x < width and 0 <= coor.y < height

grid = load_lines()
height = len(grid)
width = len(grid[0])

def print_grid(grid):
    print("GRID")
    for line in grid:
        print(line)
    print("GRID END")

def find_antennas(grid):
    antennas = defaultdict(list)
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c in FREQS:
                antennas[c].append(Vect(x, y))
    return antennas

def find_antinodes(antennas):
    antinodes = set()
    for antenna, positions in antennas.items():
        if len(positions) == 1:
            continue

        pos_pairs = itertools.combinations(positions, 2)
        for a,b in pos_pairs:
            pair_ans = a.compute_antinodes(b)
            for antinode in pair_ans:
                if coor_inbounds(antinode):
                    antinodes.add(antinode)
    return antinodes


def ans_from_in_dir(pos, vect):
    antinodes = set()
    while(coor_inbounds(pos)):
        antinodes.add(pos)
        pos = pos + vect
    return antinodes


def find_antinodes_b(antennas):
    antinodes = set()
    for antenna, positions in antennas.items():
        if len(positions) == 1:
            continue

        pos_pairs = itertools.combinations(positions, 2)
        for a,b in pos_pairs:
            ab_vect = b - a
            antinodes |= ans_from_in_dir(b, ab_vect)
            antinodes |= ans_from_in_dir(a, ab_vect*-1)
    return antinodes

antennas = find_antennas(grid)
# antinodes = find_antinodes(antennas)
antinodes = find_antinodes_b(antennas)
print(len(antinodes))
