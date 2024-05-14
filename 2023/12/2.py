import re
from pathlib import Path
from typing import List

# todo vratit pak finalne na 5
FOLD_TIMES = 1
OPERATIONAL = "."
BROKEN = "#"
UNKNOWN = "?"
BROKEN_PATTERN = re.compile("(#+)")
MULTIPLE_OPERATIONAL_PATTERN = re.compile("[.]{2,}")


def debug(*strings):
    if True:
    # if False:
        print(*strings)


def load_lines():
    # file = "./1.in"
    # file = "./2.in"
    # file = "./2.S.in"
    # file = "./2.XS.in"   # 2393557  # 21s (fold=4)  # fold=1 133, like 1s
    # file = "./3.in"
    file = "./4.in"  # should be 5
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
            debug("invalid, all groups satisfied, but still some BROKEN chars left in record...")
            # pass
        else:
            debug("yielding", record)
            yield record  # maybe 1 would be sufficient?


def generate_all_combinations_list5(record, groups, offset) -> List[List[int]]:
    debug(groups, "gen", record, groups, offset)
    if len(groups) == 1:
        generated = [[offset + candidate.start(1)]
                     for candidate in _generate_valid_candidates(record, groups)
                     if BROKEN not in record[candidate.end(1):]]
        debug(groups, "generated last group", generated)
        return generated
    return _generate_all_combinations_for_more_groups(record, groups, offset)


def _generate_all_combinations_for_more_groups(record, groups, offset) -> List[List[int]]:
    valid_candidates = _generate_valid_candidates(record, groups)

    all_possibilities = []
    prev_subpossibilities = None
    for candidate in valid_candidates:
        debug(groups, "expanding candidate", candidate, candidate.start(1), candidate.end(1), f"{prev_subpossibilities=}")
        if prev_subpossibilities is None:
            subrecord_offset = candidate.end(1) + 1  # plus one for space between groups
            curr_subpossibilities = generate_all_combinations_list5(record[subrecord_offset:], groups[1:],
                                                                    offset + subrecord_offset)
        else:
            curr_subpossibilities = [subpossibility for subpossibility in prev_subpossibilities if _subpossibility_valid(subpossibility, offset + candidate.end(1))]

        if not curr_subpossibilities:
            debug(groups, "No curr_subpossibilities for candidate, groups", groups)
            prev_subpossibilities = None
            continue  # it can work later after first sol and second nonsol too I think

        curr_possibilities = [[offset + candidate.start(1), *possibility] for possibility in curr_subpossibilities]
        debug(groups, candidate, groups, "add partial solution ->", f"{curr_possibilities=}")
        all_possibilities.extend(curr_possibilities)
        debug(groups, f"{all_possibilities=}")

        prev_subpossibilities = curr_subpossibilities
        # print("try another candidate")
    return all_possibilities


def _subpossibility_valid(subpossibility, prev_candidate_end):
    return prev_candidate_end + 1 <= subpossibility[0]


def _generate_valid_candidates(record, groups) -> List[re.Match]:
    first_group, *rest_of_groups = groups
    end_of_window = (len(record) - sum([r + 1 for r in rest_of_groups])) if rest_of_groups else len(record)

    pattern = rf"(?<!#)(?=([#?]{{{first_group}}})(?!#))"
    candidate_positions = list(re.finditer(pattern, record[:end_of_window + 1]))
    debug(record, pattern, first_group, rest_of_groups, end_of_window, "candidate_starts",
          [c.start(1) for c in candidate_positions])

    valid_candidates = []
    for candidate in candidate_positions:
        if BROKEN in record[:candidate.start(1)]:
            debug(
                f"invalid candidate! {candidate.start(1)}. Groups: {candidate.groups()}. Previous chars {record[:candidate.start(1)]} contains BROKEN. candidate: {record[candidate.start(1):candidate.end(1)]}")
            continue
        if candidate.start(1) + first_group > end_of_window:
            debug(
                f"invalid candidate! too far. {candidate} {candidate.start(1)}. {candidate.start(1) + first_group}>{end_of_window}")
            continue
        valid_candidates.append(candidate)
    return valid_candidates


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
    # solutions = list(generate_all_combinations_list4("".join(record), groups))
    solutions = list(generate_all_combinations_list5("".join(record), groups, 0))
    debug(solutions)
    return len(solutions)


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

# for first group, identify min and max position and for every one generate all possibilities
# then for another position of first group - take prev. possibilities and removes invalid ones, rest is still valid

# heuristic - generating candidates not via regex, but via "rolling window" - stop immediatelly also after we get behind hash/broken!
# heuristic - remove space in front of for every subproblem, also if hash/broken is the first, fill the group immediatelly

# todo heuristic - WITH FOLDING, NOT SO APPLICABLE! if sum of (group + 1) -1 is len record, then its only 1 possibility (if it is 100% valid before), or check validity of such solution
# todo heuristic - if already broken streak can be only one group, start with that group?

# pridal jsem groups na zacatek a zatm to staci
# debug print also uroven zanoreni k printum a to si pocitat v rekurzi?! strasne to pomuze ladeni (nebo opravdovy debug no)
# https://stackoverflow.com/questions/12399259/finding-the-level-of-recursion-call-in-python
# or code something like this guy: https://www.codementor.io/@dmitrybelaventsev/python-trace-recursive-function-tkq79m4so


# todo problem je ten, ze muj super algoritmus ma diru
#  kdyz je prvni solution [0, 3, 5] a druhy ma byt [0, 5, 7], tak mi ho nenajde - problem: ?#???#.? 2,1,1 (output ma byt 3)
# 0,3,5
# 0,5,7
# 1,5,7
# if idx is 5 or more then run the search once again?
# IDK, I give up now. Would have to draw it probably and think about cases
