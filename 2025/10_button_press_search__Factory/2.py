import ast
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Any

from utils.utils import ints


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

def process_line(line):
    target, buttons, joltage = parse(line)
    # init_state = tuple([0 for _ in range(len(target))])
    init_state = [0 for _ in range(len(joltage))]
    # goal_node = Search(buttons).search(init_state, joltage)
    goal_node = Search(buttons).search(tuple(init_state), tuple(joltage))
    return goal_node.pressed_buttons


def parse(line):
    target_raw, *buttons_raw, joltage_raw = line.split(" ")
    print(target_raw, buttons_raw, joltage_raw)
    target = tuple([c == "#" for c in target_raw[1:-1]])

    button_sets = [ast.literal_eval(b) for b in buttons_raw]
    button_sets = [(b,) if isinstance(b, int) else b for b in button_sets]
    # button_sets = [set(b) for b in button_sets]

    joltage = ints(joltage_raw)
    return target, button_sets, joltage

@dataclass(frozen=True)
class Node:
    state: tuple
    pressed_buttons: int = 0

    def expand(self, buttons):
        children = []
        for b in buttons:
            # if b in self.pressed_buttons:
            #     continue
            # flip
            new_state = list(self.state)
            for pos in b:
                new_state[pos] += 1
            new_state = tuple(new_state)
            # print(self.state, b, new_state)

            children.append(Node(new_state, self.pressed_buttons+1))
        return children

class Search:
    def __init__(self, buttons):
        self.buttons = buttons

    def search(self, init_state: Any, goal_state: Any) -> Optional[Node]:
        # print(init_state, goal_state, self.buttons)

        visited_states = set()
        queue = deque([self._get_start_node(init_state)])

        while queue:
            node = queue.popleft()
            if node.state not in visited_states:
                if node.state == goal_state:
                    self.debug(f"found solution {node}")
                    return node

                visited_states |= {node.state}
                # XXX: over?
                if any(actual > goal for actual, goal in zip(node.state, goal_state)):
                    self.debug(f"Over goal")
                    continue

                new_nodes = node.expand(self.buttons)
                queue.extend(new_nodes)

                self.debug(node, new_nodes)
            else:
                self.debug(f"{node.state} already visited before!")

        self.debug("goal not reached")
        return None

    @staticmethod
    def _get_start_node(init_state) -> Node:
        return Node(init_state)

    @staticmethod
    def debug(*texts):
        pass
        # return print(*texts, file=sys.stderr, flush=True)


lines = load_lines()
s = 0
for line in lines:
    number = process_line(line)
    print(number, line)
    s += number

print(s)
