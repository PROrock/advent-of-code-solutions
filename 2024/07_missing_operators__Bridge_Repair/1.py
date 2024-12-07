from pathlib import Path


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

OPS=[False, True]
OPS_B=["+", "*", "||"]

def can(so_far, numbers, test_val):
    if len(numbers) == 0:
        return so_far == test_val

    n = numbers[0]
    for op in OPS_B:
        if can(do_op(so_far, n, op), numbers[1:], test_val):
            return True
    return False

def can_b(so_far, numbers, test_val):
    if len(numbers) == 0:
        return so_far == test_val
    if so_far >= test_val:  # slight speed optimisation, not necessarily needed for the star
        return False

    n = numbers[0]
    for op in OPS_B:
        subresult = can_b(do_op_b(so_far, n, op), numbers[1:], test_val)
        if subresult:
            return True
    return False


def can_add_operators(test_val, numbers):
    # return can(numbers[0], numbers[1:], test_val)
    return can_b(numbers[0], numbers[1:], test_val)

def process_line(line):
    test_val, rest = line.split(": ")
    test_val = int(test_val)
    numbers = [int(i) for i in rest.split()]

    if can_add_operators(test_val, numbers):
        return test_val
    return 0

def do_op(a, b, is_mult):
    return a*b if is_mult else a+b
def do_op_b(a, b, op):
    if op == "+": return a+b
    if op == "*": return a*b
    else: return int(str(a)+str(b))

lines = load_lines()
s = 0
for line in lines:
    number = process_line(line)
    s += number
print(s)
