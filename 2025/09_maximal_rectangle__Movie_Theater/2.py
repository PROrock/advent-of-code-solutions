from pathlib import Path

from utils.grid_utils import Vect, print_grid, set_elem_at_pos, elem_at_pos
from utils.utils import ints

VALID_TILES = {"#", "X"}


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


lines = load_lines()
points = [Vect(*ints(line)) for line in lines]
# print(points)

# construct grid
width = max([p.x for p in points]) + 2
height = max([p.y for p in points]) + 2
print(width, height)
# lists takes too long
# grid = [list("."*width) for _ in range(height)]
# grid = [["." for _ in range(width)] for _ in range(height)]
grid = ["."*width for _ in range(height)]
print("grid")
# todo here
#  either try to adapt to str code
#  or somehow try to do it without the grid instantiation with just the polygon
# print_grid(grid)

# points
for p in points:
    set_elem_at_pos(grid, p, "#")
print_grid(grid)

# construct lines
for a,b in zip(points, points[1:]+points[:1]):
    dir = b-a
    dir = dir.normalize_to_signs()
    # print(dir)
    p = a
    while p != b:
        p += dir
        set_elem_at_pos(grid, p, "X")
    set_elem_at_pos(grid, p, "#")
print_grid(grid)

# fill shape
# # not working
# for line in grid:
#     inside = False
#     last_was_wall = False
#     for x, c in enumerate(line):
#         if c in {"#", "X"}:
#             last_was_wall = True
#             # inside = not inside
#         else:
#             if last_was_wall:
#                 inside = not inside
#                 last_was_wall = False
#             if inside:
#                 line[x] = "X"

# fill shape
# not working
for line in grid:
    inside = False
    last_was_wall = False
    inside_idx = None
    for x, c in enumerate(line):
        if c in VALID_TILES:
            if inside:
                line[inside_idx:x] = list("X"*(x-inside_idx))
            last_was_wall = True
        else:
            if last_was_wall:
                inside = not inside
                inside_idx = x
                last_was_wall = False
print_grid(grid)


# sort the points by y then x
sps = sorted(points, key=lambda p: (p.y, p.x))
# print(sps)

def is_valid_line(p, q):
    dir = (q-p)
    dir_norm = dir.normalize_to_signs()
    return all(elem_at_pos(grid, p+(dir_norm*i)) in VALID_TILES for i in range(dir.l_inf_norm()))


def valid_perimeter():
    # check 4 sides
    for x, y in zip((a.x, b.x), (b.y, a.y)):
        corner = Vect(x, y)
        if not is_valid_line(a, corner):
            return False
        if not is_valid_line(b, corner):
            return False
    return True


# every pair* with row and column checks to both sides
m = 0
for a in sps:
    for b in sps:
        if b.y < a.y or b==a:
            continue

        if valid_perimeter():
            area = a.area_for_grid(b)
            if area > m:
                m = area

print(m)
