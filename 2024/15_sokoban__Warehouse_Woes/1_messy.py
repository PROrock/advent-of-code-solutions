import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from utils.grid_utils import print_grid, Vect, elem_at_pos, find_all_in_grid, ARR_TO_VECT, \
    find_one_in_grid, fill_grid

EMPTY = "."
BOX = "O"
BOX_L = "["
BOX_R = "]"
BOX_BOTH = "[]"


def load_lines():
    # file = "./1.s.in"
    # file = "./1.s.b.in"
    # file = "./1.in"
    file = "./2.in"
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

def snd_v(box):
    return box + Vect(1, 0)

def add_box(box):
    boxes[box] = box
    boxes[snd_v(box)] = box

def del_box(box):
    del boxes[box]
    del boxes[snd_v(box)]

lines = load_lines()
empty_line_idx = lines.index("")
grid = lines[:empty_line_idx]
# part b
grid = twice_map(grid)
print_grid(grid)

boxes_list = find_all_in_grid(grid, "[")
grid = fill_grid(grid, boxes_list, ".")
grid = fill_grid(grid, find_all_in_grid(grid, "]"), ".")
print(boxes_list)

boxes = {}
for box in boxes_list:
    add_box(box)
print(boxes)
# print_grid_str(grid)

instructions = "".join(lines[empty_line_idx + 1:])
height = len(grid)
width = len(grid[0])
print_grid(grid)
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

    def get_boxes_to_move_y(self, box_pos, dir) -> Optional[List[Vect]]:
        assert box_pos in boxes and snd_v(box_pos) in boxes

        all_boxes_to_move = [box_pos]
        for pos in [box_pos, snd_v(box_pos)]:
            new_pos = pos + dir
            if elem_at_pos(self.grid, new_pos) != EMPTY:  #wall
                return None

            box_coll_pos = self.get_box_coll_pos(new_pos)
            if box_coll_pos is not None:
                boxes_to_move = self.get_boxes_to_move_y(boxes[box_coll_pos], dir)
                if boxes_to_move is None:
                    return None
                # print(f"{pos=}, add {boxes_to_move=}")
                all_boxes_to_move.extend(boxes_to_move)
            # else pass
        return all_boxes_to_move

    def process_instruction(self, instruction):
        dir = ARR_TO_VECT[instruction]
        new_robot_pos = self.pos + dir
        # print(instruction, dir, new_robot_pos, "b:", list(boxes.keys()))

        # self.process_both(dir, new_robot_pos)
        if dir.x != 0:
            self.process_x(dir, new_robot_pos)
        else:
            self.process_y(dir, new_robot_pos)

    def process_y(self, dir, new_robot_pos):
        prev_pos = self.pos
        new_pos = prev_pos + dir
        elem = elem_at_pos(self.grid, new_pos)

        if elem == EMPTY:
            box_coll_pos = self.get_box_coll_pos(new_pos)
            if box_coll_pos is None:
                self.pos = new_robot_pos
            else:
                # if new_pos in boxes or (new_pos + Vect(-1, 0)) in boxes:
                boxes_to_move = self.get_boxes_to_move_y(boxes[box_coll_pos], dir)
                if boxes_to_move is not None:
                    self.move_boxes(boxes_to_move, dir)
                    self.pos = new_robot_pos
            # else pass
        elif elem == "#":
            pass  # cannot move, ignore instruction
        else:
            print(f"ERR: Unknown element '{elem}'")

    @staticmethod
    def get_box_coll_pos(new_pos):
        if new_pos in boxes:
            return new_pos
        return None

    def process_both(self, dir, new_robot_pos):
        first_box = None
        new_pos = self.pos + dir
        elem = elem_at_pos(self.grid, new_pos)
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

    def move_boxes(self, boxes_to_move, dir):
        boxes_to_move = set(boxes_to_move)
        for box in boxes_to_move:
            del_box(box)
        for box in boxes_to_move:
            new_box = box + dir
            add_box(new_box)

    def process_x(self, dir, new_robot_pos):
        prev_pos = self.pos
        boxes_to_move = []

        while True:
            new_pos = prev_pos + dir
            # assert inbounds(grid, new_pos)

            elem = elem_at_pos(self.grid, new_pos)
            # print(f"{new_pos=}, {elem=}, {boxes_to_move=}")
            if elem == EMPTY:
                box_coll_pos = new_pos if new_pos in boxes else None
                if box_coll_pos is None:
                    if len(boxes_to_move):
                        self.move_boxes(boxes_to_move, dir)
                    self.pos = new_robot_pos
                    break
                else:
                    boxes_to_move.append(boxes[box_coll_pos])
                    new_pos = new_pos + dir  # skip second part of the box
            elif elem == "#":
                break  # cannot move, ignore instruction
            else:
                print(f"ERR: Unknown element '{elem}'")
            prev_pos = new_pos

# todo copy process_y and create process_both, using can_move_in_dir_function, which is the single place where checking
#  of WALL is and using x and y-specific recursive functions for getting boxes to move

def process_instructions(grid, instructions):
    start_pos = find_one_in_grid(grid, "@")
    print(f"{start_pos=}")
    grid[start_pos.y][start_pos.x] = EMPTY

    s = State(grid, start_pos)
    for i in instructions:
        s.process_instruction(i)
    return s

def gps(boxes):
    s = 0
    for b in boxes:
        num = b.x + 100 * b.y
        s += num
    return s


fgrid = process_instructions(grid, instructions).grid
# fill_grid(fgrid, boxes, "[")
# print_grid(fgrid)
# a
# boxes = find_all_in_grid(grid, BOX)
# print(boxes)
# print(gps(boxes))

real_boxes=[v for k,v in boxes.items() if k==v]
print(gps(real_boxes))
