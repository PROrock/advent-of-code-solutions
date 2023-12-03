import re
import string
import sys

SYMBOL_PATTERN = re.compile("[^\da-zA-Z.]")


schematic = []
while True:
    line=sys.stdin.readline().rstrip("\r\n")
    if not line:
        break
    schematic.append(line)

for line in schematic:
    print(line)
width = len(schematic[0])

s = 0


def get_part_number_and_len(schematic, x, y):
    end = x + 1
    while end < width and schematic[y][end] in string.digits:
        end+=1
    # for end in range(x, width):
    #     if schematic[y][end] not in string.digits:
    #         break
    number_len = end - x
    # while x < width and schematic[x] in string.digits:
    #     number+
    number = 0
    print(number, number_len)
    return number, number_len


for y in range(len(schematic)):
    x = 0
    while x < width:
        if schematic[y][x] in string.digits:
            number, number_len = get_part_number_and_len(schematic, x, y)
            # print(number, number_len)
            s += number
            # move behind this number
            x += number_len
            print("OJ:", x)
        else:
            x += 1

print(s)
