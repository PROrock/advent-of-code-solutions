import re
from pathlib import Path

OPERATIONAL = "."
BROKEN = "#"
UNKNOWN = "?"
BROKEN_PATTERN = re.compile("(#+)")
MULTIPLE_OPERATIONAL_PATTERN = re.compile("[.]{2,}")


def debug(*strings):
    if False:
        print(*strings)


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    # file = "./2.S.in"
    # file = "./2.XS.in"
    # file = "./3.in"
    return Path(file).read_text().splitlines()


def generate_all_combinations_list4(record, groups):
    debug("gen", record, groups)
    if len(groups):
        first_group, *rest_of_groups = groups
        end_of_window = (len(record) - sum([r+1 for r in rest_of_groups])) if rest_of_groups else len(record)

        pattern = rf"(?<!#)(?=([#?]{{{first_group}}})(?!#))"
        candidate_positions = list(re.finditer(pattern, record[:end_of_window+1]))
        debug(record, pattern, first_group, rest_of_groups, end_of_window, "candidate_starts", [c.start(1) for c in candidate_positions])
        for candidate in candidate_positions:
            if BROKEN in record[:candidate.start(1)]:
                debug(f"invalid candidate! {candidate.start(1)}. Groups: {candidate.groups()}. Previous chars {record[:candidate.start(1)]} contains BROKEN. candidate: {record[candidate.start(1):candidate.end(1)]}")
                continue
            if candidate.start(1) + first_group > end_of_window:
                debug(f"invalid candidate! too far. {candidate} {candidate.start(1)}. {candidate.start(1) + first_group}>{end_of_window}")
                continue
            # print(candidate, candidate.end(), candidate.end(1))
            yield from generate_all_combinations_list4(record[candidate.end(1)+1:], groups[1:])
            # print("try 2d option")
    else:
        if BROKEN in record:
            debug(f"invalid, all groups satisfied, but still some BROKEN chars left in record...")
            pass
        else:
            debug("yielding", record)
            yield record  # maybe 1 would be sufficient?


def strip_leading_operationals(record):
    for i, c in enumerate(record):
        if c != OPERATIONAL:
            return record[i:]
    return []


def get_n_combinations(record, groups):
    record = list(record)
    s = 0
    # fill first group if possible
    record, groups = fill_first_group_if_possible(record, groups)
    # repeat from the back
    record, groups = fill_first_group_if_possible(list(reversed(record)), list(reversed(groups)))
    record = list(reversed(record))
    groups = list(reversed(groups))

    unknown_indices = [i for i, c in enumerate(record) if c == UNKNOWN]
    n_surely_broken = record.count(BROKEN)
    n_missing_broken = sum(groups) - n_surely_broken
    if n_missing_broken == len(unknown_indices):
        # print("just one option - fill all questions marks with broken")
        return 1
    return len(list(generate_all_combinations_list4("".join(record), groups)))


def fill_first_group_if_possible(record, groups):
    while groups and record and record[0] == BROKEN:
        # fill first group + space
        first_group = groups[0]
        new_record = record[first_group + 1:]
        new_record = strip_leading_operationals(new_record)
        # print(f"shortened {record} to {new_record} by completing group {first_group}")
        record = new_record
        groups = groups[1:]
    return record, groups


def simplify(record: str):
    new_record = record.strip(OPERATIONAL)
    return MULTIPLE_OPERATIONAL_PATTERN.sub(OPERATIONAL, new_record)


s = 0
lines = load_lines()
for line in lines:
    record, groups = line.split()
    record = simplify(record)

    groups = [int(i) for i in groups.split(",")]
    # print(record, groups)

    number = get_n_combinations(record, groups)
    print(record, groups, number)
    debug()
    s += number

print(s)
