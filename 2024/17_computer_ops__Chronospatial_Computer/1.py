import math
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint

from typing import List


def load_lines():
    # file = "./1.in"
    # file = "./1.b.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

@dataclass
class Computer:
    a: int
    b: int
    c: int
    program: List[int]
    output: List[int] = field(default_factory=list)
    op_idx: int = 0

    def _combo_op(self, i):
        if i<=3:
            return i
        return (self.a,self.b,self.c)[i-4]

    def op0(self, op):
        self.a = self._adv(op)

    def _adv(self, op):
        # return math.floor(self.a / 2 ** self._combo_op(op))
        # return self.a // 2 ** self._combo_op(op)
        return self.a >> self._combo_op(op)

    def op1(self, op):
        self.b = self.b ^ op

    def op2(self, op):
        self.b = self._combo_op(op) % 8

    def op3(self, op):
        if self.a != 0:
            self.op_idx = op

    def op4(self, op):
        self.b = self.b ^ self.c

    def op5(self, op):
        self.output.append(self._combo_op(op) % 8)

    def op6(self, op):
        self.b = self._adv(op)

    def op7(self, op):
        self.c = self._adv(op)

    def ops(self):
        return [self.op0, self.op1,self.op2,self.op3,self.op4,self.op5,self.op6,self.op7]

    def run(self):
        while True:
            if self.op_idx >= len(self.program):
                # print("halt")
                break

            # self.print_state()
            operation = self.program[self.op_idx]
            self.process(operation, self.program[self.op_idx + 1])
            if not (operation == 3 and self.a != 0):
                self.op_idx += 2

    def process(self, operation, operand):
        # print(f"{operation=}, {operand=}")
        self.ops()[operation](operand)

    def print_state(self):
        print(self)

    def check_copy(self):
        return self.output == self.program[:len(self.output)]


lines = load_lines()
registers=lines[:3]
registers=[int(reg_line.split(": ")[1]) for reg_line in registers]
program=lines[4].split(": ")[1]
program=[int(i) for i in program.split(",")]
# print(registers)
# print(program)

a,b,c = registers
# part a
computer = Computer(a,b,c,program)
computer.run()
print(",".join([str(i) for i in computer.output]))

# part b

# thinking notes:
# ops to save to a: 0,
# pro 0,3 -> always A=floor(A/2^3) and A must be == 0 after len(program) cycles/operations
# A = 0 at the end of the last iteration
# A = 1 - 7 at the beginning of the last iteration
# A = 8 - 63 at the beginning of the second to last iteration
assert len(program)%2==0
assert program[-2]==3
assert program[-1]==0

ins_codes = program[::2]
# print(ins_codes)
ADV_CODE = 0  # only operation which saves something to the A reg.!
n_advs = sum([i == ADV_CODE for i in ins_codes])
assert n_advs == 1
advs_idx = program.index(ADV_CODE)
advs_oper = program[advs_idx+1]
assert advs_oper <= 3

denominator = 2**advs_oper
n = len(program)

all_candidates={}
candidates = [0] # so it halts!
for i in range(n):
    program_cycle = len(program)-i-1
    p = program[program_cycle]
    print("new", i, program_cycle, "p=", p, candidates)

    next_candidates = []
    for cand in candidates:
        lo = cand * denominator
        hi = (cand+1)*denominator - 1

        # print("candidate", c, lo, hi)
        for aa in range(lo, hi+1):
            computer = Computer(aa,b,c,program[:-2]) # -2 -> without jumping back!
            computer.run()
            if computer.output[0] == p and cand != aa: # to ignore zero
                next_candidates.append(aa)

    all_candidates[i] = next_candidates
    candidates = next_candidates

aa=candidates[0]
computer = Computer(aa,b,c,program)
computer.run()
if computer.output is not None and computer.output == computer.program:
    print("RLY FOUND")
    print(aa)