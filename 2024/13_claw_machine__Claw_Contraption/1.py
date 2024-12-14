import re
from pathlib import Path
from typing import NamedTuple

B_OFFSET = 10000000000000

def is_eps_equal(a, b, eps=1e-6):
    return abs(a-b)<eps

def solve_system_2_equations(a,b,c,d,e,f):
    """
    system:
    ax + by + c = 0
    dx + ey + f = 0

    solve:
    x=(-by-c)/a
    x=(-ey-f)/d
    (-by-c)/a = (-ey-f)/d
    (-by-c)*d = (-ey-f)*a
    -dby-dc = -aey-af
    aey-dby = dc-af
    (ae-db)y = dc-af
    y = (dc-af)/(ae-db)
    then:
    x=(-by-c)/a
    """
    assert a != 0
    assert b != 0
    assert c != 0
    assert d != 0
    y = (d*c-a*f)/(a*e-d*b)
    # x = (-b*y-c)/a
    # numerically more stable for part b!
    x = -(b/a)*y - c/a

    # print(x, y)
    # print(a*x+b*y+c)
    # print(d*x+e*y+f)
    # assert a*x+b*y+c == 0
    # assert d*x+e*y+f == 0
    # assert is_eps_equal(a*x+b*y+c, 0)
    # assert is_eps_equal(d*x+e*y+f, 0)
    if is_eps_equal(b/a, e/d):
        print("parallel! No or inf solutions")
        return None, None
    return x, y

# # x+y=5
# # 2x-y=1
# print(solve_system_2_equations(1, 1, -5, 2, -1, -1))


class Machine(NamedTuple):
    ax: int
    ay: int
    bx: int
    by: int
    tx: int
    ty: int

def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

def parse_xy(line):
    pattern = r" X[+=](\d+), Y[+=](\d+)"
    m = re.match(pattern, line)
    return m.groups()

def parse_machine(machine_lines):
    l = []
    for line in machine_lines[:-1]:
        l.extend(parse_xy(line.split(":")[1]))
    l = [int(i) for i in l]
    # part b
    l[4] += B_OFFSET
    l[5] += B_OFFSET
    return Machine(*l)

def process_machine(m):
    #x: aA + bB + c = 0
    #y: dA + eB + f = 0
    a, b = solve_system_2_equations(m.ax, m.bx, -m.tx, m.ay, m.by, -m.ty)
    # print(a, b)

    # part a
    # for n in (a,b):
    #     if not n.is_integer():
    #         return 0
    for n in (a,b):
        if n < 0:
            return 0
    a,b=int(round(a)), int(round(b))
    if not(m.ax*a+m.bx*b==m.tx and m.ay*a+m.by*b==m.ty):
        return 0
    return 3*a+b

lines = load_lines()
lines.append("")

machines = []
for i in range(len(lines)//4):
    machines.append(parse_machine(lines[i*4:(i+1)*4]))

s = 0
for machine in machines:
    # print(machine)
    number = process_machine(machine)
    # print(number)
    s += number

print(s)
