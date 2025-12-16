from pathlib import Path
from pprint import pprint

from utils.grid_utils import create_grid, rotate, print_grid, flip, EMPTY
from utils.utils import ints, gen_split_lines_by_empty_lines


def load_lines():
    file = "./1.in"
    # file = "./2.in"
    return Path(file).read_text().splitlines()

def parse_shapes(line_groups):
    shapes = {}  # idx -> 3x3 grid
    for idx, line_group in enumerate(line_groups):
        # idx = line_group[0][0]
        grid = line_group[1:]
        shapes[idx] = tuple([tuple(line) for line in grid])
    return shapes

def get_rotations(sgrid):
    s = set()
    # print_grid(sgrid)
    for flipped in (False, True):
        if flipped:
            sgrid = flip(sgrid)
            # print_grid(sgrid)
        for i in range(4):
            r = rotate(sgrid, i)
            s.add(r)
            # print_grid(r)
    return s

def parse_region(line):
    integers = ints(line)
    assert len(integers) == 8

    size = (max(integers[:2]), min(integers[:2]))
    return size, integers[2:]

def process_region(region):
    # to do: sanity check enough pixels for the shapes

    size, shapes = region
    rgrid = create_grid(*size)
    return 1 if fit(shapes, rgrid) else 0

def fit(shapes, rgrid):
    # print("fit", shapes)
    if sum(shapes) == 0:
        return True

    # todo try list instead of generator! might be quicker
    i_shape = next((i for i, s in enumerate(shapes) if s != 0), None)

    for j, rotation in enumerate(all_rotations[i_shape]):
        for y in range(len(rgrid) - len(rotation) + 1):
            for x in range(len(rgrid[0]) - len(rotation[0]) + 1):
                # print(f"Testing shape {i_shape} in rotation {j} to pos ({x}, {y}).")
                added = add_shape(rgrid, rotation, x, y, i_shape)
                # print("shaped added:", added)
                # print_grid(rgrid)
                if added:
                    shapes[i_shape] -= 1
                    result = fit(shapes, rgrid)
                    if result:
                        print("result")
                        print_grid(rgrid)
                        return True
                    shapes[i_shape] += 1
                    rollback_the_grid_to_empty(rgrid, rotation, x, y, len(rotation[0]), len(rotation)-1)

        # print("rotation done")
    # print("Test done")
    return False

def add_shape(rgrid, rotation, x_offset, y_offset, i_shape):
    # if we expect the block won't fit in most cases, might make sense to first just check, than fill, not to having to rollback everytime
    for y in range(len(rotation)):
        for x in range(len(rotation[0])):
            if rotation[y][x] == EMPTY:
                continue
            val = rgrid[y_offset+y][x_offset+x]
            if val != EMPTY:
                rollback_the_grid_to_empty(rgrid, rotation, x_offset, y_offset, x, y)
                return False

            rgrid[y_offset+y][x_offset+x] = str(i_shape)
    return True

def rollback_the_grid_to_empty(rgrid, rotation, x_offset, y_offset, max_x, max_y):
    for y in range(max_y+1):
        for x in range(max_x if y == max_y else len(rotation[0])):
            if rotation[y][x] != EMPTY:
                rgrid[y_offset + y][x_offset + x] = EMPTY


lines = load_lines()
line_groups = list(gen_split_lines_by_empty_lines(lines))
definitions = parse_shapes(line_groups[:6])
pprint(definitions)

# gen all rotations and flipping and deduplicate!
all_rotations = {i: get_rotations(sgrid) for i, sgrid in definitions.items()}
# pprint(all_rotations)
# for i, rotations in all_rotations.items():
#     print(i)
#     for rotation in rotations:
#         print_grid(rotation)
#     print()


regions = [parse_region(line) for line in line_groups[6]]
regions = sorted(regions, key=lambda r: (r[0], r[1]))

s = 0
for region in regions:
    print(region)
    number = process_region(region)
    print(number)
    s += number

print(s)
