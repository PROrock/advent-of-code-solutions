from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from utils.grid_utils import Vect, create_grid, WALL, VECTS_CLOCKWISE, inbounds, elem_at_pos, DIR_TO_VECT, inbounds_wh, \
    fill_grid, print_grid, print_grid_str

# todo
small = True
if small:
    N_FALLEN = 12
    WIDTH = HEIGHT = 7
else:
    N_FALLEN = 1024
    WIDTH = HEIGHT = 71

def load_lines():
    if small:
        file = "./1.in"
    else:
        file = "./2.in"
    return Path(file).read_text().splitlines()

@dataclass(frozen=True)
class State:
    pos: Vect

@dataclass(frozen=True)
class Node:
    state: State
    time: int
    prev_node: Optional["Node"]

    @staticmethod
    def create(coor, score, prev_node=None):
        return Node(State(coor), score, prev_node)

    @property
    def pos(self):
        return self.state.pos

    def expand(self):
        children = []
        for dir_ in VECTS_CLOCKWISE:
            new_pos = self.pos + dir_
            if inbounds_wh(new_pos, WIDTH, HEIGHT) and new_pos not in bytes:
                children.append(Node.create(new_pos, self.time + 1, self))

        # print(f"{self}: {children=}")
        return children

    def pos_path(self):
        node = self
        path = []
        while node.prev_node is not None:
            path.append(node.pos)
            node = node.prev_node
        path.append(node.pos)
        return list(reversed(path))


def search(start_pos, end_pos) -> Optional[Node]:
    visited_states = set()
    start_pos = Node.create(start_pos, 0)
    queue = deque([start_pos])
    while queue:
        node = queue.popleft()
        if node.pos == end_pos:
            print("Found end")
            return node

        if node.state in visited_states:
            # print(f"{node.state} was already visited! {node}")
            continue

        queue.extend(node.expand())
        visited_states.add(node.state)
    print("not found")
    return None

lines = load_lines()[:N_FALLEN]
bytes = [Vect(*[int(i) for i in l.split(",")]) for l in lines]
print(bytes)


found_node = search(Vect(0, 0), Vect(WIDTH - 1, HEIGHT - 1))
print(len(found_node.pos_path())-1)

# grid = create_grid(HEIGHT, WIDTH)
# grid = fill_grid(grid, bytes, "#")
# grid = fill_grid(grid, found_node.pos_path())
# print_grid_str(grid)

