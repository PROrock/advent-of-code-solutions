# ideas to add:
#  class Trie from 2024 day 19 (how to subclass dict?)

import re

INT_STR = "(-?\d+)"
INT_PAT = re.compile(INT_STR)

def replace_in_str_from(s, idx, replacement):
    return f"{s[:idx]}{replacement}{s[idx + len(replacement):]}"

def split_lines_on_empty_line(lines):
    empty_line_idx = lines.index("")
    a = lines[:empty_line_idx]
    b = lines[empty_line_idx+1:]
    return a,b

def ints(s):
    return [int(i) for i in INT_PAT.findall(s)]

def argmax(iterable):
    return max(enumerate(iterable), key=lambda t:t[1])[0]
def argmin(iterable):
    return min(enumerate(iterable), key=lambda t:t[1])[0]
