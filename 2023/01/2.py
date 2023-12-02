import re
import string
import sys
from itertools import dropwhile


def reverse(s: str) -> str:
    return s[::-1]


def get_first_digit(line, pattern, mapping):
    line_subbed = pattern.sub(lambda m: mapping.get(m.group(0)), line, count=1)
    return int(next(dropwhile(lambda x: x not in string.digits, line_subbed)))


WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
WORD_TO_IDX = {word: str(i+1) for i, word in enumerate(WORDS)}
WORD_REV_TO_IDX = {reverse(word): str(i + 1) for i, word in enumerate(WORDS)}
PATTERN = re.compile(f"({'|'.join(WORDS)})")
PATTERN_REV = re.compile(f"({reverse('|'.join(WORDS))})")

s = 0
while True:
    line = sys.stdin.readline().rstrip("\r\n")
    if not line:
        break

    first = get_first_digit(line, PATTERN, WORD_TO_IDX)
    last = get_first_digit(reverse(line), PATTERN_REV, WORD_REV_TO_IDX)
    number = 10 * first + last
    # print(number)
    s += number

print(s)
