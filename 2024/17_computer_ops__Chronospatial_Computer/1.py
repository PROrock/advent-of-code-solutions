import math
from dataclasses import dataclass, field
from pathlib import Path

from typing import List


def load_lines():
    file = "./1.in"
    # file = "./2.in"
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
        return math.floor(self.a / 2 ** self._combo_op(op))

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
                print("halt")
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
        # print(self.a, self.b, self.c, self.op_idx)
        print(self)


lines = load_lines()
registers=lines[:3]
registers=[int(reg_line.split(": ")[1]) for reg_line in registers]
program=lines[4].split(": ")[1]
program=[int(i) for i in program.split(",")]
print(registers)
print(program)

a,b,c = registers
computer = Computer(a,b,c, program)
computer.run()
print(",".join([str(i) for i in computer.output]))
