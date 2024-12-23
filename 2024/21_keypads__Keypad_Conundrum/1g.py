import itertools
from pathlib import Path
from typing import Any, List
from dataclasses import dataclass
from utils.grid_utils import DIRS_CLOCKWISE, DIR_TO_VECT, elem_at_pos, find_one_in_grid, inbounds, PrioritizedItem, \
    Vect, load_grid_str, ARR_TO_VECT

KEYPAD = {c: Vect(x,y) for y, line in enumerate(["789", "456", "123", "X0A"]) for x, c in enumerate(line)}
# print(KEYPAD)
DIRPAD = {c: Vect(x,y) for y, line in enumerate(["X^A", "<v>"]) for x, c in enumerate(line)}
# print(DIRPAD)

def signum(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


def to_arrx(diff, pos, keypad):
    arrs=[]
    for dim, d_arrs in zip(diff, ["<>", "^v"]):
        s = signum(dim)
        sym = "" if s == 0 else d_arrs[(s+1)//2]
        arrs.append(sym*abs(dim))
    if pos.y == keypad["X"].y:  # if you in the gap row, change/move y first, x 2nd
        arrs = arrs[::-1]
    return list(itertools.chain.from_iterable(arrs))

def to_arr(diff, pos, keypad):
    arrs=[]
    for dim, d_arrs in zip(diff, ["<>", "^v"]):
        s = signum(dim)
        sym = "" if s == 0 else d_arrs[(s+1)//2]
        arrs.append(sym*abs(dim))
    arrs = arrs[::-1] # y first
    if pos.x == keypad["X"].x or "<" in arrs[1]:
        arrs = arrs[::-1] # x first
    return list(itertools.chain.from_iterable(arrs))


def spath(code, keypad):
    pos = keypad["A"]
    arrs = []
    for c in code:
        arr, pos = arrs_from_pos_to_c(pos, c, keypad)
        arrs.extend(arr)
        arrs.append("A")  # press the button labeled c
        # print(arrs)
    return arrs

def arrs_from_pos_to_c(pos, c, keypad):
    diff = (keypad[c] - pos)
    arr = to_arr(diff, pos, keypad)
    return arr, keypad[c]

def process_line(line):
    arrs = spath(line, KEYPAD)
    arrs2 = spath(arrs, DIRPAD)
    arrs3 = spath(arrs2, DIRPAD)
    # print(line)
    # print("".join(arrs))
    # print("".join(arrs2))
    # print("".join(arrs3))
    # exp = "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"  #3 179A
    # exp = "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"  # 5 379A
    # # # print(exp)
    # # # print(line, len(arrs3), int(line[:-1]), "".join(arrs3))
    # pprint(sim_whole("".join(arrs3)))
    # print("--")
    # pprint(sim_whole(exp))
    # pprint3(sim_whole("".join(arrs3)))
    # print("--")
    # pprint3(sim_whole(exp))

    #
    # assert "".join(arrs3)==exp
    #
    print(line, len(arrs3), int(line[:-1]), "".join(arrs3))
    return len(arrs3)*int(line[:-1])


def sim_whole(arrs3):
    # print(arrs3)
    a2 = sim(arrs3, DIRPAD["A"], DIRPAD)
    a1 = sim(a2, DIRPAD["A"], DIRPAD)
    a0 = sim(a1, KEYPAD["A"], KEYPAD)
    # print(a2)
    # print(a1)
    # print(a0)
    return [arrs3, a2, a1, a0]
def sim(arrs, pos, keypad):
    output = []
    invk = {v:c for c,v in keypad.items()}
    for a in arrs:
        if a == "A":
            output.append(invk[pos])
        else:
            pos += ARR_TO_VECT[a]
    return "".join(output)
def pprint(fas):
    for i, line in enumerate(fas):
        if i == 0:
            print(line)
            prev_line = line
            continue
        # prev_line=fas[i-1]
        output = []
        line_idx = 0
        for c in prev_line:
            if c =="A":
                output.append(line[line_idx])
                line_idx += 1
            else:
                output.append(" ")
        prev_line = "".join(output)
        print(prev_line)
def pprint3(fas):
    for line in fas:
        print(line)


# process_line("085A")
# process_line("379A")
# 1/0

lines = load_lines()
s = 0
for line in lines:
    number = process_line(line)
    s += number

print(s)
# 182844
# 188752 too high
# 192644 is higher, if we go y first, so maybe the order rly matter!


# v<A<AA>>^AvAA<^A>Av<<A>>^AAAvA^Av<A<A>>^AvA<^A>Av<A>^Av<<A>>^AAvA<^A>A
#   v <<A>>^A<AAA>Av<A>^AvA<AA>^A
#       <   A^^^AvA>vvA
#           085A
