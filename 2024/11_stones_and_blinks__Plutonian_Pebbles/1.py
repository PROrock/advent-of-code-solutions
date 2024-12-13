from functools import lru_cache
from pathlib import Path

# N_BLINKS = 6
# N_BLINKS = 25
N_BLINKS = 75


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

def next_nums(num):
    if num == 0:
        return [1]
    if len(s:=str(num))%2==0:
        half = len(s) // 2
        return [int(s[:half]), int(s[half:])]
    return [num*2024]

@lru_cache(maxsize=None)
def mul(num, n_blinks):
    if n_blinks == 0:
        return 1

    l = 0
    nums = next_nums(num)
    for n in nums:
        l += mul(n, n_blinks-1)
    return l

def process_line(line):
    l=0
    nums = [int(i) for i in line.split()]
    for n in nums:
        l += mul(n, N_BLINKS)
    return l

lines = load_lines()
s = 0
for line in lines:
    number = process_line(line)
    s += number
print(s)
