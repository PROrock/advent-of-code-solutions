import itertools
from functools import lru_cache
from pathlib import Path
from time import perf_counter
from typing import NamedTuple

# from utils.grid_utils import Vect, ARR_TO_VECT


class Vect(NamedTuple):
    x: int
    y: int

    def invert(self):
        return Vect(-self.x, -self.y)

    def __add__(self, other):
        return Vect(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vect(self.x - other.x, self.y - other.y)

    def __mul__(self, multiplier):
        return Vect(self.x * multiplier, self.y * multiplier)

    def l1_dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

ARR_TO_VECT = {
    "^": Vect(0, -1),
    ">": Vect(1, 0),
    "v": Vect(0, 1),
    "<": Vect(-1, 0),
}
KEYPAD = {c: Vect(x,y) for y, line in enumerate(["789", "456", "123", "X0A"]) for x, c in enumerate(line)}
DIRPAD = {c: Vect(x,y) for y, line in enumerate(["X^A", "<v>"]) for x, c in enumerate(line)}

# ideas:
# line by line again? probably not - rly slow
# somehow compute directly?
# somehow skip more lines in 1 go? 5? dict for that?
# somehow dynamic programming?

DENUM = 5

# todo
# N_ROBOTS = 2
# N_ROBOTS = 5
# N_ROBOTS = 10
# N_ROBOTS = 15
# N_ROBOTS = 17
# N_ROBOTS = 18  # 15-19,5s w/o cleanup, (15s w/o, 1m19s w/)
N_ROBOTS = 20  # 5x5, 73s with 4As (and rly no extend), 75s with rly no extend, 90s with no extend , 245s with extend!
# N_ROBOTS = 25

# 5: 2747526
#10: 261627290
#15: 24923343972
#17: 154231715988
#18: 383670273596
#20: 2374260460314  # took many mins (18,5 mins w. cleanup) and 60GBs of memory
#day 11: 75 blinks:
#D11:237994815702032

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
    # target_pos = keypad[c]
    if (pos.y == keypad["X"].y and keypad[c].x == keypad["X"].x) or (
            ">" in arrs[0] and pos.x != keypad["X"].x):
        arrs = arrs[::-1]  # y first
    return list(itertools.chain.from_iterable(arrs))


@lru_cache(maxsize=None)
def spath(code, is_dirpad):
    # print("cache miss", code)
    keypad = DIRPAD if is_dirpad else KEYPAD
    pos = keypad["A"]
    arrs = []
    for c in code:
        arr, pos = arrs_from_pos_to_c(pos, c, keypad)
        arrs.extend(arr)
        arrs.append("A")  # press the button labeled c
        # print(arrs)
    # return "".join(arrs)
    # return arrs
    return tuple(arrs)

def spath_dir(code):
    arrs = []
    # segments = code.split("A")[:-1]
    # segments = [s+"A" for s in segments]
    segments = arr_split(code, "A")
    # print("code", code)
    # print(segments)

    for s in segments:
        arrs.extend(spath(s, is_dirpad=True))
    return tuple(arrs)
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

# slightly faster (but maybe because of cleanup?)
def arr_split_orig(arr, sep):
    prev_i = 0
    for i,c in enumerate(arr):
        if c==sep:
            yield arr[prev_i:i+1]
            prev_i = i+1

    # yield arr[prev_i:i+1]  # commented, so I don't have to forget last yield (because A is always the last letter)

def arr_split2(arr, sep):
    prev_i = 0
    aas = False
    for i,c in enumerate(arr):
        if c!=sep and aas:
            yield arr[prev_i:i]
            prev_i = i
            aas = False
        if c==sep:
            aas = True
    yield arr[prev_i:i+1]

def arr_split_mult_sep(arr, sep, n_times):
    prev_i = 0
    t = 0
    for i,c in enumerate(arr):
        if c==sep:
            if t == n_times-1:
                yield arr[prev_i:i+1]
                prev_i = i+1
                t=0
            else:
                t+=1
    if len(arr[prev_i:i+1])>0:
        yield arr[prev_i:i+1]
def arr_split(arr, sep):
    # return arr_split_orig(arr, sep)
    # return arr_split2(arr, sep)
    return arr_split_mult_sep(arr, sep, 4)


# todo revert?
@lru_cache(maxsize=None)
def spath_dir_rec(code, n):
    if n == 0:
        # print(n, code)
        return code
    # if n>=20:
    # if n>=N_ROBOTS-2:
    # if n>=15:
    #     print(n, code)

    segments = arr_split(code, "A")
    # segments = code.split("A")[:-1]
    # segments = [s+"A" for s in segments]
    # print("code", code)
    # print(segments)
    # print(n, N_ROBOTS-n, "code", code, segments)

    # if n>=N_ROBOTS-1:
    #     print(n, code, segments)

    # 3s user 3,3 total
    arrs = []
    for s in segments:
        next_level_code = spath(s, is_dirpad=True)  # spath_dir(s) doesnt make sense, already split into segments!
        # arrs.extend(spath_dir_rec(next_level_code, n-1))
        arrs.append(spath_dir_rec(next_level_code, n-1))
    arrs = list(itertools.chain.from_iterable(arrs))

    # 13s user 14,3 total
    # whole_next_code = []
    # for s in segments:
    #     next_level_code = spath(s, is_dirpad=True)  # spath_dir(s) doesnt make sense, already split into segments!
    #     whole_next_code.append(next_level_code)
    # arrs = spath_dir_rec("".join(whole_next_code), n-1)
    # return "".join(arrs)
    return arrs

def spath_dir_5(code):
    if code in d5:
        return d5[code]

    # print("mapping miss", "".join(code))
    sp = spath_dir_rec(code, DENUM)
    # print("mapping miss END")  # it's not the DENUM levels of spath, it's the overhead, the merging and splitting!
    d5[code] = sp
    return sp

def spath_dir_mapping(code, n):
    if code in mapping:
        return mapping[code]

    sp = spath_dir_rec(code, n)
    mapping[code] = sp
    return sp

def arrs_from_pos_to_c(pos, c, keypad):
    diff = (keypad[c] - pos)
    arr = to_arr(diff, pos, keypad, c)
    return arr, keypad[c]

def process_line_a(line):
    arrs = spath(line, is_dirpad=False)
    arrs2 = spath(arrs, is_dirpad=True)
    arrs3 = spath(arrs2, is_dirpad=True)
    pprint(sim_whole("".join(arrs3)))
    print(line, len(arrs3), int(line[:-1]), "".join(arrs3))
    return len(arrs3)*int(line[:-1])

def process_line_b_by_lines(line):
    arrs = spath(line, is_dirpad=False)
    # levels=[arrs]
    for i in range(N_ROBOTS):
        # arrs1 = spath(arrs, is_dirpad=True)
        arrs2 = spath_dir(arrs)
        arrs=arrs2
        # levels.append(arrs)
        # print(i+1, len(arrs), "prev", len(levels[i]), "ratio", len(arrs)/len(levels[i]))  # ratio is around 2.5

    # pprint3(levels[::-1])
    # print("-")
    # pprint(levels[::-1])
    # print(line, len(arrs), int(line[:-1]), arrs)
    return len(arrs)*int(line[:-1])

def process_line_b_rec(line):
    arrs = spath(line, is_dirpad=False)
    # levels=[arrs]

    segments = arr_split(arrs, "A")
    # segments = arrs.split("A")[:-1]
    # # print(segments)
    # segments = [s+"A" for s in segments]
    arrs = []
    for s in segments:
        arrs.extend(spath_dir_rec(s, N_ROBOTS))

    # pprint(levels[::-1])
    # arrs = "".join(arrs)
    # pprint(sim_whole(arrs))
    # print(line, len(arrs), int(line[:-1]), arrs)
    return len(arrs)*int(line[:-1])

def process_line_b_rec_5(line):
    arrs = spath(line, is_dirpad=False)

    for epoch in range(N_ROBOTS//DENUM):
        print(epoch, len(arrs))

        segments = arr_split(arrs, "A")
# todo back
#         segments = list(arr_split(arrs, "A"))
#         print(segments)

        # arrs = []
        # for s in segments:
        #     arrs.extend(spath_dir_5(s))
        # arrs = tuple(arrs)
        arrs = []
        for s in segments:
            arrs.append(spath_dir_5(s))
        arrs = tuple(itertools.chain.from_iterable(arrs))

    return len(arrs)*int(line[:-1])

def process_line_b_rec_mapping(line):
    arrs = spath(line, is_dirpad=False)

    segments = arr_split(arrs, "A")
    arrs = []
    for s in segments:
        arrs.extend(spath_dir(s))
    arrs = tuple(arrs)

    denum = 8
    for epoch in range(N_ROBOTS//denum):
        print(epoch, len(arrs))

        segments = arr_split(arrs, "A")
        arrs = []
        for s in segments:
            # arrs.extend(spath_dir_mapping(s, denum))
            arrs.append(spath_dir_mapping(s, denum))
        arrs = tuple(itertools.chain.from_iterable(arrs))
        # arrs = tuple(arrs)

    return len(arrs)*int(line[:-1])
def process_line_b(line):
    # return process_line_b_by_lines(line)
    # return process_line_b_rec(line)
    return process_line_b_rec_5(line)
    # return process_line_b_rec_mapping(line)

def sim_whole(arrs3):
    a2 = sim(arrs3, DIRPAD["A"], DIRPAD)
    a1 = sim(a2, DIRPAD["A"], DIRPAD)
    a0 = sim(a1, KEYPAD["A"], KEYPAD)
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


# process_line_a("179A")
# process_line_b("179A")
# for d in ["283A"]:
#     process_line_a(d)
#     process_line_b(d)
# 1/0

start = perf_counter()
d5 = {}
mapping = {}
lines = load_lines()
s = 0
for line in lines:
    print(line)
    # number = process_line_a(line)
    number = process_line_b(line)
    # 1/0
    s += number

print(s)
end = perf_counter()
print(end-start, "s")
print((end-start)/60, "mins")
