import re
from collections import deque, defaultdict
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint

from utils.utils import ints, split_lines_on_empty_line


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
    # a,op,b,out = re.fullmatch(r"(\w{3}) (AND|OR|XOR) (\w{3}) -> (\w{3})")
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
vals_lines, gates_lines = split_lines_on_empty_line(lines)
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
# # pprint(vals)
# # pprint(gates)
# # print(zs)
#
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

# gen_dot(gates)

max_z = max(int(z[1:]) for z in zs)
# print(max_z)

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

# pprint(correct)
# gen_dot(correct)

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
w2g = {}
# for i in range(max_z):
#     for l in "xyz":
#         w2g[n(l, i)] = n(l, i)
# pprint(w2g)

# # z45 = l44+m44
# q = deque([n("z", max_z)])
# while len(q):
#     v = q.popleft()
#     cg = correct[v]
#     wg = gates[v]
#     # print(cg)
#     # print(wg)
#     assert wg.op == cg.op
#     # todo symmetry! also start from x and y probably!
#     w2g[wg.a]=cg.a
#     w2g[wg.b]=cg.b
#
#     q.extend([wg.a,wg.b])
#     # todo
#     break

xys=list()
for i in range(max_z):
    for l in "xy":
        xys.append(n(l, i))

def find_by_op(gs, op, assert_size=None):
    filtered = [g for g in gs if g.op == op]
    if assert_size is not None:
        assert len(filtered)==assert_size
    return filtered[0]

xys_set = set(xys)
x_to_check = [n("x", i) for i in range(0, max_z)]

swapped = []
def check_l(v: str, i, x):
    # print(f"checking {v}")
    if v.startswith("z"):
        print(f"candidate for swap! {v} is swapped with an 'l' node!")
        return

    wgs = in2gates[v]
    corr_v = n("l", i)
    cgs = in2corrects[corr_v]
    if len(wgs) != len(cgs):
        # gate = gates[v]
        # swapped_with = "k" if gate.op=="XOR" else "c"
        # print(f"candidate for swap! {v} should have {len(cgs)}, but has {len(wgs)} out arrows. Candidate for k or c node. By gate and op {gate} it is '{swapped_with}'. {wgs}")
        print(f"candidate for swap! {v} should have {len(cgs)}, but has {len(wgs)} out arrows. Candidate for k or c node. Wrong in2gates: {wgs}")
        return
    # assert len(wgs) == len(cgs)
    # assert 1 <= len(wgs) <= 2
    # assert 1 <= len(cgs) <= 2
    # assert len(wgs) == 1
    # assert len(cgs) == 1
    w2g[lv]= corr_v

def check_general(v: str, corr_v, exp_insize):
    if corr_v == n("c", max_z-1):
        corr_v = n("z", max_z)
        exp_insize = 0

    wgs = in2gates[v]
    cgs = in2corrects[corr_v]
    # print(v, corr_v, wgs, cgs)
    assert exp_insize == len(cgs)

    if len(wgs) != len(cgs):
        swapped.append(v)
        print(f"candidate for swap! {v} should have {len(cgs)} like {corr_v}, but has {len(wgs)} out arrows. Candidates {get_candidates(wgs)}. Wrong in2gates: {wgs}")
        return None
    w2g[lv]= corr_v
    return corr_v

def get_candidates(wgs):
    if len(wgs) == 2:
        return ["k", "c"]
    if len(wgs) == 1:
        # g=wgs[0]
        # if
        return ["l", "m"]
    if len(wgs) == 0:
        return ["z"]
    print("WEIRD CANDICATES!!! ", wgs)
    return ["WEIRD CANDICATES!"]
#
for i, x in enumerate(x_to_check):
    if i == 0:
        # todo
        # todo 0 as exception! doesnt have k and l but z and c!
        continue
    # if i == 1:
    #     # todo
    #     # todo 0 as exception! doesnt have k and l but z and c!
    #     continue
    v = x
    wgs = in2gates[v]
    cgs = in2corrects[v]

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
# todo why 9?



# inputs a,b are always right!
# outputs can be wrong
# network can be wrong but inputs are calling right inputs

# for z in zs:
#     wgs = in2gates[z]
#     if len(wgs) != 0:
#         print(f"{z} has {len(wgs)}, {wgs=}")
# for z in zs:
#     wgs = gates.get(z)
#     if wgs is not None:
#         print(f"{z} has {wgs=}")
# # always

missing = set(gates)-set(w2g)
print(missing)


pprint(w2g)
print(",".join(sorted(swapped)))