from pathlib import Path


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


def print_grid(grid):
    print("GRID")
    for line in grid:
        print(line)
    print("GRID END")


def split_to_patterns(lines):
    pattern = []
    for line in lines:
        if line:
            pattern.append(line)
        else:
            yield pattern
            pattern = []
    yield pattern


def is_reflecting_by_y_with_smudge(pattern, y):
    sum_diffs = 0
    for i,j in zip(range(y, -1, -1), range(y+1, len(pattern))):
        # print(i+1, j+1)
        # print(i, j)
        n_diffs = sum([c1 != c2 for c1, c2 in zip(pattern[i], pattern[j])])
        sum_diffs += n_diffs
        if sum_diffs > 1:
            return False
    return sum_diffs == 1

def summarize_y_pattern(pattern):
    for y in range(len(pattern)-1):
        if is_reflecting_by_y_with_smudge(pattern, y):
            return y+1
    return None


def summarize_pattern(pattern):
    if y_pattern_num := summarize_y_pattern(pattern):
        return 100*y_pattern_num
    transposed_pattern = list(zip(*pattern))
    return summarize_y_pattern(transposed_pattern)


lines = load_lines()
# print_grid(lines)

patterns = list(split_to_patterns(lines))
# print(f"{len(patterns)=}")


s = 0
for pattern in patterns:
    number = summarize_pattern(pattern)
    # print(number)
    s += number

print(s)
