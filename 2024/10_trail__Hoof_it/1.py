from collections import defaultdict
from pathlib import Path
from typing import NamedTuple


def load_lines():
    # file = "1.a.in"
    # file = "1.b.in"
    # file = "1.c.in"
    # file = "1.d.in"
    # file = "1.e.in"
    # file = "1.in"
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

def as_ints(grid):
    ints = []
    for line in grid:
        ints.append([-1 if i=="." else int(i) for i in line])
    return ints


grid = load_lines()
grid = as_ints(grid)
height = len(grid)
width = len(grid[0])

def print_grid(grid):
    print("GRID")
    for line in grid:
        print(line)
    print("GRID END")

def find_all_in_grid(grid, val):
    r = []
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == val:
                r.append(Vect(x, y))
    return r
# def find_all_in_grid(grid, char_):
#     r = []
#     for y, line in enumerate(grid):
#         for m in re.finditer(char_, line):
#             r.append(Vect(m.start(), y))
#     return r

DIR_TO_VECT = {
    "N": Vect(0, -1),
    "E": Vect(1, 0),
    "S": Vect(0, 1),
    "W": Vect(-1, 0),
}
DIRS_CLOCKWISE = list(DIR_TO_VECT.values())


def expand(node, grid, level):
    children = []
    for dir_vect in DIRS_CLOCKWISE:
        new_coor = node + dir_vect
        if coor_inbounds(new_coor) and elem_at_coor(grid, new_coor) == level:
            children.append(new_coor)
    return children


def score(grid):
    nines = find_all_in_grid(grid, 9)
    next_level = 8
    curr = {n:{n} for n in nines}

    while next_level >= 0:
        # print(next_level+1)
        # pprint(curr)
        next_ = defaultdict(set)
        for node, peaks in curr.items():
            children = expand(node, grid, next_level)
            for c in children:
                next_[c] |= peaks
        curr = next_
        next_level -= 1
    return sum([len(peaks) for peaks in curr.values()])


def rating(grid):
    nines = find_all_in_grid(grid, 9)
    next_level = 8
    curr = {n:{n:1} for n in nines}  # coor -> {peak -> n_ways/rating}

    while next_level >= 0:
        # print(next_level+1)
        # pprint(curr)

        next_ = defaultdict(lambda: defaultdict(int))
        for node, peak_map in curr.items():
            # print(node, peak_map)
            children = expand(node, grid, next_level)
            for c in children:
                new_peak_map = next_[c]
                for peak, r in peak_map.items():
                    # print(c, peak, r)
                    new_peak_map[peak] += r
        curr = next_
        next_level -= 1
    return sum([sum(peak_map.values()) for peak_map in curr.values()])

# print(score(grid))
print(rating(grid))
