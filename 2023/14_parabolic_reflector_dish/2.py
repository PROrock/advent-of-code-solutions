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
    print()

def debug(*strings):
    if False:
        print(*strings)

def reverse_lines_in_grid(grid):
    return [line[::-1] for line in grid]

def transpose_grid(grid):
    transposed_grid = ["".join(tuple_) for tuple_ in zip(*grid)]
    return transposed_grid


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
            new_segments.append(n_rocks*ROCK + (len(segment)-n_rocks)*EMPTY)
        new_line = WALL.join(new_segments)
        new_grid.append(new_line)
    # print()
    # print_grid(new_grid)
    return new_grid

# def tilt_to_

def tilt_to_east(grid):
    to_east_reversed = tilt_to_west(reverse_lines_in_grid(grid))
    return reverse_lines_in_grid(to_east_reversed)


def cycle_one_time(grid):
    new_grid = grid
    #north
    # print_grid(transposed_grid)
    # print("OJOJ")
    new_grid = transpose_grid(tilt_to_west(transpose_grid(new_grid)))
    # todo here

    #west
    new_grid = tilt_to_west(new_grid)

    #south
    new_grid = transpose_grid(reverse_lines_in_grid(tilt_to_west(reverse_lines_in_grid(transpose_grid(new_grid)))))

    #east
    new_grid = reverse_lines_in_grid(tilt_to_west(reverse_lines_in_grid(new_grid)))

    return new_grid



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
print_grid(grid)
# transposed_grid = list(["".join(tuple_) for tuple_ in zip(*grid)])
# print_grid(transposed_grid)

# s = 0
new_grid = grid
for i in range(3):
    new_grid = cycle_one_time(new_grid)
    print(f"After {i+1}. cycle")
    print_grid(new_grid)
# for line in transposed_grid:
#     number = process_line(line)
#     # print(number)
#     s += number

# print(s)
