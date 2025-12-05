import math
import re
import sys
from functools import lru_cache

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
    return nodes, s


def move_by_steps_without_checking():
    s = 0
    nodes = [n for n in graph if n[-1] == "A"]
    for n in nodes:
        n_steps, terminal_node = find_first_terminal_node(n, s)
        print(n_steps, terminal_node)
    new_steps_rest, s = move_by_steps(nodes[:-1], s, n_steps)
    # print(new_steps_rest)
    new_nodes = [*new_steps_rest, terminal_node]
    nodes = new_nodes
    print(nodes)
    # s += n_steps
    while not all(n[-1] == "Z" for n in nodes):
        # print("repeat is needed")
        print(s, n_steps, nodes)
        nodes, s = move_by_steps(nodes, s, 1)
        # s += 1

        n_steps, terminal_node = find_first_terminal_node(nodes[-1], s)
        # print(n_steps, terminal_node)
        # todo less effective but stats!
        # for n in nodes:
        #     n_steps, terminal_node = find_first_terminal_node(n, s)
        #     print(n_steps, terminal_node)

        new_steps_rest, s = move_by_steps(nodes[:-1], s, n_steps)
        new_nodes = [*new_steps_rest, terminal_node]
        nodes = new_nodes
        # print(nodes)
        # s += n_steps
    print(s)

# move_by_steps_without_checking()

@lru_cache(maxsize=None)
def move_by_steps_inner(node, instruction_idx, n_steps):
    print(f"Node {node}, idx {instruction_idx} cache miss")
    s = instruction_idx
    for _ in range(n_steps):
        instruction = instructions[s % n_instructions]
        s += 1
        node = graph[node][instruction]
    return node


def move_by_steps_cached(nodes, s, n_steps):
    new_nodes = [move_by_steps_inner(node, s%n_instructions, n_steps) for node in nodes]
    return new_nodes, s+n_steps


# PERIOD = n_instructions
def move_by_steps_without_checking_by_283():
    s = 0
    nodes = [n for n in graph if n[-1] == "A"]

    nodes, s = move_by_steps(nodes, s, 1)
    print(s, nodes)

    while not all(n[-1] == "Z" for n in nodes):
        # print("repeat is needed")
        nodes, s = move_by_steps_cached(nodes, s, n_instructions)
        print(s)
        # print(s, nodes)

    print(s)
# move_by_steps_without_checking_by_283()

def move_by_steps_without_checking_by_terminal_period():
    s = 0
    nodes = [n for n in graph if n[-1] == "A"]

    nodes, s = move_by_steps(nodes, s, 1)
    print(s, nodes)

    first_node_period, terminal_node = find_first_terminal_node(nodes[0], s)
    print(first_node_period, terminal_node)

    while not all(n[-1] == "Z" for n in nodes):
        # print("repeat is needed")
        nodes, s = move_by_steps_cached(nodes, s, first_node_period)
        print(s)
        # print(s, nodes)

    print(s)


# move_by_steps_without_checking_by_terminal_period()  # still not fast enough


####

# compute periods - try 3 times the same number and divisible by 283
# compute tha common number
# for 2 and 3 it's 6, so its smallest common multiplier?


def compute_periods():
    s = 0
    nodes = [n for n in graph if n[-1] == "A"]

    nodes, s = move_by_steps(nodes, s, 1)
    print(s, nodes)
    start_s = s

    for node in nodes:
        s = start_s
        history = []
        for _ in range(3):
            # print("find_term", node, s)
            n_steps, terminal_node = find_first_terminal_node(node, s)
            s += n_steps
            # print(n_steps, n_steps%n_instructions, s, terminal_node, s % n_instructions)
            history.append(n_steps + 1)

            moved, s = move_by_steps([terminal_node], s, 1)
            node = moved[0]
            # print(n_steps, s, terminal_node, s % n_instructions)

        # print(history)
        # print([h%n_instructions for h in history])

        # if all([h == history[0] for h in history]) and history[0]%n_instructions==0:
        if all([h == history[0] for h in history]):
            yield history[0]
        else:
            print(f"PROBLEM with: {history=}")


def smallest_common_multiplier_naive(*numbers):
    # naive approach, still too slow
    biggest_num = max(numbers)
    print(biggest_num)
    i = biggest_num
    other_numbers = [num for num in numbers if num != biggest_num]
    while not all(num%biggest_num==0 for num in other_numbers):
        i+= biggest_num
        # print(i)
    return i


def smallest_common_multiplier_for_two(a, b):
    gcd_ = math.gcd(a, b)
    return a//gcd_ * b


def smallest_common_multiplier(*numbers):
    # impl. seems to be working correctly
    result, *rest_of_numbers = numbers
    for num in rest_of_numbers:
        new_result = smallest_common_multiplier_for_two(result, num)
        result = new_result

    for n in numbers:
        print(n, result%n==0)
    return result


periods = list(compute_periods())
print(periods)

print(smallest_common_multiplier(*periods))


# def test_scm():
#     assert smallest_common_multiplier_for_two(2, 6) == 6
#     assert smallest_common_multiplier_for_two(3, 5) == 15
#     assert smallest_common_multiplier_for_two(6, 15) == 30
#     assert smallest_common_multiplier(6, 15) == 30
#     assert smallest_common_multiplier(6, 15, 30) == 30
#     assert smallest_common_multiplier(1, 6, 15, 30) == 30
#     assert smallest_common_multiplier(3, 15, 30) == 30
#     assert smallest_common_multiplier(2, 3, 5) == 30
#     print("tests ok")
#
#
# test_scm()
