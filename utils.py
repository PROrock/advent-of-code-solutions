def replace_in_str_from(s, replacement, idx):
    return f"{s[:idx]}{replacement}{s[idx + len(replacement):]}"
