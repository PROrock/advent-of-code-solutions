import re
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
# pprint(vals)
# pprint(gates)
# print(zs)

bits=[]
for z in sorted(zs, reverse=True):
    bits.append(get_o(z))

# pprint(vals)
# print(bits)
print(int("".join([str(int(i)) for i in bits]), 2))
