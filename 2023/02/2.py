import functools
import re
import sys
from typing import NamedTuple


class Set(NamedTuple):
    red: int = 0
    green: int = 0
    blue: int = 0

    @staticmethod
    def from_str(set_str):
        return Set._make([Set.parse_color(set_str, color) for color in Set._fields])

    @staticmethod
    def parse_color(set_str, color):
        return int(matches[0]) if (matches := re.findall(fr"(\d+) {color}", set_str)) else 0

    def max_colors(self, other_set):
        return Set._make([max(self_color, other_color) for self_color, other_color in zip(self, other_set)])

    def power(self):
        return functools.reduce(lambda x, y: x * y, self)


THRESH_SET = Set(12, 13, 14)
s = 0


def parse_line(line):
    game_str, sets_str = line.split(": ")
    game_id = int(re.fullmatch(r"Game (\d+)", game_str).group(1))
    sets = [Set.from_str(set_str) for set_str in sets_str.split("; ")]
    return game_id, sets


while True:
    line=sys.stdin.readline().rstrip("\r\n")
    if not line:
        break

    game_id, sets = parse_line(line)
    max_set = functools.reduce(Set.max_colors, sets)
    s += max_set.power()

print(s)
