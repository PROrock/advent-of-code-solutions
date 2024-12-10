from dataclasses import dataclass
from pathlib import Path


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


def process_line(line):
    if len(line)%2==0:
        print("even length!")
        line = line[:-1]
    numbers = [int(i) for i in line]
    lower_idx = 1  # skip file zero
    mem_pos = numbers[0]
    upper_idx = len(numbers) - 1
    upper_count = numbers[upper_idx]
    cs = 0

    gap_len = numbers[lower_idx]
    while lower_idx < upper_idx:
        seg_len = min(upper_count, gap_len)
        cs += cs_for_id_pos_len(upper_idx, mem_pos, seg_len)
        # print(lower_idx, upper_idx, mem_pos, str(upper_idx//2)*seg_len)

        upper_count -= seg_len
        gap_len -= seg_len
        mem_pos += seg_len
        if upper_count == 0:
            upper_idx -= 2
            upper_count = numbers[upper_idx]
        if gap_len == 0:
            lower_idx += 1

            # count low file id
            seg_len = upper_count if lower_idx >= upper_idx else numbers[lower_idx]
            cs += cs_for_id_pos_len(lower_idx, mem_pos, seg_len)
            # print(lower_idx, upper_idx, mem_pos, str(lower_idx//2)*seg_len)
            mem_pos += seg_len
            lower_idx += 1
            gap_len = numbers[lower_idx]
    return cs

@dataclass
class Segment:
    fid: int  # -1 is gap
    pos: int
    len: int


def find_gap_idx(gaps, f):
    for i, gap in enumerate(gaps):
        if gap.len >= f.len and gap.pos < f.pos:
            return i
    return -1


def process_line_b(line):
    if len(line)%2==0:
        print("even length!")
        line = line[:-1]
    numbers = [int(i) for i in line]

    files = []
    gaps = []
    pos = 0
    for num_idx, l in enumerate(numbers):
        if num_idx % 2 == 0:
            files.append(Segment(num_idx // 2, pos, l))
        else:
            gaps.append(Segment(-1, pos, l))
        pos += l

    # fragment phase
    for f in reversed(files):
        gap_idx = find_gap_idx(gaps, f)
        if gap_idx >= 0:
            gap = gaps[gap_idx]
            f.pos = gap.pos
            gap.len-=f.len
            gap.pos+=f.len
            if gap.len == 0:
                del gaps[gap_idx]

    # print(sorted(files, key=lambda f: f.pos))
    cs = 0
    for f in files:
        cs+= f.fid * sum(range(f.pos, f.pos + f.len))
    return cs

def cs_for_id_pos_len(idx, pos, seg_len):
    fid = idx//2
    return fid * sum(range(pos, pos + seg_len))


lines = load_lines()
# print(process_line(lines[0]))
print(process_line_b(lines[0]))
