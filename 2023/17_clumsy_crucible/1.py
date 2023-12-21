from __future__ import annotations

import queue
from dataclasses import dataclass, field
from functools import cached_property
from itertools import islice
from pathlib import Path
from typing import NamedTuple, Optional


def load_lines():
    file = "./1.in"
    # file = "./2.in"
    # file = "./3.in"
    # file = "./4.in"
    return Path(file).read_text().splitlines()

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
DIRS_CLOCKWISE = list(DIR_TO_VECT)
OPPOSITE_DIR = {dir: opposing_dir for dir, opposing_dir in zip(DIR_TO_VECT, DIRS_CLOCKWISE[2:]+DIRS_CLOCKWISE[:2])}
# print(OPPOSITE_DIR)

def coor_inbounds(coor: Vect):
    return 0 <= coor.x < width and 0 <= coor.y < height


@dataclass
class Node():
    coor: Vect
    heat_so_far: int
    # heuristic: int
    dir_to_here: Optional[str] = None
    prev_node: Optional[Node] = field(repr=False, default=None)

    # def __init__(self):
    #     # todo until I have prio queue
    #     # self.heuristic = heuristic_func(self.coor, goal_coor)
    #     self.heuristic = 0

    @cached_property
    def heuristic(self):
        return heuristic_func(self.coor, goal_coor)
        # todo later
        # return 0

    # @property
    @cached_property
    def sort_key(self) -> int:
        return self.heat_so_far + self.heuristic

    def __gt__(self, other):
        # return self.sort_key > other.sort_key
        # todo swap when removing tuple in heap
        return True

    def __repr__(self):
        return f"Node({self.coor}, dir_here={self.dir_to_here}, f:{self.sort_key}, heat:{self.heat_so_far}, heur:{self.heuristic})"


    def last_three_dirs(self):
        return [self.dir_to_here, *[node.dir_to_here for node in islice(self.past_nodes(), 2)]]

    def last_three_dirs2(self):
        last_three_dirs = []
        node = self
        for _ in range(3):
            if node is None:
                break
            last_three_dirs.append(node.dir_to_here)
            node = node.prev_node
        return last_three_dirs

    def past_nodes(self):
        node = self.prev_node
        while node is not None:
            yield node
            node = node.prev_node


    def expand(self):
        dirs = [dir for dir in DIRS_CLOCKWISE]
        if self.dir_to_here is not None:
            dirs.remove(OPPOSITE_DIR[self.dir_to_here])

        last_three_dirs = self.last_three_dirs()
        if len(last_three_dirs) == 3 and all(last_three_dirs[0]==dir for dir in last_three_dirs):
            try:
                dirs.remove(last_three_dirs[0])
            except ValueError:
                pass
        # print(last_three_dirs, dirs)

        children = []
        for dir in dirs:
            dir_vect = DIR_TO_VECT[dir]
            new_coor = self.coor + dir_vect
            if coor_inbounds(new_coor):
                tile_heat = int(get_tile(grid, new_coor))
                children.append(Node(new_coor, self.heat_so_far + tile_heat, dir, self))
            #     # print(f"{self}: child {new_coor=}, {new_tile=}")
        return children

def heuristic_func(coor, goal_coor):
    return coor.l1_dist(goal_coor)


def cheapest_path(start_coor: Vect, goal_coor: Vect):
    visited = set()
    # prio_queue = [Node(start_coor, 0, None)]
    prio_queue = queue.PriorityQueue()
    start_node = Node(start_coor, 0)
    prio_queue.put_nowait((start_node.sort_key, start_node))
    # queue = deque([Node(start_coor, 0, None)])
    while prio_queue:
        # node = heapq.heappop(prio_queue)
        heur_value, node = prio_queue.get_nowait()
        print("Processing", node, heur_value)
        if node.coor in set([past.coor for past in node.past_nodes()]):
            print(f"{node.coor} was visited! {node}")
            continue

        # if node.coor in visited:
        #     print(f"{node.coor} was visited! {node}")
        #     # todo maybe not correct
        #     continue
        if node.coor == goal_coor:
            print("GOAL", node)
            return node

        children = node.expand()
        for child in children:
            # heapq.heappush(prio_queue, child)
            prio_queue.put_nowait((child.sort_key, child))
        visited.add(node.coor)

        # todo
        if len(visited) > 100 :
            break
    return None

def print_grid(grid):
    print("GRID")
    for line in grid:
        print(line)
    print("GRID END")


grid = load_lines()
height = len(grid)
width = len(grid[0])

start_coor = Vect(0,0)
goal_coor = Vect(width-1, height-1)
goal_node = cheapest_path(start_coor, goal_coor)
print(goal_node.heat_so_far)

path = list(reversed(goal_node.past_nodes()))
# print(path)

solution_grid = [list(line) for line in grid]
# for line in grid:

for node in path:
    solution_grid[node.coor.y][node.coor.x] = "#"

solution_grid = ["".join(line) for line in solution_grid]
print_grid(solution_grid)


