from collections import Counter
from operator import itemgetter
from pathlib import Path

from utils.grid_utils import Vect3d
from utils.utils import ints, multiply


def load_lines():
    # file, n_unions = "./1.in", 10
    file, n_unions = "./2.in", 1000
    return Path(file).read_text().splitlines(), n_unions


lines, n_unions = load_lines()
nodes = [Vect3d(*ints(line)) for line in lines]
# pprint(dict(enumerate(nodes)))

distances = {} # dist -> m, n
for m, mv in enumerate(nodes):
    for n, nv in enumerate(nodes):
        if n <= m:
            continue

        distances[mv.l2_dist(nv)] = (m, n)

assert len(distances) == (len(nodes)**2-len(nodes))/2
# pprint(distances)

# idea: dict would be better -> slow finding of which component is particular node (maybe add to speed up union?)
components = list(range(len(nodes)))
c = 0
# or [:n_unions] instead of c
for d, pair in sorted(distances.items(), key=itemgetter(0)):
    m, n = pair
    c += 1
    # print(d, m, n, components)
    if components[m] != components[n]:
        # union
        comp_to_del = components[n]
        for i in range(len(components)):
            if components[i] == comp_to_del:
                components[i] = components[m]
    # print(c, m, n)
    # print(c, m, n, nodes[m], nodes[n], nodes[m].l2_dist(nodes[n]))
    print(c, m, n, nodes[m].l2_dist(nodes[n]))
    if c == n_unions:
        break
# print(components)

# 3 largest circuits
sizes = Counter(components)
# print(len(sizes), sizes)
top3 = sizes.most_common(3)
print(top3)
print(multiply([size for _, size in top3]))
