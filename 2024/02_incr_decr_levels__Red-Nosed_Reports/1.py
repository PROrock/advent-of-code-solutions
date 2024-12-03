from pathlib import Path

def signum(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def remove_at_index(list_, idx):
    return list_[:idx] + list_[idx+1:]

def load_lines():
    # file = "./1.in"
    file = "./2.in"
    # file = "./3.in"
    return Path(file).read_text().splitlines()


def process_line_part_1(numbers):
    direction = 0
    prev = numbers[0]
    for curr in numbers[1:]:
        diff = curr - prev
        sign = signum(diff)
        if sign == 0:
            return 0  #unsafe
        if direction == 0:
            direction = sign
        if direction != sign or abs(diff) > 3:
            return 0  #unsafe
        prev = curr
    return 1


# def process_signs(numbers):
#     already_removed = False
#     diffs = [curr - prev for prev, curr in zip(numbers[:-1], numbers[1:])]
#
#     signs = [signum(d) for d in diffs]
#     # print(line)
#     print(diffs)
#     # print(signs)
#
#     counter = Counter(signs)
#     if len(counter.most_common(3)) == 1:
#         return None, diffs, already_removed
#
#     second_most_common_tuple = counter.most_common(3)[1]
#     second_most_common_dir = second_most_common_tuple[1]
#     if second_most_common_dir > 1 or len(counter.most_common(3)) > 2:
#         return 0, diffs, already_removed
#
#     bad_sign = signs.index(second_most_common_tuple[0])
#     idx_to_add = to_which_end_to_add(diffs, bad_sign)
#     removed_d = diffs[bad_sign]
#     diffs = remove_at_index(diffs, bad_sign)
#     diffs[bad_sign+idx_to_add] += removed_d
#     already_removed = True
#
#     # to-do check new diffs! might not be still good - still not good!
#     signs = [signum(d) for d in diffs]
#     if len(Counter(signs).most_common(3)) != 1:
#         return 0, diffs, already_removed
#
#     return None, diffs, already_removed
#
#
# def to_which_end_to_add(diffs, bad_sign):
#     if bad_sign == 0:
#         return 0
#     if bad_sign == len(diffs) - 1:
#         return -1
#     prev_d, bad_d, next_d = diffs[bad_sign - 1:bad_sign + 2]
#     prev_abs = abs(prev_d + bad_d)
#     next_abs = abs(bad_d + next_d)
#     if 0 < prev_abs < next_abs:  # +prev_d is better, del left end to mitigate the difference
#         return -1
#     return 0
#
#
# def process_line_part_2(numbers):
#     safeness, diffs, already_removed = process_signs(numbers)
#     # print(safeness, diffs, already_removed)
#
#     if safeness is not None:
#         return safeness
#
#     abs_d = [abs(d) for d in diffs]
#     too_big = [d for d in abs_d if d > 3]
#     # return 1-bool(len(too_big))
#
#     if not len(too_big):
#         return 1
#     if already_removed or len(too_big) > 1:
#         return 0
#     too_big_idx = abs_d.index(too_big[0])
#     return int(too_big_idx in {0, len(abs_d)-1})  # if first or last, removing will help, otherwise no
#
#     # abs_d = remove_at_index(abs_d, too_big_idx)
#
#     # return int(len([d for d in abs_d if d > 3]))
#
#     # if len(too_big) > (1 - int(already_removed)):
#     #     return 0
#     # return 1


def process_line_part_2_naive(numbers):
    safeness = process_line_part_1(numbers)
    if safeness == 1:
        return 1

    # try del each num
    for i in range(len(numbers)):
        safe_after_del = process_line_part_1(remove_at_index(numbers, i))
        if safe_after_del == 1:
            return 1
    return 0


lines = load_lines()
s = 0
for line in lines:
    numbers = [int(i) for i in line.split()]
    # number = process_line_part_1(numbers)
    # number = process_line_part_2(numbers)
    number = process_line_part_2_naive(numbers)
    # print(number, line)
    s += number

print(s)
