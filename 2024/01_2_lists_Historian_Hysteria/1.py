from collections import Counter
from pathlib import Path


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


lines = load_lines()
left, right = [], []
for line in lines:
    first, second = [int(i) for i in line.split()]
    left.append(first)
    right.append(second)

a = list(sorted(left))
b = list(sorted(right))
sum_diffs = sum([abs(i - j) for i, j in zip(a, b)])
print(sum_diffs)

# part 2
right_counter = Counter(right)

sum_sim = 0
for l in left:
    sim = l * right_counter.get(l, 0)
    sum_sim += sim
print(sum_sim)