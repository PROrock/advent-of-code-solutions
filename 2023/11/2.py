import re
import sys
from typing import NamedTuple

EXPAND_CONST=1_000_000
# 2x   374
# 10x  1030
# 100x 8410


def get_step(a, b):
    return 1 if a <= b else -1


class Vect(NamedTuple):
    x: int
    y: int

    def l1_dist(self, other, empty_rows, empty_cols):
        return self.axis_l1_dist(self.x, other.x, empty_cols) + self.axis_l1_dist(self.y, other.y, empty_rows)

    @staticmethod
    def axis_l1_dist(a, b, empty_cols):
        x_range = range(a, b, get_step(a, b))
        n_empty_in_dist = len([1 for col in empty_cols if col in x_range])
        x_dist = len(x_range) + n_empty_in_dist * (EXPAND_CONST-1)
        return x_dist

def load_grid():
    grid = []
    while True:
        line = sys.stdin.readline().rstrip("\r\n")
        if not line:
            break
        grid.append(line)
    return grid


def get_empty_rows(grid):
    empty_line = "."*len(grid[0])
    empty_lines = [y for y, line in enumerate(grid) if line == empty_line]
    return empty_lines


def get_empty_rows_and_cols(grid):
    empty_rows = get_empty_rows(grid)

    rotated_grid = ["".join(col) for col in zip(*grid)]
    empty_cols = get_empty_rows(rotated_grid)
    return empty_rows, empty_cols


def find_all_galaxies(grid):
    for y, line in enumerate(grid):
        for m in re.finditer("#", line):
            yield m.start(), y


def sum_all_shortest_paths(galaxies, empty_rows, empty_cols):
    s = 0
    for i, first_galaxy in enumerate(galaxies):
        for second_galaxy in galaxies[i+1:]:
            dist = first_galaxy.l1_dist(second_galaxy, empty_rows, empty_cols)
            s += dist
    return s


grid = load_grid()
empty_rows, empty_cols = get_empty_rows_and_cols(grid)

galaxies = [Vect(*coor) for coor in find_all_galaxies(grid)]
print(sum_all_shortest_paths(galaxies, empty_rows, empty_cols))