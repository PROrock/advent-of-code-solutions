from pathlib import Path


def load_lines():
    file = "./1.in"
    # file = "./2.in"
    return Path(file).read_text().splitlines()


def process_line(line):
    return -1


lines = load_lines()
s = 0
for line in lines:
    number = process_line(line)
    # print(number)
    s += number

print(s)
