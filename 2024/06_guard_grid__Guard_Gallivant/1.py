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

def n_of_visited():
    visited = set()
    guard_pos = find_in_grid(grid, "^")
    print("guard_pos", guard_pos)

    pos = guard_pos
    d = Vect(0, -1)
    while coor_inbounds(pos):
        # print(f"{pos=}, {d=}")
        # print_visited_grid(grid, visited)
        # print_grid(grid)

        visited.add(pos)
        # next
        next_pos = pos + d
        if not coor_inbounds(next_pos):
            break
        if elem_at_coor(grid, next_pos) == "#":
            d = RIGHT_DIRS[(RIGHT_DIRS.index(d) + 1) % 4]
            # lazy to update pos here
        else:
            pos = next_pos

    # print_visited_grid(grid, visited)
    # print_grid(grid)
    return len(visited)


def try_obstacle(pos, d):
    visited = set()
    visited.add((pos, d))

    d = turn_right(d)
    # print(f"try_obstacle {pos=}, {d=}")
    while True:
        # print(f"{pos=}, {to_symbol(d)}, {d=}")
        # print_visited_grid(grid, visited)
        # print_grid(grid)

        # next
        next_pos = pos + d
        if not coor_inbounds(next_pos):
            return 0
        while elem_at_coor(grid, next_pos) == "#":
            d = turn_right(d)
            next_pos = pos + d
            if not coor_inbounds(next_pos):
                return 0

        pos = next_pos
        if (pos, d) in visited:
            return 1
        visited.add((pos, d))


def n_of_loops():
    s=0
    guard_pos = find_in_grid(grid, "^")
    print("guard_pos", guard_pos)

    pos = guard_pos
    visited = set()

    d = Vect(0, -1)
    while coor_inbounds(pos):
        # print(f"{pos=}, {to_symbol(d)}, {d=}")
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
            if len(visited) > 1:  # skip for starting position
                obstacle_loop = try_obstacle(pos, d)
                # if obstacle_loop:
                #     print("possible obstacle found at", next_pos, to_symbol(d), d, len(visited))
                s += obstacle_loop
            pos = next_pos

    # print_visited_grid(grid, visited)
    # print_grid(grid)
    return s

def turn_right(d):
    return RIGHT_DIRS[(RIGHT_DIRS.index(d) + 1) % 4]


# print(n_of_visited())
print(n_of_loops())

# 6b: 1966 too high
