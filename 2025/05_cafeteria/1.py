import dataclasses
from pathlib import Path

from utils.utils import gen_split_lines_by_empty_lines


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()

@dataclasses.dataclass
class Range:
    min: int
    max: int

def process_line(line):
    i = int(line)
    for r in ranges:
        if  r.min <= i <= r.max:
            return 1
    return 0


lines = load_lines()
ranges_raw, ingr = list(gen_split_lines_by_empty_lines(lines))
ranges = [Range(*[int(i) for i in r.split("-")]) for r in ranges_raw]
ranges = sorted(ranges, key=lambda r: (r.min, r.max))
print("sorted")
# print(ranges)

def all_fresh_ids():
    results = [ranges[0]]
    for r in ranges[1:]:
        last_result = results[-1]
        # print(r, last_result, r.min, last_result.max)
        if r.min <= last_result.max:
            last_result.max = max(last_result.max, r.max)
            # print(f"updated {last_result=}")
        else:
            results.append(r)
            # print(f"adding {r}")

    return results


results = all_fresh_ids()
# print(results)
print(sum([r.max - r.min + 1 for r in results]))

# # part 1
# s = 0
# for line in ingr:
#     number = process_line(line)
#     # print(number, line)
#     s += number
# print(s)
