import itertools
from functools import lru_cache
from pathlib import Path
from typing import Any, List
from dataclasses import dataclass
from utils.grid_utils import DIRS_CLOCKWISE, DIR_TO_VECT, elem_at_pos, find_one_in_grid, inbounds, PrioritizedItem, \
    Vect, load_grid_str, ARR_TO_VECT

KEYPAD = {c: Vect(x,y) for y, line in enumerate(["789", "456", "123", "X0A"]) for x, c in enumerate(line)}
# print(KEYPAD)
DIRPAD = {c: Vect(x,y) for y, line in enumerate(["X^A", "<v>"]) for x, c in enumerate(line)}
# print(DIRPAD)

# todo
# N_ROBOTS = 0
# N_ROBOTS = 2
N_ROBOTS = 5
# N_ROBOTS = 10
# N_ROBOTS = 15
# N_ROBOTS = 25

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


def to_arrx(diff, pos, keypad, c):
    arrs=[]
    for dim, d_arrs in zip(diff, ["<>", "^v"]):
        s = signum(dim)
        sym = "" if s == 0 else d_arrs[(s+1)//2]
        arrs.append(sym*abs(dim))
    if pos.y == keypad["X"].y:  # if you in the gap row, change/move y first, x 2nd
        arrs = arrs[::-1]
    return list(itertools.chain.from_iterable(arrs))

def to_arr_y(diff, pos, keypad, c):
    arrs=[]
    for dim, d_arrs in zip(diff, ["<>", "^v"]):
        s = signum(dim)
        sym = "" if s == 0 else d_arrs[(s+1)//2]
        arrs.append(sym*abs(dim))
    arrs = arrs[::-1] # y first
    if pos.x == keypad["X"].x or "<" in arrs[1]:                             # works on big (n==2)
    # if pos.x == keypad["X"].x or ("<" in arrs[1] and pos.y != keypad["X"].y):  # works on small
    # if pos.x == keypad["X"].x or ("<" in arrs[1] and keypad[c].x!=keypad["X"].x):
        arrs = arrs[::-1] # x first
    return list(itertools.chain.from_iterable(arrs))

def to_arr(diff, pos, keypad, c):
    arrs=[]
    for dim, d_arrs in zip(diff, ["<>", "^v"]):
        s = signum(dim)
        sym = "" if s == 0 else d_arrs[(s+1)//2]
        arrs.append(sym*abs(dim))
    # prefer x first
    # if ">" in arrs[0] and
    # target_pos = keypad[c]
    if (pos.y == keypad["X"].y and keypad[c].x == keypad["X"].x) or (
            ">" in arrs[0] and pos.x != keypad["X"].x):
        arrs = arrs[::-1]  # y first
    return list(itertools.chain.from_iterable(arrs))


@lru_cache(maxsize=None)
def spath(code, is_dirpad):
    print("cache miss", code)
    keypad = DIRPAD if is_dirpad else KEYPAD
    pos = keypad["A"]
    arrs = []
    for c in code:
        arr, pos = arrs_from_pos_to_c(pos, c, keypad)
        arrs.extend(arr)
        arrs.append("A")  # press the button labeled c
        # print(arrs)
    return "".join(arrs)

def spath_dir(code):
    arrs = []
    segments = code.split("A")[:-1]
    # print(segments)
    segments = [s+"A" for s in segments]
    # print("code", code)
    # print(segments)

    for s in segments:
        arrs.extend(spath(s, is_dirpad=True))
    return "".join(arrs)
def spath_dirAA_WIP(code):
    arrs = []
    segments = code.split("AA")
    print("code", code)
    print(segments)
    segments = [s+"AA" for s in segments]
    print(segments)

    for s in segments:
        arrs.extend(spath(s, is_dirpad=True))
    return "".join(arrs)

@lru_cache(maxsize=None)
def spath_dir_rec_bad(code, n):
    if n == 0:
        print(n, code)
        return code
    # if n>=20:
    #     print(n, code)

    arrs = []
    segments = code.split("A")[:-1]
    # print(segments)
    segments = [s+"A" for s in segments]
    # print("code", code)
    # print(segments)
    # print(n, N_ROBOTS-n, "code", code, segments)

    if n>=20:
        print(n, code, segments)

    for s in segments:
        # arrs.extend(spath(s, is_dirpad=True))
        next_level_code = spath(s, is_dirpad=True)
        # next_level_code = spath_dir(s)  # doesnt make sense, already splitted into segments!
        arrs.extend(spath_dir_rec_bad(next_level_code, n-1))
    return "".join(arrs)

@lru_cache(maxsize=None)
def spath_dir_rec(code, n):
    if n == 0:
        print(n, code)
        return code
    # if n>=20:
    #     print(n, code)

    arrs = []
    segments = code.split("A")[:-1]
    # print(segments)
    segments = [s+"A" for s in segments]
    # print("code", code)
    # print(segments)
    # print(n, N_ROBOTS-n, "code", code, segments)

    if n>=20:
        print(n, code, segments)

    for s in segments:
        # arrs.extend(spath(s, is_dirpad=True))
        next_level_code = spath(s, is_dirpad=True)
        # next_level_code = spath_dir(s)  # doesnt make sense, already split into segments!
        arrs.extend(spath_dir_rec(next_level_code, n-1))
    return "".join(arrs)


def arrs_from_pos_to_c(pos, c, keypad):
    diff = (keypad[c] - pos)
    arr = to_arr(diff, pos, keypad, c)
    return arr, keypad[c]

def process_line_a(line):
    arrs = spath(line, is_dirpad=False)
    arrs2 = spath(arrs, is_dirpad=True)
    arrs3 = spath(arrs2, is_dirpad=True)
    # print(line)
    # print("".join(arrs))
    # print("".join(arrs2))
    # print("".join(arrs3))
    # exp = "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"  #3 179A
    # exp = "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"  # 5 379A
    # # # print(exp)
    # # # print(line, len(arrs3), int(line[:-1]), "".join(arrs3))
    pprint(sim_whole("".join(arrs3)))
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

def process_line_b(line):
    arrs = spath(line, is_dirpad=False)
    levels=[arrs]
    for i in range(N_ROBOTS):
        # arrs1 = spath(arrs, is_dirpad=True)
        arrs2 = spath_dir(arrs)

        # print(arrs1)
        # print(arrs2)
        # assert arrs1==arrs2
        # arrs=arrs1  #226406498
        arrs=arrs2   #226406498
        levels.append(arrs)
        print(i+1, len(arrs))

    # for i in range(N_ROBOTS):
    #     # arrs1 = spath(arrs, is_dirpad=True)
    #     arrs2 = spath_dir(arrs)
    #
    #     # print(arrs1)
    #     # print(arrs2)
    #     # assert arrs1==arrs2
    #     # arrs=arrs1  #226406498
    #     arrs=arrs2   #226406498
    #     levels.append(arrs)
    #     print(i+1, len(arrs))

    pprint3(levels[::-1])
    pprint(levels[::-1])
    print(line, len(arrs), int(line[:-1]), arrs)
    return len(arrs)*int(line[:-1])

def process_line_b_new(line):
    arrs = spath(line, is_dirpad=False)
    # levels=[arrs]

    segments = arrs.split("A")[:-1]
    # print(segments)
    segments = [s+"A" for s in segments]
    arrs = []
    for s in segments:
        arrs.extend(spath_dir_rec(s, N_ROBOTS))

    # for i in range(N_ROBOTS):
    #     # arrs1 = spath(arrs, is_dirpad=True)
    #     arrs2 = spath_dir(arrs)
    #
    #     # print(arrs1)
    #     # print(arrs2)
    #     # assert arrs1==arrs2
    #     # arrs=arrs1  #226406498
    #     arrs=arrs2   #226406498
    #     levels.append(arrs)
    #     print(i+1, len(arrs))

    # pprint3(levels[::-1])
    # pprint(levels[::-1])
    arrs = "".join(arrs)

    pprint(sim_whole(arrs))
    # pprint(sim_whole("<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"))
    print(line, len(arrs), int(line[:-1]), arrs)
    return len(arrs)*int(line[:-1])


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
    prev_line = fas[0]
    print(prev_line)
    for i, line in enumerate(fas[1:]):
        output = []
        c_in_line_idx = 0

        for c in prev_line:
            if c =="A":
                # print(c, c_in_line_idx, line, prev_line)
                output.append(line[c_in_line_idx])
                c_in_line_idx += 1
            else:
                output.append(" ")
        prev_line = "".join(output)
        print(prev_line)
def pprint3(fas):
    for line in fas:
        print(line)


# process_line_a("085A")
# process_line_a("379A")
# process_line_b("179A")
# for d in ["283A"]:
#     process_line_a(d)
#     process_line_b(d)
# 1/0

lines = load_lines()
s = 0
for line in lines:
    # number = process_line_a(line)
    number = process_line_b(line)
    # 1/0
    s += number

print(s)

# v<A<AA>>^AvAA<^A>Av<<A>>^AAAvA^Av<A<A>>^AvA<^A>Av<A>^Av<<A>>^AAvA<^A>A
#   v <<A>>^A<AAA>Av<A>^AvA<AA>^A
#       <   A^^^AvA>vvA
#           085A
