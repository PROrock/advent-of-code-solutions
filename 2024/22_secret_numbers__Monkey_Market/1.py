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
    for i in range(N):
        next_num = compute_next(num)
        # print(i, next_num)
        num = next_num
    return num

def price(n):
    return int(str(n)[-1])

class PC(NamedTuple):
    p: int
    c: int

def get_price_and_change(line):
    num = int(line)
    ptc = []
    prev_p = price(num)
    for i in range(N):
        next_num = compute_next(num)
        # print(i, next_num)
        p = price(next_num)
        c = p-prev_p
        ptc.append(PC(p,c))

        prev_p = p
        num = next_num
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
    ptc = get_price_and_change(line)
    buyers.append(ptc)

def get_fc_to_price(pcs) -> Dict[Tuple, int]:
    fc2p = {}
    prev_last_three = [c for p,c in pcs[:3]]
    for i in range(3, len(pcs)):
        next_fc = (*prev_last_three, pcs[i].c)
        if next_fc not in fc2p:
            fc2p[next_fc]=pcs[i].p
        prev_last_three=next_fc[1:]
    return fc2p

fc2p = [get_fc_to_price(b) for b in buyers]
all_fcs = list({k for d in fc2p for k in d})
# print(f"{len(all_fcs)=}")

total_p = [sum([d.get(fc, 0) for d in fc2p]) for fc in all_fcs]
print(max(total_p))
