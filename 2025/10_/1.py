import ast
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Any


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

def process_line(line):
    target, buttons, joltage = parse(line)
    init_state = tuple([False for _ in range(len(target))])
    goal_node = Search(buttons).search(init_state, target)
    return len(goal_node.pressed_buttons)


def parse(line):
    target_raw, *buttons_raw, joltage_raw = line.split(" ")
    # print(target_raw, buttons_raw, joltage_raw)
    target = tuple([c == "#" for c in target_raw[1:-1]])

    button_sets = [ast.literal_eval(b) for b in buttons_raw]
    button_sets = [(b,) if isinstance(b, int) else b for b in button_sets]
    # button_sets = [set(b) for b in button_sets]
    return target, button_sets, joltage_raw

@dataclass(frozen=True)
class Node:
    state: tuple
    pressed_buttons: set

    def expand(self, buttons):
        children = []
        for b in buttons:
            if b in self.pressed_buttons:
                continue
            # flip
            new_state = list(self.state)
            for pos in b:
                new_state[pos] = not new_state[pos]
            new_state = tuple(new_state)
            # print(self.state, b, new_state)

            children.append(Node(new_state, {*self.pressed_buttons, b}))
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

                new_nodes = node.expand(self.buttons)
                queue.extend(new_nodes)
                visited_states |= {node.state}

                self.debug(node, new_nodes)
            else:
                self.debug(f"{node.state} already visited before!")

        self.debug("goal not reached")
        return None

    @staticmethod
    def _get_start_node(init_state) -> Node:
        return Node(init_state, set())

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
