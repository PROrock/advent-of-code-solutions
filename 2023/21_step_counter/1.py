import re
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

# ROCK = "#"
EMPTY_SPACE = "."

def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

def print_grid(grid):
    print("GRID")
    for line in grid:
        print(line)
    print("GRID END")

def get_tile(grid, coor):
    return grid[coor.y][coor.x]

class Vect(NamedTuple):
    x: int
    y: int

    def invert(self):
        return Vect(-self.x, -self.y)

    def __add__(self, other):
        return Vect(self.x + other.x, self.y + other.y)

    def l1_dist(self, other):
        return abs(self.x-other.x)+abs(self.y-other.y)


DIR_TO_VECT = {
    "N": Vect(0, -1),
    "E": Vect(1, 0),
    "S": Vect(0, 1),
    "W": Vect(-1, 0),
}
# DIRS_CLOCKWISE = list(DIR_TO_VECT)
# OPPOSITE_DIR = {dir: opposing_dir for dir, opposing_dir in zip(DIR_TO_VECT, DIRS_CLOCKWISE[2:]+DIRS_CLOCKWISE[:2])}
# print(OPPOSITE_DIR)

def coor_inbounds(coor: Vect):
    return 0 <= coor.x < width and 0 <= coor.y < height


@dataclass(frozen=True)
class Node:
    coor: Vect
    depth: int

    def expand(self):
        dirs = [dir for dir in DIR_TO_VECT]
        # if self.dir_to_here is not None:
        #     dirs.remove(OPPOSITE_DIR[self.dir_to_here])

        children = []
        for dir in dirs:
            dir_vect = DIR_TO_VECT[dir]
            new_coor = self.coor + dir_vect
            if coor_inbounds(new_coor) and get_tile(grid, new_coor) == EMPTY_SPACE:
                children.append(Node(new_coor, self.depth + 1))
        # print(f"{self}: {children=}")
        return children


def search(start_node, max_depth):
    visited_coors = set()
    visited_nodes = set()
    queue = deque([Node(start_node, 0)])
    while queue:
        node = queue.popleft()
        if node.coor in visited_coors:
            # print(f"{node.coor} was already visited! {node}")
            continue
        if node.depth > max_depth:
            # print(f"{node=} has depth bigger than {max_depth}")
            continue

        children = node.expand()
        queue.extend(children)
        visited_coors.add(node.coor)
        visited_nodes.add(node)

    # print(f"{len(visited_coors)=}")
    # print(f"{len(visited_nodes)=}")
    return visited_nodes

def find_start(grid):
    for y, line in enumerate(grid):
        if m := re.search("S", line):
            x = m.start()
            return Vect(x, y)


grid = load_lines()
height = len(grid)
width = len(grid[0])

start_coor = find_start(grid)
visited_nodes = search(start_coor, max_depth=64)
print(len([node for node in visited_nodes if node.depth%2==0]))
