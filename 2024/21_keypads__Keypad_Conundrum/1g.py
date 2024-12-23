from pathlib import Path
from typing import Any, List
from dataclasses import dataclass
from utils.grid_utils import DIRS_CLOCKWISE, DIR_TO_VECT, elem_at_pos, find_one_in_grid, inbounds, PrioritizedItem, \
    Vect, load_grid_str, ARR_TO_VECT

KEYPAD = {c: Vect(x,y) for y, line in enumerate(["789", "456", "123", "X0A"]) for x, c in enumerate(line)}
print(KEYPAD)

DIRPAD = {c: Vect(x,y) for y, line in enumerate(["X^A", "<v>"]) for x, c in enumerate(line)}
print(DIRPAD)

def signum(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def load_lines():
    file = "./1.in"
    # file = "./2.in"
    return Path(file).read_text().splitlines()


def to_arr(diff):
    arrs=[]
    for dim, d_arrs in zip(diff, ["<>", "^v"]):
        s=signum(dim)
        sym = "" if s == 0 else d_arrs[(s+1)//2]
        arrs.extend(sym*abs(dim))
    return arrs


def spath(code, keypad):
    pos = keypad["A"]
    arrs = []
    for c in code:
        arr, pos = arrs_from_pos_to_c(c, pos, keypad)
        arrs.extend(arr)
        # press A
        arrs.append("A")
        # print(arrs)
        # 1/0
    return arrs


def arrs_from_pos_to_c(c, pos, keypad):
    diff = (keypad[c] - pos)
    # print(diff)
    arr = to_arr(diff)
    # print(arr)
    return arr, keypad[c]

def sim(arrs, pos, keypad):
    output = []
    invk = {v:c for c,v in keypad.items()}
    for a in arrs:
        if a == "A":
            output.append(invk[pos])
        else:
            pos += ARR_TO_VECT[a]
    return "".join(output)


def process_line(line):
    arrs = spath(line, KEYPAD)
    arrs2 = spath(arrs, DIRPAD)
    arrs3 = spath(arrs2, DIRPAD)
    print(line)
    print("".join(arrs))
    print("".join(arrs2))
    print("".join(arrs3))
    exp3 = "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"
    assert "".join(arrs3)==exp3
    # print(exp3)
    # print(line, len(arrs3), int(line[:-1]), "".join(arrs3))
    #
    # sim_whole(arrs3)
    # print("--")
    # sim_whole(exp3)

    print(line, len(arrs3), int(line[:-1]), "".join(arrs3))
    return len(arrs3)*int(line[:-1])


def sim_whole(arrs3):
    a2 = sim(arrs3, DIRPAD["A"], DIRPAD)
    a1 = sim(a2, DIRPAD["A"], DIRPAD)
    a0 = sim(a1, KEYPAD["A"], KEYPAD)
    print(a2)
    print(a1)
    print(a0)


lines = load_lines()
s = 0
for line in lines:
    # todo
    if line == "179A":
        number = process_line(line)
        s += number

print(s)
