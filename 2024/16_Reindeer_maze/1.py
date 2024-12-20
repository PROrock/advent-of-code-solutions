import queue
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

TURN_SCORE = 1000

EMPTY_SPACE = "."
WALL = "#"

def load_lines():
    # file = "1.a.in"
    # file = "1.b.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

def elem_at_coor(grid, coor):
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

    def __mul__(self, multiplier):
        return Vect(self.x * multiplier, self.y * multiplier)

def coor_inbounds(coor: Vect):
    return 0 <= coor.x < width and 0 <= coor.y < height

def print_grid(grid):
    print("GRID")
    for line in grid:
        print(line)
    print("GRID END")

def find_all_in_grid(grid, val):
    r = []
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == val:
                r.append(Vect(x, y))
    return r

DIR_TO_VECT = {
    "N": Vect(0, -1),
    "E": Vect(1, 0),
    "S": Vect(0, 1),
    "W": Vect(-1, 0),
}
VECTS_CLOCKWISE = list(DIR_TO_VECT.values())
DIRS_CLOCKWISE = list(DIR_TO_VECT.keys())

@dataclass(frozen=True)
class State:
    coor: Vect
    facing: str


@dataclass(frozen=True)
class Node:
    state: State
    score: int

    @staticmethod
    def create(coor, facing, score):
        return Node(State(coor, facing), score)

    @property
    def coor(self):
        return self.state.coor
    @property
    def facing(self):
        return self.state.facing
    def __gt__(self, other):
        return self.score > other.score
        # todo swap when removing tuple in heap
        # return True

    def expand(self):
        children = []
        # go forward
        # todo go allthe way?
        dir_vect = DIR_TO_VECT[self.facing]
        new_coor = self.coor + dir_vect
        if elem_at_coor(grid, new_coor) != WALL:
            children.append(Node.create(new_coor, self.facing, self.score + 1))

        # turn L/R
        curr_idx = DIRS_CLOCKWISE.index(self.facing)
        left = DIRS_CLOCKWISE[(curr_idx - 1) % 4]
        right = DIRS_CLOCKWISE[(curr_idx + 1) % 4]
        for turn in [left, right]:
            children.append(Node.create(self.coor, turn, self.score + TURN_SCORE))

        # print(f"{self}: {children=}")
        return children


def search(start_node):
    visited_states = set()
    # queue = deque([Node.create(start_node, "E", 0)])
    prio_queue = queue.PriorityQueue()
    start_node = Node.create(start_node, "E", 0)
    prio_queue.put_nowait((start_node.score, start_node))
    while prio_queue:
        # node = queue.popleft()
        _, node = prio_queue.get_nowait()
        if node.coor == end_node:
            print("Found end")
            return node.score

        if node.state in visited_states:
            # print(f"{node.state} was already visited! {node}")
            continue

        children = node.expand()
        # queue.extend(children)
        for c in children:
            prio_queue.put_nowait((c.score, c))
        visited_states.add(node.state)
    return "not found"

grid = load_lines()
height = len(grid)
width = len(grid[0])

start_node = find_all_in_grid(grid, "S")[0]
end_node = find_all_in_grid(grid, "E")[0]
print(end_node)

print(search(start_node))
