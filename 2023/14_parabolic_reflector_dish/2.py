from pathlib import Path

ROCK = "O"
WALL = "#"
EMPTY = "."
MAX_CYCLES_TO_DETECT_CYCLE=1_000
N_CYCLES=1_000_000_000


def load_lines():
    file = "./1.in"
    # file = "./2.in"
    return tuple(Path(file).read_text().splitlines())

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
    return tuple([line[::-1] for line in grid])

def transpose_grid(grid):
    transposed_grid = tuple(["".join(tuple_) for tuple_ in zip(*grid)])
    return transposed_grid


def tilt_to_west(grid):
    new_grid = []
    for line in grid:
        new_segments = []
        segments = line.split(WALL)
        for segment in segments:
            n_rocks = segment.count(ROCK)
            new_segments.append(n_rocks*ROCK + (len(segment)-n_rocks)*EMPTY)
        new_line = WALL.join(new_segments)
        new_grid.append(new_line)
    return tuple(new_grid)


def tilt_to_east(grid):
    to_east_reversed = tilt_to_west(reverse_lines_in_grid(grid))
    return reverse_lines_in_grid(to_east_reversed)


def cycle_one_time(grid):
    # print("rly computing cycle")
    new_grid = grid
    #north
    new_grid = transpose_grid(tilt_to_west(transpose_grid(new_grid)))
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


def compute_line_load(line):
    s = 0
    segments = line.split(WALL)
    max_load = len(line)
    for segment in segments:
        load = process_segments(segment, max_load)
        debug(segment, max_load, load)
        max_load -= len(segment) + 1
        s += load
    return s


def get_cycle_warmup_and_period(grid):
    grid_idx = {grid: 0}
    for i in range(MAX_CYCLES_TO_DETECT_CYCLE):
        new_grid = cycle_one_time(grid)
        if new_grid in grid_idx:
            print(f"cycle detected - From grid idx {grid_idx[grid]} to {grid_idx[new_grid]}")
            return grid_idx[new_grid], grid_idx[grid] - grid_idx[new_grid] + 1
        else:
            grid_idx[new_grid] = len(grid_idx)

        # print(f"detection: From grid idx {grid_idx[grid]} to {grid_idx[new_grid]}")
        grid = new_grid

def get_grid_by_idx(grid, idx):
    """Better solution would be to save the grid_idx dict or something."""
    for i in range(idx):
        grid = cycle_one_time(grid)
    return grid

def get_final_grid(orig_grid):
    warmup, period = get_cycle_warmup_and_period(orig_grid)
    # print(warmup, period)

    remaining_cycles = N_CYCLES - warmup
    remainder_cycles = remaining_cycles % period
    final_idx = warmup + remainder_cycles
    # print(remaining_cycles, remainder_cycles, final_idx)
    return get_grid_by_idx(orig_grid, final_idx)


def compute_total_load(grid):
    s = 0
    transposed_grid = transpose_grid(grid)
    for line in transposed_grid:
        number = compute_line_load(line)
        # print(number)
        s += number
    return s


orig_grid = load_lines()
final_grid = get_final_grid(orig_grid)
# assert [g for g, idx in grid_idx.items() if idx == final_idx][0] == final_grid

print(compute_total_load(final_grid))
# answer: 103
