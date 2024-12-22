from functools import lru_cache
from pathlib import Path


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

END = "$"

@lru_cache(maxsize=None)
def check(goal):
    if goal=="":
        return True

    for m in gen_matching(t, goal):
        if check(goal[len(m):]):
            return True
    return False

@lru_cache(maxsize=None)
def get_poss(goal):
    if goal=="":
        return 1

    poss = 0
    for m in gen_matching(t, goal):
        poss += get_poss(goal[len(m):])
    return poss


lines = load_lines()
patterns = lines[0].split(", ")
print(patterns)

def add_pattern(trie, p):
    node = trie
    for l in p+"$":
        if l not in node:
            node[l] = {}
            next_node = node[l]
        else:
            next_node = node[l]
        node = next_node

def create(patterns):
    trie = {}
    for p in patterns:
        add_pattern(trie, p)
    return trie

def gen_matching(trie, query):
    node = trie
    for i, l in enumerate(query):
        next_node = node.get(l)
        if next_node is None:
            return
        if END in next_node:
            yield query[:i+1]
        node = next_node


t = create(patterns)
print(t)

s = 0
for line in lines[2:]:
    # part_a
    # number = int(check(line))
    number = get_poss(line)
    s += number

print(s)
