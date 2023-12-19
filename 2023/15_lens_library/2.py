import re
from pathlib import Path
from typing import NamedTuple

STEP_FORMAT = re.compile("(\w+)=(\d)")

class Lens(NamedTuple):
    label: str
    focal_len: int

def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


def hash_(step):
    h = 0
    for c in step:
        h = ((h+ord(c))*17)%256
    return h


lines = load_lines()


def parse_step():
    if match := STEP_FORMAT.fullmatch(step):
        label, focal_len = match.groups()
        focal_len = int(focal_len)
    else:
        if step[-1] == "-":
            label, focal_len = step[:-1], None
        else:
            print("BIG WARNING!")
    return label, focal_len

def get_lens_with_label(lenses, label):
    for i, lens in enumerate(lenses):
        if lens.label == label:
            return i, lens
    return None, None

hash_map = {}
for line in lines:
    for step in line.split(","):
        label, focal_len = parse_step()
        box = hash_(label)

        if focal_len is None:
            if box in hash_map:
                lenses = hash_map[box]
                lens_idx, lens = get_lens_with_label(lenses, label)
                # print(label, focal_len, box, "lens_idx", lens_idx, lens)
                if lens_idx is not None:
                    # lenses.remove(lens)
                    hash_map[box] = lenses[:lens_idx] + lenses[lens_idx+1:]
                # hash_map[box] = hash_map[box].remove(label)
        else:
            if box not in hash_map:
                hash_map[box] = []
            lenses = hash_map[box]
            lens_idx, lens = get_lens_with_label(lenses, label)
            new_lens = Lens(label, focal_len)
            if lens is None:
                lenses.append(new_lens)
            else:
                lenses[lens_idx] = new_lens

        # print(step, box, hash_map)

# print(hash_map)
# for k,v in hash_map.items():
#     print(k, ":", v)
# print()

s = 0
for box, lenses in hash_map.items():
    for lens_idx, lens in enumerate(lenses):
        number = (box+1) * (lens_idx+1) * lens.focal_len
        # print(lens, number)
        s += number

print(s)
