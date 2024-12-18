import re
from pathlib import Path

mul_pat = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
do_pat = re.compile(r"do\(\)")
dont_pat = re.compile(r"don't\(\)")


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    # file = "./3.in"
    # file = "./4.in"
    return Path(file).read_text().splitlines()


def process_line_1(line):
    matches = mul_pat.findall(line)
    result = 0
    for m in matches:
        # print(m)
        a,b = [int(i) for i in m]
        op_result = a * b
        result+=op_result
    return result

def process_line_2(line):
    result = 0
    # maybe already sorted?
    do_m = list(sorted(do_pat.finditer(line), key=lambda m: m.start()))
    dont_m = list(sorted(dont_pat.finditer(line), key=lambda m: m.start()))
    # print(do_m)
    # print(dont_m)
    # both = list(sorted(do_m+dont_m, key=lambda m: m.start()))
    # print(both)
    # for m in both:
    #     print(m[0])

    # find start idx
    # find end idx
    # find all muls between start and end

    start_idx = 0
    while start_idx is not None:
        # find end idx
        dont_m = [m for m in dont_m if m.start() >= start_idx]
        end_idx = dont_m[0].start() if len(dont_m) else (len(line)+1)

        subline = line[start_idx:end_idx]
        subresult = process_line_1(subline)
        print(start_idx, end_idx, "subline", subline, subresult)
        result += subresult

        do_m = [m for m in do_m if m.start() > end_idx]
        start_idx = do_m[0].start() if len(do_m) else None
    return result

assert process_line_2("mul(2,10)") == 20
assert process_line_2("do()mul(2,10)") == 20
assert process_line_2("don't()do()mul(2,10)") == 20
assert process_line_2("don't()mul(2,10)") == 0
assert process_line_2("don't()don't()mul(2,10)") == 0
assert process_line_2("do()don't()mul(2,10)") == 0
assert process_line_2("do()don't()mul(2,10)don't()mul(3,10)") == 0
assert process_line_2("do()nul(2,10)") == 0
assert process_line_2("do()mul(2,10") == 0
assert process_line_2("do()mul(2.10)") == 0
assert process_line_2("do()mul(210)") == 0
assert process_line_2("do()mul2,10)") == 0

assert process_line_2("mul(2,10)don't()mul(3,10)") == 20
assert process_line_2("mul(2,10)don't()mul(3,10)do()") == 20
assert process_line_2("mul(2,10)mul(3,10)") == 50
assert process_line_2("mul(2,10)do()mul(3,10)") == 50
assert process_line_2("mul(2,10)do()mul(3,10)don't()") == 50
assert process_line_2("mul(2,10)do()mul(3,10)do()") == 50
assert process_line_2("mul(2,10)do()don't()do()mul(3,10)do()") == 50
assert process_line_2("mul(2,10)do()don't()mul(5,100)do()mul(3,10)do()") == 50

assert process_line_2("mul(2,10)do()mul(3,10)don't()mul(4,10)") == 50
assert process_line_2("mul(2,10)do()mul(3,10)do()mul(4,10)") == 90
assert process_line_2("mul(2,10)do()mul(3,10)!@#$%^&*()_+mul(4,10)") == 90
assert process_line_2("mul(2,10)do()don't()do()mul(3,10)do()mul(4,10)") == 90
assert process_line_2("don't()mul(5,100)do()mul(2,10)do()do()mul(3,10)do()mul(4,10)") == 90
assert process_line_2("don't()mul(5,100)do()mul(2,10)do()don't()mul(5,100)do()mul(3,10)do()mul(4,10)") == 90
assert process_line_2("don't()mul(5,100)do()mul(2,10)do()don't()mul(5,100)do()mul(3,10)don't()mul(5,100)do()mul(4,10)") == 90
assert process_line_2("don't()mul(5,100)do()mul(2,10)do()don't()mul(5,100)do()mul(3,10)don't()!@#$%^&*()___+}{|:?><mul(5,100)@#$%^&*()_+do()mul(4,10)") == 90
assert process_line_2("mul(2,10)do()don't()mul(5,100)do()mul(3,10)do()mul(4,10)") == 90
assert process_line_2("mul(2,10)do()don't()mul(5,100)do()do()mul(3,10)do()mul(4,10)") == 90
assert process_line_2("mul(2,10)do()don't()mul(5,100)do()do()mul(3,10)do()mul(4,10)") == 90
assert process_line_2("do()+mul(232,260)who(),who()[)+what()#[mul(972,455)mul(299,267)#}}+%% }@") == 582413
print("asserts")
print()

lines = load_lines()
s = 0
for line in lines:
    # number = process_line_1(line)
    number = process_line_2(line)
    print(number)
    s += number

print(s)
# D poslat, treba jsem to spatne prepsal
# D check copied input radsi
# D nechal bych ulezet, at neztracim cas zatim!
# ND nebylo by uplne koser! muzes zkusit vystrihnout ty casti dont() az do() a pak na to pustit sum_mul jen jednou :shrug:
