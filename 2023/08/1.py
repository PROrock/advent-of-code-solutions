import re
import sys

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

    source, left, right = re.fullmatch(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", line).groups()
    # print(match.groups())
    graph[source] = (left, right)


# for n in graph:
#     print(n, graph[n])

s = 0
node = "AAA"
instruction_idx = 0
while node != "ZZZ":
    s += 1
    instruction = instructions[instruction_idx]
    new_node = graph[node][instruction]
    # print(s, instruction_idx, instruction, node, new_node)

    instruction_idx = (instruction_idx + 1) % n_instructions
    node = new_node

print(s)
