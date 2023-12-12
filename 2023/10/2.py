from __future__ import annotations

import re
import sys
from collections import deque
from dataclasses import dataclass
from enum import IntEnum
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

    def __sub__(self, other):
        return Vect(self.x - other.x, self.y - other.y)


DIRS_BY_TILE = {
    "|": ((0, -1), (0, 1)), # a vertical  pipe connecting (0, -1), (0, 1)
    "-": ((1, 0), (-1, 0)), # a horizonta pipe connecting (1, 0), (-1, 0)
    "L": ((0, -1), (1, 0)), # a 90-degree bend connecting (0, -1), (1, 0)
    "J": ((0, -1), (-1, 0)), # a 90-degree bend connecting (0, -1), (-1, 0)
    "7": ((0, 1), (-1, 0)), # a 90-degree bend connecting (0, 1), (-1, 0)
    "F": ((0, 1), (1, 0)), # a 90-degree bend connecting (0, 1), (1, 0)
    ".": (), # ground; there is no pipe in this tile
    "S": ((0, -1), (0, 1), (1, 0), (-1, 0)), # the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has
}
DIRS_BY_TILE = {k: [Vect(*dir) for dir in v] for k, v in DIRS_BY_TILE.items()}
CORNER_TILES = set("LJ7F")
X_INCREMENTING_TILES = {"|", *CORNER_TILES}
Y_INCREMENTING_TILES = {"-", *CORNER_TILES}


@dataclass
class Node:
    coor: Vect
    g: int
    dir_to_here: Optional[Vect]

    def expand(self, grid):
        tile = get_tile(grid, self.coor)
        dirs = DIRS_BY_TILE[tile]
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
            new_dirs = DIRS_BY_TILE[new_tile]
            if reverse_dir in new_dirs:
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


def get_loop_coors(start_coor):
    visited = set()
    queue = deque([Node(start_coor, 0, None)])
    while queue:
        node = queue.popleft()
        # r we finished?
        if node.coor in visited:
            print(f"{node.coor} was visited! {node}")
            break

        children = node.expand(grid)
        queue.extend(children)
        visited.add(node.coor)
    return visited


def replace(s, replacement, idx):
    return s[:idx] + replacement + s[idx+1:]


def clear_grid(grid, loop_coors):
    cleared_grid = ["."*len(line) for line in grid]
    for coor in loop_coors:
        cleared_grid[coor.y] = replace(cleared_grid[coor.y], get_tile(grid, coor), coor.x)
    return cleared_grid


def fix_start(cleared_grid, start_coor):
    children = Node(start_coor, 0, None).expand(cleared_grid)
    child_dirs = [child.coor-start_coor for child in children]
    correct_tile = [k for k,v in DIRS_BY_TILE.items() if v == child_dirs][0]
    cleared_grid[start_coor.y] = replace(cleared_grid[start_coor.y], correct_tile, start_coor.x)
    return cleared_grid


class TileState(IntEnum):
    OUTSIDE = 0
    OUTSIDE_TO_PIPE = 1
    INSIDE = 2
    PIPE_TO_OUTSIDE = 3

    def increment_by(self, increment):
        return TileState((self.value + increment) % len(TileState))


# Sonar's Cognitive complexity 47 - this should be refactored, but isn't
def count_insides(cleared_grid):
    s = 0
    prev_line_inside = [TileState.OUTSIDE] * len(cleared_grid[0])
    prev_line_corners = [None] * len(cleared_grid[0])

    for y, line in enumerate(cleared_grid):
        new_prev_line_inside = prev_line_inside[:]
        new_prev_line_corners = prev_line_corners[:]
        x_inside = TileState.OUTSIDE
        x_corner = None
        for x, tile in enumerate(line):
            # solve next y
            if tile in Y_INCREMENTING_TILES:
                if tile in CORNER_TILES:
                    new_prev_line_corners[x] = tile if prev_line_corners[x] is None else None
                    shares_dir = prev_line_corners[x] is not None and len(set(DIRS_BY_TILE[prev_line_corners[x]]).intersection(set(DIRS_BY_TILE[tile])))
                    increment = 3 if shares_dir else 1
                else:
                    increment = 2
                new_prev_line_inside[x] = new_prev_line_inside[x].increment_by(increment)

            # solve next x
            if tile in X_INCREMENTING_TILES:
                if tile in CORNER_TILES:
                    new_x_corner = tile if x_corner is None else None
                    shares_dir = x_corner is not None and len(set(DIRS_BY_TILE[x_corner]).intersection(set(DIRS_BY_TILE[tile])))
                    x_corner = new_x_corner
                    increment = 3 if shares_dir else 1
                else:
                    increment = 2
                x_inside = x_inside.increment_by(increment)
            elif tile == ".":
                if x_inside == TileState.INSIDE and prev_line_inside[x] == TileState.INSIDE:
                    s += 1
        prev_line_inside = new_prev_line_inside
        prev_line_corners = new_prev_line_corners
    return s


N_STATES = len(TileState)

grid = load_grid()
start_coor = find_start(grid)
loop_coors = get_loop_coors(start_coor)

cleared_grid = clear_grid(grid, loop_coors)
cleared_grid = fix_start(cleared_grid, start_coor)

print(count_insides(cleared_grid))
