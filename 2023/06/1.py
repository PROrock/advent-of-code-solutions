import sys

times = [int(i) for i in sys.stdin.readline().rstrip("\r\n").split(":")[1].split()]
distances = [int(i) for i in sys.stdin.readline().rstrip("\r\n").split(":")[1].split()]


def n_ways_over_record(t, s):
    # s = v*t
    dists = [p * (t - p) for p in range(1, t)]
    return len([d for d in dists if d > s])


s = 1
for t, dist_record in zip(times, distances):
    num = n_ways_over_record(t, dist_record)
    print(t, dist_record, num)
    s *= num
print(s)
