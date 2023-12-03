import re
import sys
from collections import defaultdict

schematic = []
while True:
    line = sys.stdin.readline().rstrip("\r\n")
    if not line:
        break
    schematic.append(line)

height = len(schematic)
width = len(schematic[0])
stars_to_neighbours = defaultdict(list)


def generate_neighbours_indices(m, y):
    if y > 0:
        for x in range(max(0, m.start() - 1), min(width, m.end() + 1)):
            yield x, y - 1
    if (x := m.start() - 1) >= 0:
        yield x, y
    if (x := m.end()) < width:
        yield x, y
    if y + 1 < height:
        for x in range(max(0, m.start() - 1), min(width, m.end() + 1)):
            yield x, y + 1


def add_to_dict(schematic, star_to_neighbours, m, y_number):
    for x, y in generate_neighbours_indices(m, y_number):
        if schematic[y][x] == "*":
            star_to_neighbours[(x, y)].append(m)


for y in range(height):
    for m in re.finditer(r"(\d+)", schematic[y]):
        add_to_dict(schematic, stars_to_neighbours, m, y)

s = 0
for star_numbers in stars_to_neighbours.values():
    if len(star_numbers) == 2:
        first, second = star_numbers
        gear_ratio = int(first[0]) * int(second[0])
        s += gear_ratio

print(s)
