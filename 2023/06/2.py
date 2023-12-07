import sys

def read_line():
    line = sys.stdin.readline().rstrip("\r\n")
    string_number = "".join(line.split(":")[1].split())
    return int(string_number)


t = read_line()
dist_record = read_line()
print(t)
print(dist_record)


def n_ways_over_record(t, s):
    # s = v*t
    dists = [p * (t - p) for p in range(1, t)]
    return len([d for d in dists if d > s])

print(n_ways_over_record(t, dist_record))
