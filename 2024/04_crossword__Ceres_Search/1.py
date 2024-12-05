import re

M_and_S = {"M", "S"}

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

def coor_inbounds(coor: Vect):
    return 0 <= coor.x < width and 0 <= coor.y < height


grid = load_lines()
height = len(grid)
width = len(grid[0])
diags = [
    Vect(1, 1), # main diag
    Vect(1, -1), # minor diag
]
dirs = [
    Vect(1, 0), # hor
    Vect(0, 1), # vert
    *diags,
]


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


def find_xmas(y, line):
    matches = re.finditer(r"X", line)
    result = 0
    for m in matches:
        subresult = count_dirs(m.start(), y)
        result += subresult
    return result

def find_mas(y, line):
    matches = re.finditer(r"A", line)
    result = 0
    for m in matches:
        subresult = count_mas(m.start(), y)
        result += subresult
    return result

def count_mas(x, y):
    vect = Vect(x, y)
    for dir in diags:
        c1 = vect + dir
        c2 = vect + (dir * -1)
        if not coor_inbounds(c1) or not coor_inbounds(c2):
            return 0
        elems = {elem_at_coor(grid, c1), elem_at_coor(grid, c2)}
        if elems != M_and_S:
            return 0
    return 1



# print(Vect(1,2)+Vect(3,4))
# print(Vect(1,2)*-1)
# print(-1*Vect(1,2))

s = 0
for y, line in enumerate(grid):
    if y == 0 or y==len(grid)-1:
        continue
    # number = find_xmas(y, line)
    number = find_mas(y, line)
    s += number
print(s)
