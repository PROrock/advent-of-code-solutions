import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import List

from utils.grid_utils import print_grid, print_grid_str, Vect, elem_at_pos, find_all_in_grid, ARR_TO_VECT

EMPTY = "."
BOX = "O"
BOX_L = "["
BOX_R = "]"
BOX_BOTH = "[]"


def load_lines():
    file = "./1.s.in"
    # file = "./1.in"
    # file = "./2.in"
    return Path(file).read_text().splitlines()

TWICE_MAP = {
    "#": "##",
    "O": "[]",
    ".": "..",
    "@": "@.",
}

def twice_map(grid):
    # return ["".join([TWICE_MAP[c] for c in line]) for line in grid]
    new_grid = [[list(TWICE_MAP[c]) for c in line] for line in grid]
    new_grid = [list(itertools.chain.from_iterable(line)) for line in new_grid]
    return new_grid


lines = load_lines()
empty_line_idx = lines.index("")
grid = lines[:empty_line_idx]
# part b
grid = twice_map(grid)

instructions = "".join(lines[empty_line_idx + 1:])
height = len(grid)
width = len(grid[0])

print_grid_str(grid)
print(instructions)


@dataclass
class State:
    grid: List[List[str]]
    pos: Vect

    # def process_instruction_a(self, instruction):
    #     dir = DIR_TO_VECT[instruction]
    #     new_pos = self.pos + dir
    #     elem = elem_at_coor(self.grid, new_pos)
    #     # if elem == "#"
    #     first_box = None
    #     while True:
    #         if elem == EMPTY:
    #             if first_box is not None:
    #                 self.grid[new_pos.y] = replace(self.grid[new_pos.y], BOX, new_pos.x)
    #                 self.grid[first_box.y] = replace(self.grid[first_box.y], EMPTY, first_box.x)
    #                 # self.grid[new_pos.y][new_pos.x] = "0"
    #                 # self.grid[first_box.y][first_box.x] = "."
    #             self.pos += dir
    #             break
    #         elif elem == BOX:
    #             if first_box is None:
    #                 first_box = new_pos
    #         elif elem == "#":
    #             # cannot move, ignore instruction
    #             break
    #         else:
    #             print("ERROR")
    #             print("ERROR")
    #             print("ERROR")
    #
    #         new_pos += dir
    #         elem = elem_at_coor(self.grid, new_pos)

    def can_box_move(self, box_pos, dir):
        # todo later?
        # TODO also fcking it and having them dynamically in a hashmap might be easeier than always redrawing the map...
        # check new pos
        # for both x
        # recurse
        # gather boxes pos for later usage?
        pass

    def process_instruction(self, instruction):
        dir = ARR_TO_VECT[instruction]
        new_pos = self.pos + dir
        new_robot_pos = self.pos + dir
        elem = elem_at_pos(self.grid, new_pos)
        first_box = None
        while True:
            if elem == EMPTY:
                if first_box is not None:
                    if dir.x != 0:
                        # horizontal, easier
                        # n_boxes = abs(new_pos.x-self.pos.x)//2
                        # todo grid line not as str, but as list of chars, then remove and insert element!
                        del self.grid[self.pos.y][new_pos.x]
                        self.grid[self.pos.y].insert(new_robot_pos.x, EMPTY)
                        # self.grid[new_pos.y] = replace_in_str_from(self.grid[new_pos.y], BOX_BOTH * n_boxes, (self.pos + dir).x)
                        # self.grid[new_pos.y] = replace_in_str_from(self.grid[new_pos.y], BOX_BOTH * n_boxes, (self.pos + dir).x)
                        # self.grid[new_pos.y] = replace(self.grid[new_pos.y], BOX_BOTH, new_pos.x)
                        # self.grid[first_box.y] = replace(self.grid[first_box.y], EMPTY, first_box.x)
                    else:
                        # harder
                        pass

                self.pos = new_robot_pos
                break
            elif elem == BOX_L or elem == BOX_R:
                if dir.x != 0:
                    # horizontal, easier
                    if first_box is None:
                        first_box = new_pos
                else:
                    # TODO
                    pass
            elif elem == "#":
                # cannot move, ignore instruction
                break
            else:
                print(f"ERR: Unknown element '{elem}'")

            new_pos += dir
            elem = elem_at_pos(self.grid, new_pos)


def process_instructions(grid, instructions):
    pos = find_all_in_grid(grid, "@")[0]
    print(pos)
    grid[pos.y][pos.x] = EMPTY

    s = State(grid, pos)
    for i in instructions:
        s.process_instruction(i)
    return s


def gps(grid):
    s = 0
    # todo predelat na box opening
    boxes = find_all_in_grid(grid, BOX)
    print(boxes)
    for b in boxes:
        num = b.x + 100 * b.y
        s += num
    return s


fgrid = process_instructions(grid, instructions).grid
print_grid(fgrid)
print(gps(fgrid))
