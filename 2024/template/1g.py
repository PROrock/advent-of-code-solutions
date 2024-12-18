from pathlib import Path
from typing import NamedTuple


def load_lines():
    file = "./1.in"
    # file = "./2.in"
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

def coor_inbounds(coor: Vect):
    return 0 <= coor.x < width and 0 <= coor.y < height

def as_ints(grid):
    ints = []
    for line in grid:
        ints.append([-1 if i=="." else int(i) for i in line])
    return ints

def print_grid(grid):
    print("GRID")
    for line in grid:
        print(line)
    print("GRID END")

def find_all_in_grid(grid, val):
    r = []
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == val:
                r.append(Vect(x, y))
    return r
# def find_all_in_grid_re(grid, char_):
#     r = []
#     for y, line in enumerate(grid):
#         for m in re.finditer(char_, line):
#             r.append(Vect(m.start(), y))
#     return r

DIR_TO_VECT = {
    "N": Vect(0, -1),
    "E": Vect(1, 0),
    "S": Vect(0, 1),
    "W": Vect(-1, 0),
}
DIRS_CLOCKWISE = list(DIR_TO_VECT.values())

def expand(node, grid, level):
    children = []
    for dir_vect in DIRS_CLOCKWISE:
        new_coor = node + dir_vect
        if coor_inbounds(new_coor) and elem_at_coor(grid, new_coor) == level:
            children.append(new_coor)
    return children

grid = load_lines()
grid = as_ints(grid)
height = len(grid)
width = len(grid[0])

def TODO():
    s = 0

    return s

print(TODO())
