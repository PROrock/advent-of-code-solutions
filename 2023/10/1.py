from __future__ import annotations

import re
import sys
from collections import deque
from dataclasses import dataclass
from typing import NamedTuple, Optional


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.


def get_tile(grid, coor):
    return grid[coor.y][coor.x]

class Vect(NamedTuple):
    x: int
    y: int

    def invert(self):
        return Vect(-self.x, -self.y)

    def __add__(self, other):
        return Vect(self.x + other.x, self.y + other.y)


dirsByTile = {
    "|": ((0, -1), (0, 1)), # a vertical  pipe connecting (0, -1), (0, 1)
    "-": ((1, 0), (-1, 0)), # a horizonta pipe connecting (1, 0), (-1, 0)
    "L": ((0, -1), (1, 0)), # a 90-degree bend connecting (0, -1), (1, 0)
    "J": ((0, -1), (-1, 0)), # a 90-degree bend connecting (0, -1), (-1, 0)
    "7": ((0, 1), (-1, 0)), # a 90-degree bend connecting (0, 1), (-1, 0)
    "F": ((0, 1), (1, 0)), # a 90-degree bend connecting (0, 1), (1, 0)
    ".": (), # ground; there is no pipe in this tile
    "S": ((0, -1), (0, 1), (1, 0), (-1, 0)), # the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has
}
dirsByTile = {k: [Vect(*dir) for dir in v] for k, v in dirsByTile.items()}


@dataclass
class Node:
    coor: Vect
    g: int
    dir_to_here: Optional[Vect]  # maybe not needed

    def expand(self):
        tile = get_tile(grid, self.coor)
        dirs = dirsByTile[tile]
        if not dirs:
            return []
        if self.dir_to_here is not None:
            reverse_dir = self.dir_to_here.invert()
            dirs = [dir for dir in dirs if dir != reverse_dir]

        children = []
        for dir in dirs:
            new_coor = self.coor + dir
            reverse_dir = dir.invert()
            new_tile = get_tile(grid, new_coor)
            new_dirs = dirsByTile[new_tile]
            if reverse_dir in new_dirs:
                # print(f"{self}: child {new_coor=}, {new_tile=}")
                children.append(Node(new_coor, self.g + 1, dir))
        return children


def load_grid():
    grid = []
    while True:
        line = sys.stdin.readline().rstrip("\r\n")
        if not line:
            break
        grid.append(line)
    return grid


def find_start(grid):
    for y, line in enumerate(grid):
        if m := re.search("S", line):
            x = m.start()
            return Vect(x, y)


grid = load_grid()
start_coor = find_start(grid)
print("start", start_coor)

def get_loop_half_len(start_coor):
    visited = set()
    queue = deque([Node(start_coor, 0, None)])
    while queue:
        node = queue.popleft()
        # r we finished?
        if node.coor in visited:
            print(f"{node.coor} was visited! {node}")
            return node.g if node.g % 2 == 0 else -1  # must be even!

        children = node.expand()
        queue.extend(children)
        visited.add(node.coor)
    return -2


print(get_loop_half_len(start_coor))

