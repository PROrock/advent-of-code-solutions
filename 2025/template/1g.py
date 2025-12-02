from utils.grid_utils import DIRS_CLOCKWISE, DIR_TO_VECT, elem_at_pos, find_one_in_grid, inbounds, PrioritizedItem, \
    Vect, load_grid_str


def load_grid():
    file = "./1.in"
    # file = "./2.in"
    return load_grid_str(file)



grid = load_grid()
height = len(grid)
width = len(grid[0])

def solve():
    s = 0

    return s

print(solve())
