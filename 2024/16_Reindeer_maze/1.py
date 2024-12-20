import queue
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from utils.grid_utils import DIRS_CLOCKWISE, DIR_TO_VECT, elem_at_pos, find_one_in_grid, PrioritizedItem, Vect

TURN_SCORE = 1000
EMPTY_SPACE = "."
WALL = "#"

def load_lines():
    # file = "1.a.in"
    # file = "1.b.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

def coor_inbounds(coor: Vect):
    return 0 <= coor.x < width and 0 <= coor.y < height

@dataclass(frozen=True)
class State:
    coor: Vect
    facing: str

@dataclass(frozen=True)
class Node:
    state: State
    score: int
    prev_node: Optional["Node"]

    @staticmethod
    def create(coor, facing, score, prev_node=None):
        return Node(State(coor, facing), score, prev_node)

    @property
    def coor(self):
        return self.state.coor
    @property
    def facing(self):
        return self.state.facing

    def expand(self):
        children = []
        # go forward (1 step only)
        dir_vect = DIR_TO_VECT[self.facing]
        new_coor = self.coor + dir_vect
        if elem_at_pos(grid, new_coor) != WALL:
            children.append(Node.create(new_coor, self.facing, self.score + 1, self))

        # turn L/R
        curr_idx = DIRS_CLOCKWISE.index(self.facing)
        left = DIRS_CLOCKWISE[(curr_idx - 1) % 4]
        right = DIRS_CLOCKWISE[(curr_idx + 1) % 4]
        for turn in [left, right]:
            children.append(Node.create(self.coor, turn, self.score + TURN_SCORE, self))

        # print(f"{self}: {children=}")
        return children

    def coor_path(self):
        node = self
        path = []
        while node.prev_node is not None:
            path.append(node.coor)
            node = node.prev_node
        path.append(node.coor)
        return list(reversed(path))


grid = load_lines()
height = len(grid)
width = len(grid[0])


def search_score(start_node):
    visited_states = set()
    prio_queue = queue.PriorityQueue()
    start_node = Node.create(start_node, "E", 0)
    prio_queue.put_nowait((start_node.score, start_node))
    while prio_queue:
        _, node = prio_queue.get_nowait()
        if node.coor == end_node:
            print("Found end")
            return node.score

        if node.state in visited_states:
            # print(f"{node.state} was already visited! {node}")
            continue

        children = node.expand()
        for c in children:
            prio_queue.put_nowait((c.score, c))
        visited_states.add(node.state)
    return "not found"

def search_best_coors(start_node):
    best_score_for_state = {}
    prio_queue = queue.PriorityQueue()
    start_node = Node.create(start_node, "E", 0)
    prio_queue.put_nowait(PrioritizedItem(start_node.score, start_node))
    best_score = None
    best_coors = set()

    while not prio_queue.empty():
        node = prio_queue.get_nowait().item
        if best_score is not None and node.score > best_score:
            # print("this is worse than found best", node)
            continue

        if node.coor == end_node:
            # print("Found end w/ score", node.score)
            if best_score is None:
                best_score = node.score

            # print("visited_tiles", node.coor_path())
            for c in node.coor_path():
                best_coors.add(c)
            continue

        if node.state in best_score_for_state:
            if node.score > best_score_for_state[node.state]:
                # print(f"{node.state} was already visited w/ worse score! {node}")
                continue
            # assert node.score == best_score_for_state[node.state]

        children = node.expand()
        for c in children:
            prio_queue.put_nowait(PrioritizedItem(c.score, c))
        best_score_for_state[node.state] = node.score

    # grid_to_print = fill_grid_str(grid, best_coors, "O")
    # print_grid(grid_to_print)
    return len(best_coors)


start_node = find_one_in_grid(grid, "S")
end_node = find_one_in_grid(grid, "E")

# print(search_score(start_node))
print(search_best_coors(start_node))

# TODO: make faster than 36s!
