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

def reverse_lines_in_grid(grid):
    return [line[::-1] for line in grid]


# todo:
# cycle
# move in 1 dir

# def tilt_in_y_dir(grid, dir):
def tilt_to_west(grid):
    new_grid = []
    for line in grid:
        # todo here
        new_segments = []
        segments = line.split(WALL)
        for segment in segments:
            # load = process_segments(segment, max_load)
            n_rocks = segment.count(ROCK)
            new_segments.append(n_rocks*[ROCK] + (len(segment)-n_rocks)*[EMPTY])
        new_line = WALL.join(new_segments)
        new_grid.append(new_line)
    print()
    print_grid(new_grid)
    return new_grid

def tilt_to_east(grid):
    to_east_reversed = tilt_to_west(reverse_lines_in_grid(grid))
    return reverse_lines_in_grid(to_east_reversed)

# def tilt_to_

def cycle_one_time(grid):
    #north
    transposed_grid = [tuple_ for tuple_ in zip(*grid)]
    tilt_to_west(transposed_grid)
    # todo here

    #west
    #south
    #east
    # return

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
