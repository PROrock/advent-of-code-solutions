import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from utils.utils import split_lines_on_empty_line_in_2


def load_lines():
    # file = "./1.s.in"
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

@dataclass
class Gate:
    a: str
    op: str
    b: str
    out: str

    def compute(self, a, b):
        if self.op == "AND": return a and b
        if self.op == "OR": return a or b
        if self.op == "XOR": return a ^ b
        assert "WTF" == ""

def parse(line):
    groups = re.fullmatch(r"(\w{3}) (AND|OR|XOR) (\w{3}) -> (\w{3})", line).groups()
    return Gate(*groups)

def get_o(n):
    if n in vals:
        return vals[n]

    g = gates[n]
    val = g.compute(get_o(g.a),get_o(g.b))
    vals[n]=val
    return val


lines = load_lines()
vals_lines, gates_lines = split_lines_on_empty_line_in_2(lines)
vals = {}
for line in vals_lines:
    a,b = line.split(": ")
    vals[a]=bool(int(b))

gates={} # by out, out to gate
for line in gates_lines:
    gate = parse(line)
    gates[gate.out] = gate

zs = [g for g in gates if g.startswith("z")]
# # part a
# bits=[]
# for z in sorted(zs, reverse=True):
#     bits.append(get_o(z))
# print(int("".join([str(int(i)) for i in bits]), 2))

# part b
def gen_dot(gates):
    for out, g in gates.items():
        print(f"{g.out} [label=\"{g.out}\\n{g.a} {g.op} {g.b}\"]")
    for out, g in gates.items():
        print(edge_dot(g, g.a))
        print(edge_dot(g, g.b))
def edge_dot(g, a):
    return f"{a} -> {g.out} [label={g.op}]"

max_z = max(int(z[1:]) for z in zs)

def add_node(out, a, op, b):
    correct[out] = Gate(a, op, b, out)

def n(l, i):
    return f"{l}{i:02}"

correct = {}
i=0
add_node(n("z", i), n("x", i), "XOR", n("y", i))
add_node(n("c", i), n("x", i), "AND", n("y", i))

for i in range(1, max_z):
    add_node(n("k", i), n("x", i), "XOR", n("y", i))
    add_node(n("l", i), n("x", i), "AND", n("y", i))
    add_node(n("m", i), n("c", i-1), "AND", n("k", i))
    add_node(n("z", i), n("k", i), "XOR", n("c", i))
    add_node(n("c", i), n("l", i), "OR", n("m", i))

# rename c44 na z45
c44 = correct[n("c", max_z-1)]
add_node(n("z", max_z), c44.a, c44.op, c44.b)
del correct[n("c", max_z-1)]

assert len(correct) == len(gates)

def g_by_in(gates):
    in2gates = defaultdict(list)
    for g in gates.values():
        in2gates[g.a].append(g)
        in2gates[g.b].append(g)
    return in2gates

in2gates = g_by_in(gates)
in2corrects = g_by_in(correct)

# matching!
def find_by_op(gs, op, assert_size=None):
    filtered = [g for g in gs if g.op == op]
    if assert_size is not None:
        assert len(filtered)==assert_size
    return filtered[0]

def check_general(v: str, corr_v, exp_insize):
    if corr_v == n("c", max_z-1):
        corr_v = n("z", max_z)
        exp_insize = 0

    wgs = in2gates[v]
    cgs = in2corrects[corr_v]
    assert exp_insize == len(cgs)

    if len(wgs) != len(cgs):
        swapped.append(v)
        return None
    return corr_v

swapped = []
x_to_check = [n("x", i) for i in range(0, max_z)]
for i, x in enumerate(x_to_check):
    if i == 0:
        # to-do 0 as exception! doesn't have k and l but z and c!
        # could be programmed, if needed, probably via some 1-2 "if" statements as z45
        continue
    wgs = in2gates[x]
    cgs = in2corrects[x]

    lv = find_by_op(wgs, "AND", 1).out
    kv = find_by_op(wgs, "XOR", 1).out
    corr_l = check_general(lv, n("l", i), 1)
    if corr_l is not None:
        cv = in2gates[lv][0].out
        # check_c
        check_general(cv, n("c", i), 2)

    corr_k = check_general(kv, n("k", i), 2)
    if corr_k is not None:
        m_and_z = in2gates[kv]
        # print(m_and_z)
        mv = find_by_op(m_and_z, "AND", 1).out
        zv = find_by_op(m_and_z, "XOR", 1).out
        corr_m = check_general(mv, n("m", i), 1)
        corr_z = check_general(zv, n("z", i), 0)

print(",".join(sorted(swapped)))