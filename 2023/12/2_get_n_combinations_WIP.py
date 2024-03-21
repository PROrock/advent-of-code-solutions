import re
from pathlib import Path

# todo vratit pak finalne na 5
FOLD_TIMES = 4
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
    # file = "./2.in"
    # file = "./2.S.in"
    file = "./2.XS.in"   # 2393557
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


def get_n_combinations_internal(record, groups):
    print("get_n_combinations_internal", record, groups)

    # if more 2+ groups, split to sub-problems
    if len(groups) > 1:
        # split
        first_subgroup_len = len(groups)//2  # this can be tuned
        first_subgroup = groups[:first_subgroup_len]
        second_subgroup = groups[first_subgroup_len:]
        # first_group, *rest_of_groups = groups
        min_first_subgroup_start = sum([r+1 for r in first_subgroup])
        # not sure with that, would be nice to unit test
        max_first_subgroup_start = len(record) - sum([r+1 for r in second_subgroup]) + 1
        for i_split in range(min_first_subgroup_start, max_first_subgroup_start):
            # todo optimization - check if it makes sense (doesnt end with BROKEN/hash)
            # todo optimisation, some splits are the same? maybe not because the first split if it ends with BROKEN, it is said to be invalid, then its ok
            #  ?????, [2, 1],
            #  1. ??? ?? 2 combinations
            #  2. ???? ? 2 combinations, but one is the same! -> this naive approach wont work!
            # find already completely filled groups and split by them
            # maybe start by positioning the longest group, then get possibilities of ofter records
            # then move the tallest one and just remove invalid possibilities from earlier

            # for first group, identify min and max position and for every one generate all possibilities
            # then for another position of first group - take prev. possibilities and removes invalid ones, rest is still valid
            # todo heuristic - if sum of (group + 1) -1 is len record, then its only 1 possibility (if it is 100% valid before), or check validity of such solution
            # todo heuristic - if already broken streak can be only one group, start with that group?

            return get_n_combinations_internal(record[:i_split], first_subgroup) * get_n_combinations_internal(record[i_split:], second_subgroup)
    # elif 1 group - compute
    elif len(groups) == 1:
        return get_n_combinations_internal_one_group(record, groups)

    else:  # 0 groups
        print("can i get here?", record, groups)

        if BROKEN in record:
            debug("invalid, all groups satisfied, but still some BROKEN chars left in record...")
            return 0
        else:
            return 1  # ok


def get_n_combinations_internal_one_group(record, groups):
    pass

    # # compute
    # n_surely_broken = record.count(BROKEN)
    # n_missing_broken = sum(groups) - n_surely_broken
    # if n_missing_broken == record.count(UNKNOWN):
    #     # print("just one option - fill all questions marks with broken")
    #     return 1
    # # ?#?#? 3 is 1
    # # ??##? 3 is 2
    # # ??#?? 3 is 3
    # # ?.#?? 3 is 1
    # # ?#.#? 3 is 0
    # # ?.#?. 3 is 0
    # # ?.#?. 1 is 1
    # # ?.??. 1 is 3
    # # todo can it end with non-dot? if last, yes, otherwise, no
    # # regex based?
    # # try every position, travel forward to after dot if present, check only the new position? - PAL way! I like
    # first_broken_idx = record.find(UNKNOWN)
    # last_broken_idx = record.rfind(UNKNOWN)
    #
    #
    # group_len = sum(groups)
    # # pos = 0
    # overlap = 0 if first_broken_idx == -1 else (last_broken_idx-first_broken_idx + 1)
    # if overlap == group_len:
    #     # overlap = (last_broken_idx-first_broken_idx+1)
    #     # if overlap == group_len:
    #     return 1
    #
    # min_starting_pos = 0 if first_broken_idx == -1 else first_broken_idx - (group_len - overlap)
    # max_starting_pos = len(record) - group_len if first_broken_idx == -1 else last_broken_idx - (group_len - overlap)  # inclusive
    # # pos = max(0, last_broken_idx-first_broken_idx)
    # non_dot_streak = 0
    # # # todo have to start and end on first, last hash!
    # # while pos <= len(record) - group_len:
    # #     if record[pos] == OPERATIONAL:
    # #         non_dot_streak = 0
    # #         pos =
    # pos = min_starting_pos
    # while pos <= max_starting_pos:
    #     if record[pos] == OPERATIONAL:
    #         non_dot_streak = 0
    #         # todo here
    #         pos +=
    #     else:
    #         non_dot_streak += 1
    #         pos += 1





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


def unfold(record, groups):
    records = [record] * FOLD_TIMES
    return UNKNOWN.join(records), groups * FOLD_TIMES


s = 0
lines = load_lines()
for line in lines:
    record, groups = line.split()
    groups = [int(i) for i in groups.split(",")]
    # print(record, groups)
    record, groups = unfold(record, groups)
    # print(record, groups)
    record = simplify(record)

    number = get_n_combinations(record, groups)
    print(record, groups, number)
    debug()
    s += number

print(s)


# todo:
# D zkusit profiler asi na netu - rekurze se vola strasne moc hodnekrat
# zkusit rozdelit na podproblemy - kolik zpusobu pro tyto podskupiny je na tomto splitu * na tom zbyvajicim a secist pro ruzne splity.
# pak zacit umistenim nejdelsi groupou
