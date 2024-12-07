import re
from pathlib import Path

mul_pat = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

def load_lines():
    # file = "./1.in"
    file = "./2.in"
    # file = "./3.in"
    # file = "./4.in"
    # file = "./5.in"
    return Path(file).read_text().splitlines()

def process_line(line):
    result = 0
    start_idx = 0
    segments=[]
    matches_pos = []
    while start_idx != -1:
        end_idx = line.find("don't()", start_idx)
        if end_idx == -1:
            end_idx = len(line)

        assert start_idx < end_idx
        subline = line[start_idx:end_idx]
        subresult, matches = sum_muls(subline)
        matches_pos.extend([(start_idx+m.start(), start_idx+m.end()) for m in matches])
        # print(start_idx, end_idx, subline, subresult)
        result += subresult
        # print(start_idx, end_idx, subresult, result)
        segments.append(subline)

        start_idx = line.find("do()", end_idx)
        #debug
        fixed_start_idx = len(line) if start_idx == -1 else start_idx
        disabled_part = line[end_idx:fixed_start_idx]
        # print("disabled:", disabled_part)
        segments.append(disabled_part)

        assert start_idx == -1 or start_idx > end_idx

    #debug
    assert "".join(segments) == line
    print(line)
    print("".join(("E" if i%2==0 else "D")*len(s) for i, s in enumerate(segments)))
    helper = " "*len(line)
    for m in matches_pos:
        # helper = helper[:m.start()] + "M"*(m.end()-m.start()) + helper[m.end():]
        helper = helper[:m[0]] + "M"*(m[1]-m[0]) + helper[m[1]:]
    print(helper)

    return result

def sum_muls(line2):
    ss = 0
    matches = list(mul_pat.finditer(line2))
    # helper = " "*len(line)
    for m in matches:
        a,b = [int(i) for i in m.groups()]
        multiplication = a * b
        # assert multiplication > 0
        ss += multiplication
        # print(ss, multiplication, m)
        # helper = helper[:m.start()] + "M"*(m.end()-m.start()) + helper[m.end()+1:]

    # print(line)
    # print(helper)
    return ss, matches


lines = load_lines()
s = 0
for line in lines:
    # number = sum_muls(line)
    number = process_line(line)
    s += number
    # print(number, s)

print(s)
