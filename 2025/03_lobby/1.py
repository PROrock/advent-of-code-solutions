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

N_BATTERIES = 12
def process_line_part2(line):
    nums = [int(i) for i in line]

    voltage = []
    for i in range(N_BATTERIES):
        digit = max(nums[:len(nums)-N_BATTERIES+i+1])
        digit_i = nums.index(digit)
        nums = nums[digit_i+1:]
        voltage.append(digit)
        # print(line, i, digit, digit_i, nums)
    return int("".join(map(str, voltage)))


lines = load_lines()
s = 0
for line in lines:
    # number = process_line(line)
    number = process_line_part2(line)
    # print(number, line)
    s += number

print(s)
