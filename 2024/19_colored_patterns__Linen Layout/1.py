from pathlib import Path


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

END = "$"
# class Node:
#
# class Trie:
#
#     @staticmethod
#     def create(patterns):
#

# def check(goal):
#     ms = list(pat.finditer(goal))
#     for m in ms:
#         print(m)

def check(goal):
    # print("check", goal)
    if goal=="":
        return True

    # print(list(gen_matching(t, goal)))
    for m in gen_matching(t, goal):
        if check(goal[len(m):]):
            return True
    return False

def process_line(line):
    # print(line)
    return int(check(line))


lines = load_lines()
patterns = lines[0].split(", ")
print(patterns)
# pat_joined = "|".join(patterns)
# pat_string = f"^({pat_joined})"
# pat = re.compile(pat_string)
# print(pat_string)


def add_pattern(trie, p):
    node = trie
    for l in p+"$":
        if l not in node:
            node[l] = {}
            next_node = node[l]
        else:
            next_node = node[l]
        node = next_node
    # print(f"added {p=}, {trie}")

# todo class Trie
def create(patterns):
    trie = {}
    for p in patterns:
        add_pattern(trie, p)
    return trie

def get_matching(trie, query):
    node = trie
    matches = []
    for l in query:
        next_node = node.get(l)
        if next_node is None:
            return []
        node = next_node
        # stil to-do

def gen_matching(trie, query):
    node = trie
    for i, l in enumerate(query):
        # print(query, i, l, node)
        next_node = node.get(l)
        if next_node is None:
            return
        if END in next_node:
            yield query[:i+1]
        node = next_node


t = create(patterns)
print(t)
# 1/0

pat_del = []
# for p

# single_letter_pats = [p for p in patterns if len(p)==1]
# print(f"{single_letter_pats=}")
# c = Counter([len(p) for p in patterns])
# print(c)

s = 0
for line in lines[2:]:
    number = process_line(line)
    # 1/0
    # print(number)
    s += number

print(s)
