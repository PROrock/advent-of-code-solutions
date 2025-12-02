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

def add_line(s, dial, number):
    small_num = abs((dial + number) // 100)
    if dial + number <= 0 and (dial + number) % 100 == 0:
        small_num += 1
    if dial == 0 and number < 0:
        small_num -= 1
    s += small_num

    dial = (dial + number) % 100
    print(number, dial, s, small_num)
    return s, dial


for line in lines:
    number = process_line(line)
    s, dial = add_line(s, dial, number)

print(s)

# print()
# assert add_line(0, 50, -50) == (1, 0)
# assert add_line(0, 50, -150) == (2, 0)
# assert add_line(0, 97, -897) == (9, 0)
# assert add_line(0, 0, -345) == (3, 55)

