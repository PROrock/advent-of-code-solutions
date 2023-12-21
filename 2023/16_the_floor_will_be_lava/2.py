import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple


class Vect(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Vect(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vect(self.x - other.x, self.y - other.y)


@dataclass(frozen=True)
class Beam:
    coor: Vect
    dir: str


DIR_TO_VECT = {
    "N": Vect(0, -1),
    "E": Vect(1, 0),
    "S": Vect(0, 1),
    "W": Vect(-1, 0),
}

TILE_TO_NEW_DIRS = {
    "/": {"N": ["E"], "E": ["N"], "S": ["W"], "W": ["S"]},
    "\\": {"N": ["W"], "E": ["S"], "S": ["E"], "W": ["N"]},
    "|": {"N": ["N"], "E": ["N", "S"], "S": ["S"], "W": ["N", "S"]},
    "-": {"N": ["E", "W"], "E": ["E"], "S": ["E", "W"], "W": ["W"]},
}

def print_bool_grid(grid):
    print("GRID")
    for line in grid:
        print("".join(["#" if tile else "." for tile in line]))
    print("GRID END")


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()




grid = load_lines()
height = len(grid)
width = len(grid[0])
energized_tiles = [[False] * width for _ in grid]


def get_tile(grid, coor):
    return grid[coor.y][coor.x]

def coor_inbounds(coor):
    return 0 <= coor.x < width and 0 <= coor.y < height

def process_beams(starting_beams):
    beams = starting_beams
    processed_beams = set()
    while beams:
        beam = beams.pop()
        if beam in processed_beams:
            continue

        new_beams = process_beam(beam)
        beams.extend(new_beams)
        processed_beams.add(beam)


def energize_coor(coor):
    energized_tiles[coor.y][coor.x] = True

def process_beam(beam):
    coor = beam.coor
    new_coor = coor + DIR_TO_VECT[beam.dir]
    # print(beam, new_coor)
    while coor_inbounds(new_coor) and get_tile(grid, new_coor) == ".":
        energize_coor(new_coor)
        new_coor = new_coor + DIR_TO_VECT[beam.dir]
    # print(beam, "stopped at", new_coor)
    if coor_inbounds(new_coor):
        tile = get_tile(grid, new_coor)
        new_dirs = TILE_TO_NEW_DIRS[tile][beam.dir]
        energize_coor(new_coor)
        # print(beam, "to", new_coor, new_dirs)
        return [Beam(new_coor, new_dir) for new_dir in new_dirs]
    else:
        return []


horizontal_starts = [(Beam(Vect(-1,y), "E"), Beam(Vect(width, y), "W")) for y in range(height)]
vertical_starts = [(Beam(Vect(x, -1), "S"), Beam(Vect(x, height), "N")) for x in range(width)]
all_starts = [*horizontal_starts, *vertical_starts]
all_starts = list(itertools.chain.from_iterable(all_starts))

max_energy = 0
for starting_beam in all_starts:
    energized_tiles = [[False] * width for _ in grid]
    starting_beams = [starting_beam]
    process_beams(starting_beams)

    energy = sum([int(t) for line in energized_tiles for t in line])
    if energy > max_energy:
        max_energy = energy
print(max_energy)
