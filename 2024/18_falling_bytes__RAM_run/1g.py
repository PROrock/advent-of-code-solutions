from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from utils.grid_utils import Vect, create_grid, WALL, VECTS_CLOCKWISE, inbounds, elem_at_pos, DIR_TO_VECT, inbounds_wh, \
    fill_grid, print_grid, print_grid_str

# small = True
small = False
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
    def create(pos, time, prev_node=None):
        return Node(State(pos), time, prev_node)

    @property
    def pos(self):
        return self.state.pos

    def expand(self):
        children = []
        for dir_ in VECTS_CLOCKWISE:
            new_pos = self.pos + dir_
            if inbounds_wh(new_pos, WIDTH, HEIGHT) and new_pos not in bytes:
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


def search(start_pos, end_pos) -> Optional[Node]:
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

lines = load_lines()
all_bytes = [Vect(*[int(i) for i in l.split(",")]) for l in lines]

bytes = all_bytes[:N_FALLEN]
start_pos = Vect(0, 0)
end_pos = Vect(WIDTH - 1, HEIGHT - 1)
found_node = search(start_pos, end_pos)
print(len(found_node.pos_path())-1)  # part a

path_poss = set(found_node.pos_path())

bytes_idx = N_FALLEN+1
while True:
    bytes = all_bytes[:bytes_idx]
    # print(bytes_idx)
    last_b = bytes[-1]
    if last_b in path_poss:
        found_node = search(start_pos, end_pos)
        if found_node is None:
            print(f"{last_b.x},{last_b.y}")
            break
        path_poss = set(found_node.pos_path())
    bytes_idx += 1


# grid = create_grid(HEIGHT, WIDTH)
# grid = fill_grid(grid, bytes, "#")
# grid = fill_grid(grid, found_node.pos_path())
# print_grid_str(grid)
