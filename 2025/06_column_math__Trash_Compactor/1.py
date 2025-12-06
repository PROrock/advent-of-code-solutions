import functools
import re
from pathlib import Path

from utils.grid_utils import transpose
from utils.utils import ints


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


def process_line(nums, op):
    print(nums, op)

    if op == "+":
        return functools.reduce(lambda x,y: x+y, nums)
    if op == "*":
        return functools.reduce(lambda x,y: x*y, nums)
    print("ERROR", op)
    return -1


lines = load_lines()
numbers = lines[:-1]
operators = lines[-1]
operators = list(re.findall(r"([*+])+", operators))
print(operators)

parsed = [ints(line) for line in numbers]
# print(all(len(line)==len(parsed[0]) for line in parsed))
trans = transpose(parsed)

s = 0
for nums, op in zip(trans, operators):
    number = process_line(nums, op)
    # print(number)
    s += number

print(s)
