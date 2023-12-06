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
seed_ranges = [range(seed, seed+seed_range) for seed, seed_range in zip(seeds[::2], seeds[1::2])]
sys.stdin.readline()  # empty row
print(seed_ranges)

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
        mapping = Mapping.from_range_len(source, dest, range_len)
        m.append(mapping)

maps = [sorted(m, key=lambda m: m.source_end) for m in maps]


def get_one_destination_range(one_range, mappings):
    num = one_range.start
    for m in mappings:
        if m.source_end > num:
            if m.source_start <= num:
                # found matching mapping - use it and report the rest of the range
                new_end = min(m.source_end, one_range.stop)
                return range(num + m.dest_offset, new_end + m.dest_offset), range(new_end, one_range.stop) if new_end < one_range.stop else None
            # current m is starting higher than current range_start
            new_end = min(m.source_start, one_range.stop)
            # identity
            return range(num, new_end), range(new_end, one_range.stop) if new_end < one_range.stop else None

    # all mapping_obj are lower than one_range, just identity range
    return one_range, None


def get_all_destination_ranges(one_range, mappings):
    destination_ranges = []
    while one_range is not None:
        # we could try faster version, where this is one loop -> we know where in mappings we were the last time
        new_range, next_range = get_one_destination_range(one_range, mappings)
        destination_ranges.append(new_range)
        one_range = next_range

    return destination_ranges


def get_min_location(seed_range, maps):
    ranges = [seed_range]
    for mappings in maps:
        new_ranges = [one_dest_range for one_range in ranges for one_dest_range in get_all_destination_ranges(one_range, mappings)]
        ranges = new_ranges
    return min(ranges, key=lambda r: r.start).start


def solve(seed_ranges, maps):
    locations = [get_min_location(seed_range, maps) for seed_range in seed_ranges]
    print(f"{locations=}")
    return min(locations)

print(solve(seed_ranges, maps))
