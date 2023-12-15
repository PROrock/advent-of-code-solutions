import re
from pathlib import Path

OPERATIONAL = "."
BROKEN = "#"
UNKNOWN = "?"
BROKEN_PATTERN = re.compile("(#+)")
MULTIPLE_OPERATIONAL_PATTERN = re.compile("[.]{2,}")


def replace(s, replacement, idx):
    # return s[:idx] + replacement + s[idx+1:]  # 11, 6, 6
    # return "".join((s[:idx], replacement, s[idx+1:])) # 9,7,6s
    return f"{s[:idx]}{replacement}{s[idx + 1:]}"  # 7, 10, 8, 6

def replace_list(s, replacement, idx):
    # return [*s[:idx], replacement, *s[idx+1:]]
    s[idx] = replacement
    return s

def load_lines():
    # file = "./1.in"
    # file = "./2.in"
    # file = "./2.S.in"
    file = "./2.XS.in"
    return Path(file).read_text().splitlines()


# def is_so_far_valid(record, groups):
#     # first_question_mark
#     matches = list(re.finditer("(#+)", record))
#     matched_groups = [m.end()-m.start() for m in matches]
#     # print(matched_groups, groups)
#     return matched_groups == groups

def generate_all_combinations_list(record):
    # print("gen", record)
    unknown_indices = [i for i, c in enumerate(record) if c == UNKNOWN]
    if len(unknown_indices):
        first_unknown_idx = unknown_indices[0]
        for option in (OPERATIONAL, BROKEN):
            record[first_unknown_idx] = option
            # new_record = replace_list(record, option, first_unknown_idx)
            # print(f"put {option} on index {first_unknown_idx}, changing {record} to {new_record}")
            yield from generate_all_combinations_list(record)
            # print("try 2d option")
        record[first_unknown_idx] = UNKNOWN
    else:
        # print("yielding", record)
        yield "".join(record)


def generate_all_combinations_list2(record, unknown_indices):
    # print("gen", record)
    # unknown_indices = [i for i, c in enumerate(record) if c == UNKNOWN]
    if len(unknown_indices):
        first_unknown_idx = unknown_indices[0]
        for option in (OPERATIONAL, BROKEN):
            record[first_unknown_idx] = option
            # new_record = replace_list(record, option, first_unknown_idx)
            # print(f"put {option} on index {first_unknown_idx}, changing {record} to {new_record}")
            yield from generate_all_combinations_list2(record, unknown_indices[1:])
            # print("try 2d option")
        record[first_unknown_idx] = UNKNOWN
    else:
        # print("yielding", record)
        yield "".join(record)

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


def generate_all_combinations(record):
    # print("gen", record)
    unknown_indices = [i for i, c in enumerate(record) if c == UNKNOWN]
    if len(unknown_indices):
        first_unknown_idx = unknown_indices[0]
        for option in (OPERATIONAL, BROKEN):
            new_record = replace(record, option, first_unknown_idx)
            # print(f"put {option} on index {first_unknown_idx}, changing {record} to {new_record}")
            yield from generate_all_combinations(new_record)
            # print("try 2d option")
    else:
        # print("yielding", record)
        yield record


def get_n_combinations_wip(record, groups):
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


def is_valid(record, groups):
    matches = list(BROKEN_PATTERN.finditer(record))
    if len(matches) != len(groups):
        return False
    matched_groups = [m.end()-m.start() for m in matches]
    # print(matched_groups, groups)
    return matched_groups == groups


def strip_leading_operationals(record):
    # if not record:
    #     return record
    for i, c in enumerate(record):
        if c != OPERATIONAL:
            return record[i:]
    return []


def get_n_combinations(record, groups):
    record = list(record)
    s = 0
    # print("gen list", list(generate_all_combinations(record)))
    # for generated_record in generate_all_combinations(record):
    # for generated_record in generate_all_combinations_list(list(record)):

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
    # for generated_record in generate_all_combinations_list2(list(record), unknown_indices):
    for generated_record in generate_all_combinations_list3(record, unknown_indices, n_missing_broken):
        if is_valid(generated_record, groups):
            s += 1
            # print(f"{generated_record} is valid, {s=}")
    return s


def fill_first_group_if_possible(record, groups):
    while record[0] == BROKEN and record and groups:
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
    # print(number)
    print(record, groups, number)
    s += number

print(s)

# todo:
# D count how many of broken we need to add
# D small optimization - strip dots, replace 2 dots with 1

# generate candidate positions via regex of [.?]
# sliding window - forget last and read next char