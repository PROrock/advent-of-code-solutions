import dataclasses
import string
import sys


@dataclasses.dataclass
class Mapping:
    source_start: int
    source_end: int
    dest_offset: int

    @staticmethod
    def from_range_len(source, dest, range_len):
        return Mapping(source, source+range_len, dest-source)


seeds = [int(seed) for seed in sys.stdin.readline().rstrip("\r\n").split(": ")[1].split()]
sys.stdin.readline()  # empty row

maps = []
m = []
while True:
    line = sys.stdin.readline()
    if not line:
        maps.append(m)
        break
    line = line.rstrip("\r\n")

    if not line:  # end of map definition
        maps.append(m)
    elif line[0] in string.ascii_lowercase:  # map definition
        m = []
    else:
        dest, source, range_len = [int(i) for i in line.split()]
        if range_len < 1:
            print("range_len < 1!", range_len)
        m.append(Mapping.from_range_len(source, dest, range_len))

maps = [sorted(m, key=lambda m: m.source_end) for m in maps]


def get_destination(num, mappings):
    for m in mappings:
        if m.source_end > num:
            if m.source_start <= num:
                return num + m.dest_offset
            break
    return num


def get_location(seed, maps):
    num = seed
    for mappings in maps:
        new_num = get_destination(num, mappings)
        num = new_num
    return num


def solve(seeds, maps):
    locations = [get_location(seed, maps) for seed in seeds]
    print(f"{locations=}")
    return min(locations)

print(solve(seeds, maps))
