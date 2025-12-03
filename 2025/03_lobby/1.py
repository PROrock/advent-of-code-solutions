from pathlib import Path


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


def process_line(line):
    nums = [int(i) for i in line]
    first = max(nums[:-1])
    first_i = nums.index(first)
    second = max(nums[first_i+1:])
    return first*10 + second


lines = load_lines()
s = 0
for line in lines:
    number = process_line(line)
    print(number, line)
    s += number

print(s)
