from pathlib import Path
from time import sleep
from typing import NamedTuple, Tuple, Dict, List

from utils.utils import ints

# N = 10
# N = 9
N = 2000

def load_lines():
    # file = "./123.in"
    # file = "./1.in"
    # file = "./1.b.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


def mp(val, num):
    return (val ^ num)%16777216

def compute_next(num):
    num = mp(num << 6, num)
    num = mp(num >> 5, num)
    num = mp(num << 11, num)
    return num


def process_line_a(line):
    num = int(line)
    # print(num)
    # l=[num]
    for i in range(N):
        next_num = compute_next(num)
        # print(i, next_num)
        # l.append(next_num)
        num = next_num
    # print("l", len(l), len(set(l)))
    return num


def price(n):
    return int(str(n)[-1])

class PC(NamedTuple):
    p: int
    c: int

def process_line_b(line):
    num = int(line)
    # print(num)
    # l=[num]
    ptc = []
    prev_p = price(num)
    for i in range(N):
        next_num = compute_next(num)
        # print(i, next_num)
        # l.append(next_num)
        p = price(next_num)
        c = p-prev_p
        ptc.append(PC(p,c))

        prev_p = p
        num = next_num
    # print("l", len(l), len(set(l)))
    # print(ptc)
    return ptc

#A
# lines = load_lines()
# s = 0
# for line in lines:
#     number = process_line_a(line)
#     s += number
# print(s)

lines = load_lines()
buyers = []
for line in lines:
    ptc = process_line_b(line)
    # print(len(ptc))
    buyers.append(ptc)

# for b in buyers:
#     print(b)
# print(buyers)

# def get_d_ugly(pcs) -> Dict[Tuple, int]:
#     d = {}
#     fc = tuple([c for p,c in pcs[:4]])
#     d[fc] = pcs[3].p
#     # what is faster?
#     # next_fc = fc[1:]+[pcs[5].c]
#     # next_fc = [*fc[1:],pcs[5].c]
#     # assert next_fc==fc[1:]+[pcs[5].c]
#     # print(next_fc)
#     for i in range(4, len(pcs)):
#         next_fc = (*fc[1:], pcs[i].c)
#         if next_fc not in d:
#             d[next_fc]=pcs[i].p
#         fc = next_fc
#     print(d)
#     return d


def get_d(pcs) -> Dict[Tuple, int]:
    # fcs = []
    d = {}
    prev_last_three = [c for p,c in pcs[:3]]
    for i in range(3, len(pcs)):
        next_fc = (*prev_last_three, pcs[i].c)
        # fcs.append(next_fc)
        if next_fc not in d:
            d[next_fc]=pcs[i].p
        prev_last_three=next_fc[1:]
    # print(fcs)
    return d

def get_fcs(pcs) -> List[Tuple[Tuple, int]]:
    fcs = []
    prev_last_three = [c for p,c in pcs[:3]]
    for i in range(3, len(pcs)):
        next_fc = (*prev_last_three, pcs[i].c)
        fcs.append((next_fc,pcs[i].p))
        prev_last_three=next_fc[1:]
    # print(fcs)
    return fcs

# debug
# print(get_d(buyers[0]))
# fcs = get_fcs(buyers[0])
# print("fcs")
# print(fcs)

# all_fc_seqs = [get_fcs(buyer) for buyer in buyers]
# for i in range(len(buyers)):
#     fcs = get_fcs(buyers[i])
#     Path(f"seq_{i}.txt").write_text("\n".join([str(t) for t in fcs]))

ds = [get_d(b) for b in buyers]
# ds = []
# for b in buyers:
#     d = get_d(b)
# print(ds)
all_fcs = list({k for d in ds for k in d})
print(f"{len(all_fcs)=}")

total_p = [sum([d.get(fc, 0) for d in ds]) for fc in all_fcs]

# for fc in all_fcs:
#     print(fc, sum([d.get(fc, 0) for d in ds]), [d.get(fc, 0) for d in ds])
# print("DEBUG")

# print(total_p)
# argmax_idx = max(enumerate(total_p), key=lambda t:t[1])[0]
# print(all_fcs[argmax_idx])
# print(total_p[argmax_idx])

print(max(total_p))

# wfc = (-9, 9, -1, 0)
# fc = (-9, 9, -1, 0)
# fc = (-2,1,-1,3)
# print(sum([d.get(fc, 0) for d in ds]))
# print([d.get(fc, 0) for d in ds])

