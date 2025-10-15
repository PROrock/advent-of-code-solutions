import ast
import re
from pathlib import Path


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

def parse_workflow(line):
     matches = re.fullmatch(r"(\w+)\{([a-zAR0-9<>,:]+)\}", line)
     rules = matches.group(2)
     rules = rules.split(",")
     # for rule in rules:
     #     condition, dest = rule.split(":") if rule.contains(":") else None, rule

     rules = [rule.split(":") if ":" in rule else (None, rule) for rule in rules]
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
print(parts)
print()

s = 0
for part in parts:
    result = process_part(part, workflows, "in")
    if result == "A":
        number = sum(part.values())
    else:
        number = 0
    # print(part, result, number)
    s += number

print(s)
