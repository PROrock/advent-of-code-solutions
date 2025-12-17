from pathlib import Path

from utils.grid_utils import Vect, elem_at_pos, set_elem_at_pos_str
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

# min_x and y saves like 1500 empty rows and columns
min_x = min([p.x for p in points]) - 1
min_y = min([p.y for p in points]) - 1
width -= min_x
height -= min_y
v = Vect(min_x, min_y)
points = [p-v for p in points]

print(width, height)
# lists takes too long, str is ok
grid = ["."*width for _ in range(height)]
print("grid")
# todo here
#  either try to adapt to str code
#  or somehow try to do it without the grid instantiation with just the polygon
# print_grid(grid)

# points
for p in points:
    set_elem_at_pos_str(grid, p, "#")
print("# on grid")
# print_grid(grid)
# save_grid_to_file(grid[:1000], "10_2_grid_points.txt")

# construct lines
for a,b in zip(points, points[1:]+points[:1]):
    dir = b-a
    dir = dir.normalize_to_signs()
    # print(dir)
    p = a
    while p != b:
        p += dir
        set_elem_at_pos_str(grid, p, "X")
    set_elem_at_pos_str(grid, p, "#")
print("X on grid")
# print_grid(grid)

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
for y, line in enumerate(grid):
    inside = False
    last_was_wall = False
    inside_idx = None
    for x, c in enumerate(line):
        if c in VALID_TILES:
            if inside:
                # line[inside_idx:x] = "X"*(x-inside_idx)
                inside_str = "X"*(x-inside_idx)
                line = f"{line[:inside_idx]}{inside_str}{line[x:]}"
            last_was_wall = True
        else:
            if last_was_wall:
                inside = not inside
                inside_idx = x
                last_was_wall = False
    grid[y] = line
print("inside filled")
# print_grid(grid)
# i did this, but it's too much still, takes a lot of time to generate the inside in grid!


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
