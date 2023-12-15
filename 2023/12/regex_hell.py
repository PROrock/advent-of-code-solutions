import re
BROKEN = "#"
record = "?###????"
first_group = 3
end_of_window = len(record)

pattern = f"(?=([#?]{{{first_group}}})(?!#))"
candidate_positions = list(re.finditer(pattern, record[:end_of_window]))
print(record, pattern, first_group, end_of_window, candidate_positions)
for candidate in candidate_positions:
    if candidate.start(1) > 0 and record[candidate.start(1)-1] == BROKEN:
        print(f"invalid candidate! {candidate} {candidate.start()},{candidate.start(1)}. Groups: {candidate.groups()}. "
              f"Char {record[candidate.start(1)-1]} is BROKEN. in {record[candidate.start(1)-1:candidate.end(1)+1]}")
        continue
    print(candidate, candidate.end(), candidate.end(1))
    # yield from generate_all_combinations_list4(record[candidate.end(1)+1:], groups[1:])
