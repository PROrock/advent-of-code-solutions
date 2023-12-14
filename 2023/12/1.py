import sys

OPERATIONAL = "."
BROKEN = "#"
UNKNOWN = "?"

def load_lines():
    lines = []
    while True:
        line = sys.stdin.readline().rstrip("\r\n")
        if not line:
            break
        lines.append(line)
    return lines


def generate_all_combinations(record, group):
    unknown_indices = [i for i, c in enumerate(record) if c==UNKNOWN]
    if len(unknown_indices):
        # todo here
        # first_unknown = unknown_indices[]
        pass
    else:
        # finished
        pass


def get_n_combinations(line):
    record, groups = line.split()
    groups = [int(i) for i in groups.split(",")]
    print(record, groups)

    if UNKNOWN not in record:
        return 1
    # group_it = iter(groups)
    group_idx = 0
    current_group_start = None
    for i, spring in enumerate(record):
        if spring == OPERATIONAL:
            pass
        elif spring == BROKEN:
            if current_group_start is None:
                current_group_start = i

    return 0


s = 0
lines = load_lines()
for line in lines:
    number = get_n_combinations(line)
    print(number)
    s += number

print(s)

#easier to generate and validate and count
