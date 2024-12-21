from collections import deque, defaultdict
from pathlib import Path
from pprint import pprint
from typing import Any, List, Optional
from dataclasses import dataclass
from utils.grid_utils import DIRS_CLOCKWISE, DIR_TO_VECT, elem_at_pos, find_one_in_grid, inbounds, PrioritizedItem, \
    Vect, load_grid_str, VECTS_CLOCKWISE, inbounds_wh, WALL, fill_grid, print_grid_str, fill_grid_str

# todo
# THRES = 1
THRES = 100
def load_grid():
    # file = "./1.in"
    file = "./2.in"
    return load_grid_str(file)

@dataclass(frozen=True)
class State:
    pos: Vect

@dataclass(frozen=True)
class Node:
    state: State
    time: int
    prev_node: Optional["Node"]

    @staticmethod
    def create(pos, time, prev_node=None):
        return Node(State(pos), time, prev_node)

    @property
    def pos(self):
        return self.state.pos

    def expand(self):
        children = []
        for dir_ in VECTS_CLOCKWISE:
            new_pos = self.pos + dir_
            if inbounds(grid, new_pos) and elem_at_pos(grid, new_pos) != WALL:
                children.append(Node.create(new_pos, self.time + 1, self))
        return children

    def pos_path(self):
        node = self
        path = []
        while node.prev_node is not None:
            path.append(node.pos)
            node = node.prev_node
        path.append(node.pos)
        return list(reversed(path))

    def node_path(self):
        node = self
        path = []
        while node.prev_node is not None:
            path.append(node)
            node = node.prev_node
        path.append(node)
        return list(reversed(path))

    def node_to_time(self):
        node = self
        ntt = {}
        while node.prev_node is not None:
            ntt[node.pos] = node.time
            node = node.prev_node
        ntt[node.pos] = node.time
        return ntt


def search_normal(start_pos, end_pos) -> Optional[Node]:
    visited_states = set()
    start_node = Node.create(start_pos, 0)
    queue = deque([start_node])
    while queue:
        node = queue.popleft()
        if node.pos == end_pos:
            return node
        if node.state in visited_states:
            continue

        queue.extend(node.expand())
        visited_states.add(node.state)
    print("not found")
    return None

def fill_cheats(node, cheats):
    for dir_ in VECTS_CLOCKWISE:
        new_pos = node.pos + dir_
        # if inbounds(grid, new_pos) and elem_at_pos(grid, new_pos) == WALL:
        if elem_at_pos(grid, new_pos) == WALL:
            snd_pos = new_pos + dir_
            if inbounds(grid, snd_pos) and elem_at_pos(grid, snd_pos) != WALL:
                snd_orig_time = ntt[snd_pos]
                saved = snd_orig_time - (node.time+2)
                if saved > 0:
                    cheats[saved].append((node.pos, snd_pos))

grid = load_grid()
height = len(grid)
width = len(grid[0])

start_pos = find_one_in_grid(grid, "S")
end_pos = find_one_in_grid(grid, "E")
last_node = search_normal(start_pos, end_pos)
path = last_node.pos_path()[:-1]
print(len(path))
# print(path)
# grid = fill_grid_str(grid, last_node.pos_path())
# print_grid_str(grid)

ntt = last_node.node_to_time()
cheats = defaultdict(list)  # save -> tuple[cheat_s, cheat_e]

# search_cheating(start_pos, end_pos)
for node in last_node.node_path():
    fill_cheats(node, cheats)
# print(cheats)
# pprint(cheats)

s = 0
for saved, cheat_tuples in cheats.items():
    # print(saved, len(cheat_tuples))
    if saved >= THRES:
        s+= len(cheat_tuples)
print(s)

