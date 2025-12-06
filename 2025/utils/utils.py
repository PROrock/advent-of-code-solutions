# ideas to add:
#  class Trie from 2024 day 19 (how to subclass dict?)

import re

INT_STR = "(-?\d+)"
INT_PAT = re.compile(INT_STR)

def replace_in_str_from(s, idx, replacement):
    return f"{s[:idx]}{replacement}{s[idx + len(replacement):]}"

def split_lines_on_empty_line_in_2(lines):
    empty_line_idx = lines.index("")
    a = lines[:empty_line_idx]
    b = lines[empty_line_idx+1:]
    return a,b

def gen_split_lines_by_empty_lines(lines):
    start_idx = 0
    for i, line in enumerate(lines):
        if line == "":
            yield lines[start_idx:i]
            start_idx=i+1
    yield lines[start_idx:i+1]

# delete this after 2026 if not used
def split_iterable_by_sep(iterable, sep):
    prev_i = 0
    for i,c in enumerate(iterable):
        if c==sep:
            yield iterable[prev_i:i + 1]
            prev_i = i+1

    yield iterable[prev_i:i+1]  # commented, so I don't have to forget last yield (because A is always the last letter)

def split_iterable_by_sep_v2(iterable, sep, include_sep=False):
    prev_i = 0
    for i,c in enumerate(iterable):
        if c==sep:
            end_index_offset = 1 if include_sep else 0
            yield iterable[prev_i:i + end_index_offset]
            prev_i = i+1

    yield iterable[prev_i:i+include_sep]


def ints(s):
    return [int(i) for i in INT_PAT.findall(s)]

def argmax(iterable):
    return max(enumerate(iterable), key=lambda t:t[1])[0]
def argmin(iterable):
    return min(enumerate(iterable), key=lambda t:t[1])[0]
