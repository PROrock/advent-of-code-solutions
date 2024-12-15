import re
from collections import defaultdict
from functools import reduce
from pathlib import Path
from typing import NamedTuple

POS_PATTERN = re.compile(r"[pv]=(-?\d+),(-?\d+)")
SECS = 100

# WIDTH = 11
WIDTH = 101
# HEIGHT = 7
HEIGHT = 103
X_HALF = WIDTH // 2
Y_HALF = HEIGHT // 2

def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

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

    def modulo(self, width, height):
        return Vect(self.x % width, self.y % height)

    def quadrant(self):
        # 0 1
        # 2 3
        if self.x == X_HALF or self.y==Y_HALF:
            return None
        return int(self.x < X_HALF) + 2*int(self.y < Y_HALF)

def print_grid(grid):
    print("GRID")
    for line in grid:
        # print(line)
        print("".join(["." if i==0 else str(i) for i in line]))
    print("GRID END")

def parse_pv(pos):
    m = POS_PATTERN.match(pos)
    x,y = m.groups()
    return Vect(int(x),int(y))

def parse_line(line):
    pos, vel = line.split(" ")
    p, v = parse_pv(pos), parse_pv(vel)
    # print(line, p, v)
    return p, v

def get_pos_after_s(p, v, secs):
    np = p + v * secs
    nmp = np.modulo(WIDTH, HEIGHT)
    return nmp

def cr_grid():
    grid = []
    for _ in range(HEIGHT):
        grid.append([0 for _ in range(WIDTH)])
    return grid

def fill_grid(grid, poss):
    for p in poss:
        grid[p.y][p.x] += 1

lines = load_lines()
robots=[]
for line in lines:
    p, v = parse_line(line)
    robots.append((p,v))
nr=len(robots)

def part_a(robots):
    poss = []
    for p, v in robots:
        pos = get_pos_after_s(p, v, SECS)
        poss.append(pos)

    # grid = cr_grid()
    # fill_grid(grid, poss)
    # print_grid(grid)

    qs = get_qs(poss)
    # print([qs[i] for i in range(4)])
    print(reduce(lambda a, b: a * b, qs.values(), 1))

def get_qs(poss):
    qs = defaultdict(int)
    for pos in poss:
        q = pos.quadrant()
        if q is not None:
            qs[q] += 1
    return qs

def search_for_tree(robots, seconds):
    ps, vs = [el for el in zip(*robots)]

    # grid = cr_grid()
    # fill_grid(grid, ps)
    # print_grid(grid)

    candidates = []
    for i in range(1, seconds+1):
        ps = [(p + v).modulo(WIDTH, HEIGHT) for p,v in zip(ps, vs)]

        # desperate:
        # print(i)
        # grid = cr_grid()
        # fill_grid(grid, ps)
        # print_grid(grid)

        qs = get_qs(ps)
        # print(qs)

        byx = get_byx(ps)
        # print(byx)
        # print([len(byx[x]) for x in range(WIDTH)])

        trunk_size = (nr * 0.01)
        # if any(len(v) > trunk_size for v in byx.values()):
        if any(v > nr*0.5 for v in qs.values()):
            print(f"CANDIDATE {i}")
            candidates.append(i)
            # print(i)
            grid = cr_grid()
            fill_grid(grid, ps)
            print_grid(grid)

            print(qs)
            # print([len(byx[x]) for x in range(WIDTH)])

    print(f"{candidates=}")

def get_period(p, v):
    hist = {p}
    # print(p)
    for i in range(1, 500_000_000):
        if i % 1_000_000 == 0:
            print("mil: ", i)

        # ps = []
        # for p, v in zip(ps, vs):
        new_p = (p + v).modulo(WIDTH, HEIGHT)
        # print(new_p)
        if new_p in hist:
            return len(hist)
        hist.add(new_p)
        p = new_p

def get_byx(ps):
    byx = defaultdict(list)
    for p in ps:
        byx[p.x].append(p)
    return byx

# part_a(robots)

p, v = robots[0]
period = get_period(p, v)
print(f"{period=}")
search_for_tree(robots, period)
