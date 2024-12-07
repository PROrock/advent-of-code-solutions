import re
from pathlib import Path

mul_pat = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

def load_lines():
    # file = "./1.in"
    file = "./2.in"
    # file = "./3.in"
    return Path(file).read_text().splitlines()

def process_line(line):
    result = 0
    start_idx = 0
    while start_idx != -1:
        end_idx = line.find("don't()", start_idx)
        if end_idx == -1:
            end_idx = len(line) + 10

        assert start_idx < end_idx
        subline = line[start_idx:end_idx]
        subresult = sum_muls(subline)
        # print(start_idx, end_idx, subline, subresult)
        result += subresult

        start_idx = line.find("do()", end_idx)
        assert start_idx == -1 or start_idx > end_idx
    return result

def sum_muls(line):
    ss = 0
    matches = mul_pat.finditer(line)
    # helper = " "*len(line)
    for m in matches:
        a,b = [int(i) for i in m.groups()]
        multiplication = a * b
        assert multiplication > 0
        ss += multiplication
        # helper = helper[:m.start()] + "M"*(m.end()-m.start()) + helper[m.end()+1:]

    # print(line)
    # print(helper)
    return ss


lines = load_lines()
s = 0
for line in lines:
    # number = sum_muls(line)
    number = process_line(line)
    print(number)
    s += number

print(s)
