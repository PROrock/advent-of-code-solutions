import re
import sys
from typing import NamedTuple


class Vect(NamedTuple):
    x: int
    y: int

    def l1_dist(self, other):
        return abs(self.x-other.x)+abs(self.y-other.y)


def load_grid():
    grid = []
    while True:
        line = sys.stdin.readline().rstrip("\r\n")
        if not line:
            break
        grid.append(line)
    return grid


def expand_rows(grid):
    empty_line = "."*len(grid[0])
    expanded_grid = []
    for line in grid:
        expanded_grid.append(line)
        if line == empty_line:
            expanded_grid.append(line)  # 2nd append
    return expanded_grid


def expand_universe(grid):
    row_expanded_grid = expand_rows(grid)
    # columns now
    rotated_half_expanded_grid = ["".join(col) for col in zip(*row_expanded_grid)]
    expanded_grid = expand_rows(rotated_half_expanded_grid)
    return ["".join(line) for line in zip(*expanded_grid)]


def find_all_galaxies(grid):
    for y, line in enumerate(grid):
        for m in re.finditer("#", line):
            yield m.start(), y

def sum_all_shortest_paths(galaxies):
    s = 0
    for i, first_galaxy in enumerate(galaxies):
        for second_galaxy in galaxies[i+1:]:
            dist = first_galaxy.l1_dist(second_galaxy)
            # print(first_galaxy, second_galaxy, dist)
            s+=dist
    return s


grid = load_grid()
expanded_grid = expand_universe(grid)

galaxies = [Vect(*coor) for coor in find_all_galaxies(expanded_grid)]
print(sum_all_shortest_paths(galaxies))