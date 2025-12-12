from pprint import pprint
import ast
from pathlib import Path

from utils.utils import ints


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


def validate(bs, cs):
    for indices, cond_sum in cs:  # (indices, sum)
        if sum([bs[bi] for bi in indices]) != cond_sum:
            return False
    return True


def solve(buttons, joltage):
    buttons = sorted(buttons, key=lambda b: len(b))
    length = len(joltage)
    max_b = [min([joltage[i] for i in b]) for b in buttons]
    print(max_b)

    buttons_with_pos = [[bi for bi, b in enumerate(buttons) if i in b] for i in range(length)]
    pprint(buttons_with_pos)

    # conditions (indices, sum)
    cs = []
    for i, button_with_pos in enumerate(buttons_with_pos):
        cs.append((button_with_pos, joltage[i]))
        sums = " + ".join([f"b{bi}*{buttons[bi]}" for bi in button_with_pos])
        print(f"{sums}={joltage[i]}")
    for i, mb in enumerate(max_b):
        print(f"b{i} <= {max_b[i]}")

    # brute force
    bs = [0 for _ in range(len(buttons))]
    bs[-1] = max_b[-1]

    while True:
        print(bs)

        if validate(bs, cs):
            print(f"found {bs}, {sum(bs)=}")
            return sum(bs)

        # next comb
        # print("next")
        # print(bs)
        # todo save this adder with carry?!
        carry = True
        for bi in reversed(range(len(buttons))):
            if carry:
                if bs[bi]+1 > max_b[bi]:
                    bs[bi] = 0
                    carry = True
                else:
                    bs[bi] += 1
                    carry = False
                    break
        if carry:
            print("no solution")
            break
        # print(bs)

    return -1

def process_line(line):
    target, buttons, joltage = parse(line)
    print(buttons, joltage)

    return solve(buttons, joltage)

def parse(line):
    target_raw, *buttons_raw, joltage_raw = line.split(" ")
    print(target_raw, buttons_raw, joltage_raw)
    target = tuple([c == "#" for c in target_raw[1:-1]])

    button_sets = [ast.literal_eval(b) for b in buttons_raw]
    button_sets = [(b,) if isinstance(b, int) else b for b in button_sets]
    # button_sets = [set(b) for b in button_sets]

    joltage = ints(joltage_raw)
    return target, button_sets, joltage


lines = load_lines()
s = 0
for line in lines:
    number = process_line(line)
    print(number, line)
    print()
    s += number

print(s)
