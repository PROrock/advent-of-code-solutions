from pathlib import Path


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


def process_line(line):
    num = int(line[1:])
    sign = 1 if line[0]=="R" else -1
    return num * sign


lines = load_lines()
s = 0
dial = 50
for line in lines:
    number = process_line(line)
    dial = (dial + number) % 100
    print(number, dial)
    if dial == 0:
        s += 1

print(s)
