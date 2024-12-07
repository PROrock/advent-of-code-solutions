import re
from pathlib import Path
from typing import NamedTuple


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

    def __mul__(self, multiplier):
        return Vect(self.x * multiplier, self.y * multiplier)

def coor_inbounds(coor: Vect):
    return 0 <= coor.x < width and 0 <= coor.y < height

RIGHT_DIRS = [
    Vect(0, -1), Vect(1, 0), Vect(0, 1), Vect(-1, 0)
]
RIGHT_SYMBOLS = "^>v<"
def to_symbol(d):
    return RIGHT_SYMBOLS[RIGHT_DIRS.index(d)]

grid = load_lines()
height = len(grid)
width = len(grid[0])

def print_grid(grid):
    print("GRID")
    for line in grid:
        print(line)
    print("GRID END")

def print_visited_grid(grid, visited_pos):
    for p in visited_pos:
        line = grid[p.y]
        line = line[:p.x] + "X" + line[p.x+1:]
        grid[p.y] = line

def find_in_grid(grid, char_):
    for y, line in enumerate(grid):
        if m := re.search(re.escape(char_), line):
            return Vect(m.start(), y)
    return None

def turn_right(d):
    return RIGHT_DIRS[(RIGHT_DIRS.index(d) + 1) % 4]


def n_of_visited(start_pos, start_d):
    visited = set()
    pos = start_pos
    d = start_d
    while True:
        # print(f"{pos=}, {d=}")
        # print_visited_grid(grid, visited)
        # print_grid(grid)

        visited.add(pos)
        # next
        next_pos = pos + d
        if not coor_inbounds(next_pos):
            break
        if elem_at_coor(grid, next_pos) == "#":
            d = turn_right(d)
            # lazy to update pos here
        else:
            pos = next_pos

    # print_visited_grid(grid, visited)
    # print_grid(grid)
    return len(visited)


def would_obstacle_in_front_of_loop(pos, d, obstacle_pos):
    visited_t = set()
    visited_t.add((pos, d))

    d = turn_right(d)
    # print(f"try_obstacle_in_front_of {pos=}, {d=}")
    while True:
        next_pos = pos + d
        if not coor_inbounds(next_pos):
            return False
        while elem_at_coor(grid, next_pos) == "#" or next_pos == obstacle_pos:
            d = turn_right(d)
            next_pos = pos + d
            if not coor_inbounds(next_pos):
                return False

        pos = next_pos
        t = (pos, d)
        if t in visited_t:
            return True
        visited_t.add(t)


def n_of_loops(start_pos, start_d):
    pos = start_pos
    d = start_d
    visited_pos = set()
    obstacles = set()

    while True:
        visited_pos.add(pos)
        next_pos = pos + d
        if not coor_inbounds(next_pos):
            break
        if elem_at_coor(grid, next_pos) == "#":
            d = turn_right(d)
            # lazy to update pos here
        else:
            # skip blocking your previous path and skip already tried working obstacles
            if next_pos not in visited_pos and next_pos not in obstacles:
                if would_obstacle_in_front_of_loop(pos, d, next_pos):
                    # print("possible obstacle found at", next_pos, to_symbol(d), d, len(visited_pos))
                    obstacles.add(next_pos)
            pos = next_pos
    return len(obstacles)

start_pos = find_in_grid(grid, "^")
start_d = Vect(0, -1)

# print(n_of_visited(start_pos, start_d))
print(n_of_loops(start_pos, start_d))

# 6b: 1966 too high
# 1891 too high
# 1692 too low