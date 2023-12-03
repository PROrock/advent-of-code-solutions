import re
import sys

SYMBOL_PATTERN = re.compile("[^\da-zA-Z.]")

schematic = []
while True:
    line = sys.stdin.readline().rstrip("\r\n")
    if not line:
        break
    schematic.append(line)

width = len(schematic[0])


def get_neighbours_str(schematic, m, y):
    neighbours = []
    if y > 0:
        neighbours.append(schematic[y-1][max(0, m.start()-1):min(width, m.end()+1)])
    neighbours.append(schematic[y][max(0, m.start()-1):m.start()])
    neighbours.append(schematic[y][m.end():min(width, m.end()+1)])
    if y + 1 < len(schematic):
        neighbours.append(schematic[y+1][max(0, m.start()-1):min(width, m.end()+1)])
    return "".join(neighbours)


def get_part_number_and_len(schematic, m, y):
    neighbours_str = get_neighbours_str(schematic, m, y)
    is_touching_symbol = bool(next(SYMBOL_PATTERN.finditer(neighbours_str), False))
    return int(m[0]) if is_touching_symbol else 0


s = 0
for y in range(len(schematic)):
    for m in re.finditer(r"(\d+)", schematic[y]):
        s += get_part_number_and_len(schematic, m, y)

print(s)
