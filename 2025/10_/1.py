import ast
from dataclasses import dataclass
from pathlib import Path


def load_lines():
    file = "./1.in"
    # file = "./2.in"
    return Path(file).read_text().splitlines()


def process_line(line):
    target, button_sets, joltage = parse(line)


    return -1


def parse(line):
    target_raw, *buttons_raw, joltage_raw = line.split(" ")
    print(target_raw, buttons_raw, joltage_raw)
    # target_nums = [m.start() for m in re.finditer(r"(#)", target_raw[1:-1])]
    # print(target_nums)
    # target = ["."*(len(target_raw)-2)]
    target = [c == "#" for c in target_raw[1:-1]]
    # print(target)

    button_sets = [ast.literal_eval(b) for b in buttons_raw]
    button_sets = [(b,) if isinstance(b, int) else b for b in button_sets]
    # list?
    button_sets = [set(b) for b in button_sets]
    # print(button_sets)

    # buttons = [["."*len(target)] for b in button_sets]
    # buttons = [for b, b_set in zip(buttons, button_sets)]
    return target, button_sets, joltage_raw

@dataclass(frozen=True)
class State:
    state: list

@dataclass(frozen=True)
class Node:
    # XXX: can be inlined if just one list in state
    state: State
    buttons: list

# todo here
#     @staticmethod
#     def create(pos, time, prev_node=None):
#         return Node(State(pos), time, prev_node)
#
#     @property
#     def pos(self):
#         return self.state.pos
#
#     def expand(self):
#         children = []
#         for dir_ in VECTS_CLOCKWISE:
#             new_pos = self.pos + dir_
#             if inbounds(grid, new_pos) and elem_at_pos(grid, new_pos) != WALL:
#                 children.append(Node.create(new_pos, self.time + 1, self))
#         return children
#
#     def node_path(self):
#         node = self
#         path = []
#         while node.prev_node is not None:
#             path.append(node)
#             node = node.prev_node
#         path.append(node)
#         return list(reversed(path))
#
#     def pos_path(self):
#         return [node.pos for node in self.node_path()]
#
#     def node_to_time(self):
#         return {node.pos:node.time for node in self.node_path()}


lines = load_lines()
s = 0
for line in lines:
    number = process_line(line)
    # print(number)
    s += number

print(s)
