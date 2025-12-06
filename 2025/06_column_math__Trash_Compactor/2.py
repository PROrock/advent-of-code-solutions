import functools
import re
from pathlib import Path

from utils.grid_utils import transpose
from utils.utils import split_iterable_by_sep_v2


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


def process_line(nums, op):
    print(nums, op)

    if op == "+":
        return functools.reduce(lambda x,y: x+y, nums)
        # internet says, you can just use sum(nums)
    if op == "*":
        return functools.reduce(lambda x,y: x*y, nums)
        # internet says u can use operator.mul()
    print("ERROR", op)
    return -1


lines = load_lines()
numbers = lines[:-1]
operators = lines[-1]
operators = list(re.findall(r"([*+])+", operators))
# print(operators)

print(numbers)
# pad
max_len = max([len(line) for line in numbers])
print(max_len)
numbers = [line + " "*(max_len-len(line)) for line in numbers]
# print(numbers)

trans = transpose(numbers)
trans = ["".join(t) for t in trans]
# print(trans)

# reverse
rev = trans[::-1]
# print(rev)
operators = operators[::-1]

#split!
print(len(numbers))
split = list(split_iterable_by_sep_v2(rev, " "*len(numbers)))
print("split", split)

parsed = [[int(line) for line in group] for group in split]
print(parsed)

print()
s = 0
for nums, op in zip(parsed, operators):
    number = process_line(nums, op)
    # print(number, nums, op)
    s += number

print(s)
