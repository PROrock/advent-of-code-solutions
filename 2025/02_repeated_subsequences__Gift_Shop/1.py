from pathlib import Path


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


def is_invalid(curr):
    s = str(curr)
    if len(s)%2!=0:
        return False

    mid = len(s)//2
    return s[:mid] == s[mid:]

def is_invalid_part2(curr):
    s = str(curr)
    mid = len(s)//2

    for pattern_size in range(1, mid+1):
        if 2*pattern_size > len(s):
            break

        if len(s) % pattern_size != 0:
            continue

        n_repeats = len(s)//pattern_size
        same = (s[:pattern_size] * n_repeats) == s
        if same:
            return True

    return False

def process_line(ids):
    result = []
    low, high = [int(i) for i in ids]

    curr = low
    while curr <= high:
        # XXXXXXXXXXXX: swap here part 1 and 2
        # if is_invalid(curr):
        if is_invalid_part2(curr):
            result.append(curr)
        # print(curr, result)
        curr += 1
    return result


lines = load_lines()
s = []
for line in lines:
    for id_range in line.split(","):
        ids = id_range.split("-")
        invalids = process_line(ids)

        # print(ids, invalids)
        s.extend(invalids)

print(sum(s))

# print(is_invalid(55))
# print(is_invalid(12))
