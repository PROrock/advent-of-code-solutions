from pathlib import Path

ROCK = "O"
WALL = "#"
EMPTY = "."


def load_lines():
    file = "./1.in"
    # file = "./2.in"
    return Path(file).read_text().splitlines()

def print_grid(grid):
    print("GRID")
    for line in grid:
        print(line)
    print("GRID END")

def debug(*strings):
    if False:
        print(*strings)

# todo:
# cycle
# move in 1 dir

def tilt_in_y_dir(grid, dir):
    # todo here



def process_segments(segment, max_load):
    n_rocks = segment.count(ROCK)
    return sum(range(max_load, max_load-n_rocks, -1))


def process_line(line):
    debug()
    debug("line", line)

    s = 0
    segments = line.split(WALL)
    max_load = len(line)
    for segment in segments:
        load = process_segments(segment, max_load)
        debug(segment, max_load, load)
        max_load -= len(segment) + 1
        s += load
        # print()
    return s


grid = load_lines()
# print_grid(grid)
transposed_grid = list(["".join(tuple_) for tuple_ in zip(*grid)])
# print_grid(transposed_grid)

s = 0
for line in transposed_grid:
    number = process_line(line)
    # print(number)
    s += number

print(s)
