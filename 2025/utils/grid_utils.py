# ideas to add:
# search w/ prioQ

import math
import re
from collections import deque
from dataclasses import field, dataclass
from pathlib import Path
from typing import NamedTuple, Any, List

from utils.utils import replace_in_str_from, signum

WALL = "#"
EMPTY = "."
START = "S"
END = "E"

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

    def l2_dist(self, other):
        result_vect = other - self
        return math.hypot(*result_vect)

    def l_inf_norm(self):
        return max(abs(self.x), abs(self.y))

    def normalize_to_signs(self):
        return Vect(signum(self.x), signum(self.y))

    def area_for_grid(self, other):
        # beware of the plus one for grid!
        return (abs(self.x - other.x)+1) * (abs(self.y - other.y)+1)

class Vect3d(NamedTuple):
    x: int
    y: int
    z: int

    def invert(self):
        return Vect3d(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Vect3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vect3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, multiplier):
        return Vect3d(self.x * multiplier, self.y * multiplier, self.z * multiplier)

    def l1_dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def l2_dist(self, other):
        result_vect = other - self
        return math.hypot(*result_vect)


# grid
def load_grid_str(file):
    return Path(file).read_text().splitlines()

def elem_at_pos(grid: List[Any], pos: Vect) -> Any:
    return grid[pos.y][pos.x]

def set_elem_at_pos(grid: List[List[Any]], pos: Vect, value: Any):
    grid[pos.y][pos.x] = value  # doesn't work because strings are immutable

def set_elem_at_pos_str(grid: List[str], pos: Vect, value: str):
    # grid[pos.y][pos.x] = value  # doesn't work because strings are immutable
    line = grid[pos.y]
    grid[pos.y] = f"{line[:pos.x]}{value}{line[pos.x+1:]}"


def inbounds(grid: List[Any], pos: Vect):
    return 0 <= pos.x < len(grid[0]) and 0 <= pos.y < len(grid)

def inbounds_wh(pos: Vect, width: int, height: int):
    return 0 <= pos.x < width and 0 <= pos.y < height

def print_grid_raw(grid):
    print("GRID")
    for line in grid:
        print(line)
    print("GRID END")

def print_grid(grid):
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

def transpose(grid):
    return list(zip(*grid))

def reverse_lines_in_grid(grid):
    return tuple([line[::-1] for line in grid])

def rotate(grid, n_clockwise_quarter_turns=1):
    match n_clockwise_quarter_turns:
        case 0 | 4:
            return grid
        case 1:
            return reverse_lines_in_grid(transpose(grid))
        case 2:
            return tuple(reverse_lines_in_grid(grid)[::-1])
        case 3:
            return tuple(transpose(reverse_lines_in_grid(grid)))
        case _:
            raise NotImplementedError(f"Not implemented, just use modulo, or check for negative, or FIXME. {n_clockwise_quarter_turns}")

def flip(grid):
    # return tuple(reverse_lines_in_grid(grid))  # y-axis flip
    return tuple(grid[::-1])  # x-axis flip

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
VECT_TO_ARR = {v:a for a,v in ARR_TO_VECT.items()}
EIGHT_NEIGHBOURHOOD = [Vect(x,y) for x in [-1,0,1] for y in [-1,0,1] if x != 0 or y != 0]

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


def fill_grid(grid, coors, value="O"):
    for c in coors:
        grid[c.y][c.x] = value
    return grid


def fill_grid_str(grid, coors, value="O"):
    for c in coors:
        grid[c.y] = replace_in_str_from(grid[c.y], c.x, value)
    return grid

def save_grid_to_file(grid, filename):
    lines = ["".join([str(c) for c in line]) for line in grid]
    Path(filename).write_text("\n".join(lines))
    print(f"grid saved to file {filename}")

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)
