from pathlib import Path


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


def hash_step(step):
    h = 0
    for c in step:
        h = ((h+ord(c))*17)%256
    return h


lines = load_lines()
s = 0
for line in lines:
    for step in line.split(","):
        number = hash_step(step)
        # print(step, number)
        s += number

print(s)
