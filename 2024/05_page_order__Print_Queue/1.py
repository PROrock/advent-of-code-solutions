from collections import defaultdict
from pathlib import Path


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

def process_line(line):
    valid = is_valid(line)
    if valid:
        return line[len(line)//2]
    return 0

def is_valid(line):
    prevs = set()
    for i in line:
        if len(rules.get(i, set()) & prevs):
            return False
        prevs.add(i)
    return True


lines = load_lines()
rules = defaultdict(list)
updates = []
only_updates = False
for line in lines:
    if line == "":
        only_updates = True
        continue
    if only_updates:
        updates.append([int(i) for i in line.split(",")])
    else:
        first, second = [int(i) for i in line.split("|")]
        rules[first].append(second)

# print(rules)
# print(updates)
rules = {k:set(v) for k, v in rules.items()}

s = 0
for line in updates:
    number = process_line(line)
    # print(number)
    s += number

print(s)
