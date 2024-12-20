from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple, List

EMPTY = "."
BOX = "O"


def load_lines():
    # file = "./1.s.in"
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
    "^": Vect(0, -1),
    ">": Vect(1, 0),
    "v": Vect(0, 1),
    "<": Vect(-1, 0),
}
DIRS_CLOCKWISE = list(DIR_TO_VECT.values())

def expand(node, grid, level):
    children = []
    for dir_vect in DIRS_CLOCKWISE:
        new_coor = node + dir_vect
        if coor_inbounds(new_coor) and elem_at_coor(grid, new_coor) == level:
            children.append(new_coor)
    return children

lines = load_lines()
empty_line_idx = lines.index("")
grid=lines[:empty_line_idx]
instructions = "".join(lines[empty_line_idx+1:])
height = len(grid)
width = len(grid[0])

# print_grid(grid)
# print(instructions)

def replace(s, replacement, idx):
    return f"{s[:idx]}{replacement}{s[idx + 1:]}"


@dataclass
class State:
    grid: List[str]
    pos: Vect

    def process_instruction(self, instruction):
        dir = DIR_TO_VECT[instruction]
        new_pos = self.pos + dir
        elem = elem_at_coor(self.grid, new_pos)
        # if elem == "#"
        first_box = None
        while True:
            if elem == EMPTY:
                if first_box is not None:
                    self.grid[new_pos.y] = replace(self.grid[new_pos.y], BOX, new_pos.x)
                    self.grid[first_box.y] = replace(self.grid[first_box.y], EMPTY, first_box.x)
                    # self.grid[new_pos.y][new_pos.x] = "0"
                    # self.grid[first_box.y][first_box.x] = "."
                self.pos += dir
                break
            elif elem == BOX:
                if first_box is None:
                    first_box = new_pos
            elif elem == "#":
                # cannot move, ignore instruction
                break
            else:
                print("ERROR")
                print("ERROR")
                print("ERROR")

            new_pos += dir
            elem = elem_at_coor(self.grid, new_pos)

        # todo save grid and pos

def process_instructions(grid, instructions):
    pos = find_all_in_grid(grid, "@")[0]
    print(pos)
    grid[pos.y] = replace(grid[pos.y], EMPTY, pos.x)
    # grid[pos.y][pos.x] = "."

    s = State(grid, pos)
    for i in instructions:
        s.process_instruction(i)
    return s

def gps(grid):
    s = 0
    boxes = find_all_in_grid(grid, BOX)
    print(boxes)
    for b in boxes:
        num = b.x + 100*b.y
        s+= num
    return s


fgrid = process_instructions(grid, instructions).grid
print_grid(fgrid)
print(gps(fgrid))
