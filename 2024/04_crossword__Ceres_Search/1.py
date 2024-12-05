import re

XMAS = "XMAS"
XMAS_PAT = re.compile(r"XMAS")
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

    # def l1_dist(self, other):
    #     return abs(self.x-other.x)+abs(self.y-other.y)

def coor_inbounds(coor: Vect):
    return 0 <= coor.x < width and 0 <= coor.y < height


def print_grid(grid):
    print("GRID")
    for line in grid:
        print(line)
    print("GRID END")


grid = load_lines()
height = len(grid)
width = len(grid[0])

dirs = [
    Vect(1, 0), # hor
    Vect(0, 1), # vert
    Vect(1, 1), # main diag
    Vect(1, -1), # minor diag
]

s = 0

# def process_dir(dir):
#     # hor
#     for y in range(height):
#         XMAS_PAT.find

def count_dirs(x, y):
    s = 0
    for dir in dirs:
        s+= _count_dir(x, y, dir)
        s+= _count_dir(x, y, dir*-1)
    return s

def _count_dir(x, y, dir):
    # print(x, y, dir)
    coor = Vect(x, y) + dir
    for let in XMAS[1:]:
        if not coor_inbounds(coor) or elem_at_coor(grid, coor) != let:
            return 0
        coor = coor + dir
    return 1


def process_line(y, line):
    matches = re.finditer(r"X", line)
    result = 0
    for m in matches:
        subresult = count_dirs(m.start(), y)
        result += subresult
    return result

# print(Vect(1,2)+Vect(3,4))
# print(Vect(1,2)*-1)
# print(-1*Vect(1,2))

# for dir in dirs:
    # number = process_dir(dir)
for y, line in enumerate(grid):
    number = process_line(y, line)
    # print(y, number)
    s += number
print(s)
