from pathlib import Path


def load_lines():
    file = "./1.in"
    # file = "./2.in"
    return Path(file).read_text().splitlines()

def parse_workflow(line):
    return line
def parse_part(line):
    return line


lines = load_lines()
blank_line_idx = lines.index("")
workflows = [parse_workflow(line) for line in lines[:blank_line_idx]]
parts = [parse_part(line) for line in lines[blank_line_idx+1:]]
print(workflows)
print(parts)


s = 0
for part in parts:
    result = process_part(part, workflows)
    if result == "A":
        num
    # print(number)
    s += number

print(s)
