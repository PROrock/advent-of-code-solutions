# ideas to add:
# a,b = split_parts_on_empty_line(s)
# nums = ints(s) (reads possibly negative integers in the string, splits, converts to int)

def replace_in_str_from(s, idx, replacement):
    return f"{s[:idx]}{replacement}{s[idx + len(replacement):]}"

