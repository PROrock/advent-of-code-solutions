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

    def is_any_color_over(self, other_set):
        return any(self_color > other_color for self_color, other_color in zip(self, other_set))


THRESH_SET = Set(12, 13, 14)
s = 0

def parse_line(line):
    game_str, sets_str = line.split(": ")
    game_id = int(re.fullmatch(r"Game (\d+)", game_str).group(1))
    sets = [Set.from_str(set_str) for set_str in sets_str.split("; ")]
    return game_id, sets


while True:
    line = sys.stdin.readline().rstrip("\r\n")
    if not line:
        break

    game_id, sets = parse_line(line)
    if all(not set.is_any_color_over(THRESH_SET) for set in sets):
        s += game_id

print(s)
