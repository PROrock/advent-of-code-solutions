# ideas to add:
# search w/ prioQ

import math
import re
from collections import deque
from dataclasses import field, dataclass
from pathlib import Path
from typing import NamedTuple, Any, List

from utils.utils import replace_in_str_from

WALL = "#"
EMPTY = "."


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

    def l2_dist(self, other):
        result_vect = other - self
        return math.hypot(result_vect)


# grid
def load_grid_str(file):
    return Path(file).read_text().splitlines()


def elem_at_pos(grid: List[Any], pos: Vect):
    return grid[pos.y][pos.x]


def inbounds(grid: List[Any], pos: Vect):
    return 0 <= pos.x < len(grid[0]) and 0 <= pos.y < len(grid)


def print_grid(grid):
    print("GRID")
    for line in grid:
        print(line)
    print("GRID END")


def print_grid_str(grid):
    print("GRID")
    for line in grid:
        print("".join([str(c) for c in line]))
    print("GRID END")


def find_all_in_grid(grid, val):
    return [Vect(x, y) for y, line in enumerate(grid) for x, c in enumerate(line) if c == val]


def find_one_in_grid(grid, val):
    all_ = find_all_in_grid(grid, val)
    assert len(all_) == 1
    return all_[0]


def find_all_in_grid_re(grid, char_):
    r = []
    for y, line in enumerate(grid):
        for m in re.finditer(char_, line):
            r.append(Vect(m.start(), y))
    return r


DIR_TO_VECT = {
    "N": Vect(0, -1),
    "E": Vect(1, 0),
    "S": Vect(0, 1),
    "W": Vect(-1, 0),
}
DIRS_CLOCKWISE = list(DIR_TO_VECT.keys())
VECTS_CLOCKWISE = list(DIR_TO_VECT.values())
ARR_TO_VECT = {
    "^": Vect(0, -1),
    ">": Vect(1, 0),
    "v": Vect(0, 1),
    "<": Vect(-1, 0),
}


# search, expand
def expand(pos, grid, wall=WALL):
    children = []
    for dir_ in VECTS_CLOCKWISE:
        new_pos = pos + dir_
        if inbounds(grid, new_pos) and elem_at_pos(grid, new_pos) != wall:
            children.append(new_pos)
    return children


def bfs(grid, start_pos, goal_pos):
    # todo not tried, but have bugs
    seen = set()
    q = deque([start_pos])
    while len(q):
        pos = q.popleft()
        if pos in seen:
            continue
        if pos == goal_pos:
            return pos

        seen.add(pos)

        children = expand(pos, grid)
        q.extend(children)

    print("not found")
    return None


def create_grid(height, width, init_value=EMPTY):
    grid = []
    for _ in range(height):
        grid.append([init_value for _ in range(width)])
    return grid


def fill_grid(grid, coors, value):
    for c in coors:
        grid[c.y][c.x] = value
    return grid


def fill_grid_str(grid, coors, value):
    for c in coors:
        grid[c.y] = replace_in_str_from(grid[c.y], c.x, value)
    return grid


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)
