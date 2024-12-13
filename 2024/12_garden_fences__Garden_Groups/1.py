from collections import deque, defaultdict
from pathlib import Path
from pprint import pprint
from typing import NamedTuple


def load_lines():
    # file = "./1.a.in"
    # file = "./1.b.in"
    # file = "./1.c.in"
    # file = "./1.d.in"
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

def elem_at_coor(grid, coor):
    return grid[coor.y][coor.x]

class Vect(NamedTuple):
    x: int
    y: int

    def invert(self):
        return Vect(-self.x, -self.y)

    def __add__(self, other):
        return Vect(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vect(self.x - other.x, self.y - other.y)

    def __mul__(self, multiplier):
        return Vect(self.x * multiplier, self.y * multiplier)


def coor_inbounds(coor: Vect):
    return 0 <= coor.x < width and 0 <= coor.y < height

grid = load_lines()
height = len(grid)
width = len(grid[0])

def print_grid(grid):
    print("GRID")
    for line in grid:
        print(line)
    print("GRID END")

DIR_TO_VECT = {
    "N": Vect(0, -1),
    "E": Vect(1, 0),
    "S": Vect(0, 1),
    "W": Vect(-1, 0),
}
DIRS_CLOCKWISE = list(DIR_TO_VECT.values())

def expand(node, grid, letter):
    children = []
    for dir_vect in DIRS_CLOCKWISE:
        new_coor = node + dir_vect
        if coor_inbounds(new_coor) and elem_at_coor(grid, new_coor) == letter:
            children.append(new_coor)
    return children

def mark_region(grid, region_map, first_pos, i_reg, letter):
    visited = set()
    q = deque([first_pos])
    while len(q):
        pos = q.popleft()
        if pos in visited:
            continue

        visited.add(pos)
        region_map[pos.y][pos.x] = i_reg

        neighbours = expand(pos, grid, letter)
        q.extend(neighbours)
    return visited

def create_region_map_and_areas(grid):
    areas = {}
    region_map = [[-1]*len(line) for line in grid]
    i_reg = 0

    for y, line in enumerate(grid):
        for x, letter in enumerate(line):
            pos = Vect(x, y)
            if elem_at_coor(region_map, pos) == -1:
                visited = mark_region(grid, region_map, pos, i_reg, letter)
                areas[i_reg] = len(visited)
                # print(i_reg)
                i_reg+=1

    return region_map, areas

def x_perimeter_pass(region_map, perimeters):
    for y, line in enumerate(region_map):
        first_r = line[0]
        prev_r = first_r
        perimeters[first_r] += 2
        for x, r in enumerate(line):
            if r != prev_r:
                perimeters[r] += 2
                prev_r = r

def get_perimeters(region_map):
    perimeters = defaultdict(int)
    x_perimeter_pass(region_map, perimeters)
    transposed = list(zip(*region_map))
    x_perimeter_pass(transposed, perimeters)
    return perimeters

def get_sides(region_map):
    sides = defaultdict(int)
    x_side_pass(region_map, sides)
    # print("sides after x pass")
    # print(sides)
    transposed = list(zip(*region_map))
    x_side_pass(transposed, sides)
    return sides

def x_side_pass(region_map, sides):
    # r: set of tuples (is_oi_bool, x-coor)
    prev_counted_verts=defaultdict(set)
    for y, line in enumerate(region_map):
        next_verts = defaultdict(set)

        first_r = line[0]
        handle_diff(next_verts, prev_counted_verts, first_r, sides, x=0, is_oi=True)
        prev_r = first_r
        for x, r in enumerate(line):
            if r != prev_r:
                handle_diff(next_verts, prev_counted_verts, prev_r, sides, x, is_oi=False)
                handle_diff(next_verts, prev_counted_verts, r, sides, x, is_oi=True)
                prev_r = r
        handle_diff(next_verts, prev_counted_verts, prev_r, sides, x=len(region_map), is_oi=False)
        prev_counted_verts=next_verts
        # print(f"{next_verts=}")
        # print(f"{sides=}")

def handle_diff(next_verts, prev_counted_verts, r, sides, x, is_oi):
    #oi = outside-to-inside fence (or start of the region)
    t = (is_oi, x)
    if t not in prev_counted_verts[r]:
        sides[r] += 1
    next_verts[r].add(t)

# print_grid(grid)
region_map, areas = create_region_map_and_areas(grid)
print_grid(region_map)
print("areas")
pprint(areas)

# perimeters = get_perimeters(region_map)
# print("perimeters")
# print(perimeters)

sides = get_sides(region_map)
print("sides")
print(sides)

# costs={r: area*perimeters[r] for r, area in areas.items()}
costs={r: area*sides[r] for r, area in areas.items()}
print(sum(costs.values()))
