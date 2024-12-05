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

        subline = line[start_idx:end_idx]
        subresult = sum_muls(subline)
        print(start_idx, end_idx, subline, subresult)
        result += subresult

        start_idx = line.find("do()", end_idx)
    return result

def sum_muls(line):
    ss = 0
    tuples = mul_pat.findall(line)
    for t in tuples:
        a,b = [int(i) for i in t]
        ss += a*b
    return ss


lines = load_lines()
s = 0
for line in lines:
    # number = sum_muls(line)
    number = process_line(line)
    # print(number)
    s += number

print(s)
