import re
import sys
from collections import deque
from dataclasses import dataclass

instructions = sys.stdin.readline().rstrip("\r\n")
# print(instructions)
instructions = [int(i == "R") for i in instructions]
# print(instructions)
n_instructions = len(instructions)
sys.stdin.readline()  # skip empty line

graph = {}
while True:
    line = sys.stdin.readline().rstrip("\r\n")
    if not line:
        break

    source, left, right = re.fullmatch(r"(\w{3}) = \((\w{3}), (\w{3})\)", line).groups()
    # print(match.groups())
    graph[source] = (left, right)


# for n in graph:
    ## print(n, graph[n])
    # for tn in graph[n]:
    #     print(f"\"{n}\" -> \"{tn}\";")
# print()
# sys.exit(1)


def brute_force_probably():
    # global s, nodes, history
    s = 0
    nodes = [n for n in graph if n[-1] == "A"]
    # print(nodes)
    # print(f"{len(nodes)=}")
    # terminal_nodes = [n for n in graph if n[-1] == 'Z']
    # print(f"{len(terminal_nodes)}, {terminal_nodes=}")
    history = []
    history.append(nodes)
    # counter
    # s< 1000 and
    # while not all([n[-1] == "Z" for n in nodes]):
    #     instruction = instructions[s % n_instructions]
    #     s += 1
    #
    #     new_nodes = [graph[node][instruction] for node in nodes]
    #     z_nodes = [n for n in nodes if n[-1] == "Z"]
    #     print(s, instruction, nodes, new_nodes, len(z_nodes), z_nodes)
    #     # history.append(new_nodes)
    #     nodes = new_nodes


# brute_force_probably()


# find first terminal node, go that steps in all other nodes and check if we are there
def find_first_terminal_node(starting_node, s):
    orig_s = s
    node = starting_node
    # s=0
    while node[-1] != "Z":
        instruction = instructions[s % n_instructions]
        s += 1
        new_node = graph[node][instruction]
        # print(s, instruction, node, new_node)
        node = new_node
    return s-orig_s, node


def move_by_steps(nodes, s, n_steps):
    for _ in range(n_steps):
        instruction = instructions[s % n_instructions]
        s += 1
        nodes = [graph[node][instruction] for node in nodes]
    return nodes


def terminal_period_probe():
    s = 0
    nodes = [n for n in graph if n[-1] == "A"]
    # n_steps, terminal_node = find_first_terminal_node(nodes[0])
    # print(n_steps, terminal_node)
    # new_steps_rest = move_other_by_steps(nodes[1:], n_steps)
    # print(new_steps_rest)
    # if all([n[-1] == "Z" for n in new_steps_rest]):
    #     # finito
    #     s+=n_steps
    #     print(s)
    #     sys.exit(1)
    # else:
    #     print("repeat is needed")
    for n in nodes:
        s = 0
        for _ in range(25):
            n_steps, terminal_node = find_first_terminal_node(n, s)
            s += n_steps
            print(n_steps, n_steps%n_instructions, s, terminal_node, s % n_instructions)

            moved = move_by_steps([terminal_node], s, 1)
            n = moved[0]
            s += 1
            # print(n_steps, s, terminal_node, s % n_instructions)


terminal_period_probe()
# sys.exit(1)

def move_by_steps_without_checking():
    s = 0
    nodes = [n for n in graph if n[-1] == "A"]
    for n in nodes:
        n_steps, terminal_node = find_first_terminal_node(n, s)
        print(n_steps, terminal_node)
    new_steps_rest = move_by_steps(nodes[:-1], s, n_steps)
    # print(new_steps_rest)
    new_nodes = [*new_steps_rest, terminal_node]
    nodes = new_nodes
    print(nodes)
    s += n_steps
    while not all(n[-1] == "Z" for n in nodes):
        # print("repeat is needed")
        print(s, n_steps, nodes)
        nodes = move_by_steps(nodes, s, 1)
        s += 1

        n_steps, terminal_node = find_first_terminal_node(nodes[-1], s)
        # print(n_steps, terminal_node)
        # todo less effective but stats!
        # for n in nodes:
        #     n_steps, terminal_node = find_first_terminal_node(n, s)
        #     print(n_steps, terminal_node)

        new_steps_rest = move_by_steps(nodes[:-1], s, n_steps)
        new_nodes = [*new_steps_rest, terminal_node]
        nodes = new_nodes
        # print(nodes)
        s += n_steps
    print(s)


# move_by_steps_without_checking()


# search, jestli perioda 283 do cile je vzdy a u vsech podgrafu
# pokud ano, da se napocitat nebo memo po 283, kdyz jsem na pozici x, kde budu

@dataclass
class Node:
    name: str
    g: int

    def is_goal(self):
        return self.name[-1] == "Z"

    def expand(self):
        children = []
        for new_node in graph[self.name]:
            children.append(Node(new_node, self.g+1))
        return children


def search(start_node):
    visited = set()
    queue = deque([Node(start_node, 0)])
    while queue:
        node = queue.popleft()
        # r we finished?
        if node.name in visited:
            print(f"{node.name} was already visited! {node}")
            continue
        if node.is_goal():
            print(f"{node} is goal! {len(visited)=}")
            # print("now try this w/o this condition!")
            # return None

        children = node.expand()
        queue.extend(children)
        visited.add(node.name)
    print(f"{len(visited)=}")
    return -2


def search_probe():
    nodes = [n for n in graph if n[-1] == "A"]
    # search(nodes[0])
    for starting_node in nodes:
        search(starting_node)
        print()


# search_probe()

