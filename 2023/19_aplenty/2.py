import ast
import copy
import dataclasses
import re
from functools import reduce
from pathlib import Path

@dataclasses.dataclass
class Condition:
    attr: str
    is_gt: bool
    value: int


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

def parse_workflow(line):
    matches = re.fullmatch(r"(\w+)\{([a-zAR0-9<>,:]+)\}", line)
    rules = matches.group(2)
    rules = rules.split(",")
    rules = [rule.split(":") if ":" in rule else (None, rule) for rule in rules]
    rules = [((None if cond is None else Condition(cond[0], cond[1] == ">", int(cond[2:]))), dest) for cond, dest in rules]
    return matches.group(1), rules

def parse_part(line):
    line = re.sub(r"([xmas])", "\"\\1\"", line)
    line = line.replace("=", ":")
    # print(line)
    return ast.literal_eval(line)

def process_part(part, workflows, workflow_name):
    # print(part, workflow_name)

    if workflow_name in {"A", "R"}:
        return workflow_name

    workflow = workflows[workflow_name]
    for rule in workflow:
        condition, dest = rule
        if condition is None or eval(condition, {}, part):
            return process_part(part, workflows, dest)

    return 1/0

lines = load_lines()
blank_line_idx = lines.index("")
workflows = dict(parse_workflow(line) for line in lines[:blank_line_idx])
parts = [parse_part(line) for line in lines[blank_line_idx+1:]]

print(workflows)
print()


@dataclasses.dataclass
class Interval:
    min: int
    max: int

    def apply(self, condition):
        if condition.is_gt:
            return Interval(max(self.min, condition.value+1),self.max)
        return Interval(self.min, min(self.max, condition.value-1))

    def apply_compl(self, condition):
        if condition.is_gt:
            return Interval(self.min, min(self.max, condition.value))
        return Interval(max(self.min, condition.value),self.max)

    def n_pos(self):
        if self.min > self.max: return 0
        return self.max - self.min + 1


MIN = 1
MAX = 4000


def space_search(node, space):
    # print(node, space)

    if node == "A":
        # multiply space attributes to get combinations
        dims = [interval.n_pos() for interval in space.values()]
        n_combs = reduce(lambda a, b: a * b, dims, 1)
        print(node, n_combs, space)

        return n_combs
    if node == "R":
        return 0

    workflow = workflows[node]
    s = 0
    for rule in workflow:
        condition, dest = rule

        if condition is None:
            space_copy = space
        else:
            space_copy = copy.copy(space)
            old_interval = space_copy[condition.attr]
            space_copy[condition.attr] = old_interval.apply(condition)

        result = space_search(dest, space_copy)
        s += result

        if condition is not None:
            space[condition.attr] = space[condition.attr].apply_compl(condition)
    return s


space = {l: Interval(MIN, MAX) for l, _ in zip("xmas", range(4))}
print(space_search("in", space))
