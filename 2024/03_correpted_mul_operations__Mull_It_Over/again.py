import re
from pathlib import Path

mul_pat = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
enable_pat = re.compile(r"do\(\)")
disable_pat = re.compile(r"don't\(\)")

def load_lines():
    # file = "./1.in"
    file = "./2.in"
    # file = "./3.in"
    return Path(file).read_text().splitlines()



def process_line(line):
    enables = list(enable_pat.finditer(line))
    disables = list(disable_pat.finditer(line))
    # print(enables)
    # print(disables)

    result = 0
    start_idx = 0
    while start_idx is not None:
        # any([(first_disable:=m) for m in disables if m.start() >= start_idx])
        first_disable = next((m for m in disables if m.start() >= start_idx), None)
        end_idx = first_disable.start() if first_disable is not None else len(line) + 1
        subline = line[start_idx:end_idx]
        subresult = sum_muls(subline)
        # print
        result+=subresult

        # any([(first_enable:=m) for m in enables if m.start() > end_idx])
        first_enable = next((m for m in enables if m.start() > end_idx), None)
        start_idx = first_enable.end() if first_enable is not None else None
    return result

def sum_muls(line):
    ss = 0
    tuples = mul_pat.findall(line)
    for t in tuples:
        a,b = [int(i) for i in t]
        ss += a*b
    return ss

# print(list(mul_pat.findall("mul(1,22)do()mul(333,4)")))

lines = load_lines()
s = 0
for line in lines:
    # number = sum_muls(line)
    number = process_line(line)
    # print(number)
    s += number

print(s)

