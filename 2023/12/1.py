import re
from pathlib import Path

OPERATIONAL = "."
BROKEN = "#"
UNKNOWN = "?"
BROKEN_PATTERN = re.compile("(#+)")
MULTIPLE_OPERATIONAL_PATTERN = re.compile("[.]{2,}")
# CANDIDATE_POS_PATTERN = re.compile("[.]{2,}")

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


def generate_all_combinations_list3(record, unknown_indices, n_missing_broken):
    # print("gen", record)
    # unknown_indices = [i for i, c in enumerate(record) if c == UNKNOWN]
    if len(unknown_indices):
        first_unknown_idx = unknown_indices[0]
        for option in (OPERATIONAL, BROKEN):
            if n_missing_broken == 0 and option == BROKEN:
                continue
            record[first_unknown_idx] = option
            # new_record = replace_list(record, option, first_unknown_idx)
            new_n_missing_broken = n_missing_broken - (1 if option == BROKEN else 0)
            # print(f"put {option} on index {first_unknown_idx}, changing {record} to {new_record}")
            yield from generate_all_combinations_list3(record, unknown_indices[1:], new_n_missing_broken)
            # print("try 2d option")
        record[first_unknown_idx] = UNKNOWN
    else:
        # print("yielding", record)
        yield "".join(record)


def generate_all_combinations_list4(record, groups):
    debug("gen", record, groups)
    if len(groups):
        # first_group = groups[0]
        first_group, *rest_of_groups = groups
        # sum_rest = len(record) - sum([r+1 for r in rest_of_groups]) if rest_of_groups else len(record)
        end_of_window = (len(record) - sum([r+1 for r in rest_of_groups])) if rest_of_groups else len(record)

        # pattern = f"([#?]{{{first_group}}})(?:[.?]|$)"
        # pattern = f"([#?]{{{first_group}}})(?!#)"
        # pattern = f"(?=([#?]{{{first_group}}})(?!#))"
        pattern = rf"(?<!#)(?=([#?]{{{first_group}}})(?!#))"
        # candidate_positions = list(re.finditer(pattern, record[:end_of_window]))
        candidate_positions = list(re.finditer(pattern, record[:end_of_window+1]))
        debug(record, pattern, first_group, rest_of_groups, end_of_window, "candidate_starts", [c.start(1) for c in candidate_positions])
        for candidate in candidate_positions:
            # if candidate.start(1) > 0 and record[candidate.start(1)-1] == BROKEN:
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


def is_valid(record, groups):
    matches = list(BROKEN_PATTERN.finditer(record))
    if len(matches) != len(groups):
        return False
    matched_groups = [m.end()-m.start() for m in matches]
    # print(matched_groups, groups)
    return matched_groups == groups


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
    for generated_record in generate_all_combinations_list4("".join(record), groups):
        s += 1
        # if is_valid(generated_record, groups):
        #     s += 1
        debug(f"{generated_record} is valid, {s=}")
    return s


def fill_first_group_if_possible(record, groups):
    while groups and record and record[0] == BROKEN:
        # fill first group + space
        first_group = groups[0]
        # record[1:first_group] = [BROKEN] * (first_group-1)
        # record[first_group+1] = OPERATIONAL
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

# 9049 is too high
