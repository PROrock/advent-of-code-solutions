from pathlib import Path

from utils.grid_utils import Vect
from utils.utils import ints


def load_lines():
    # file = "./1.in"
    file = "./2.in"
    return Path(file).read_text().splitlines()


lines = load_lines()
points = [Vect(*ints(line)) for line in lines]
print(points)

m = max([(abs(m.x-n.x)+1)*(abs(m.y - n.y)+1) for m in points for n in points])
print(m)
