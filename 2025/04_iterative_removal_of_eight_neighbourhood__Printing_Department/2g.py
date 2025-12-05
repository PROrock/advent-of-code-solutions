from utils.grid_utils import elem_at_pos, inbounds, Vect, load_grid_str, EIGHT_NEIGHBOURHOOD, print_grid, \
    set_elem_at_pos_str


def load_grid():
    # file = "./1.in"
    file = "./2.in"
    return load_grid_str(file)


grid = load_grid()
height = len(grid)
width = len(grid[0])

print_grid(grid)

def solve():
    s = 0
    while True:
        n_removed = remove_from_grid(s)
        s += n_removed
        if n_removed == 0:
            break
    return s


def remove_from_grid(s):
    removed = 0
    for y in range(height):
        for x in range(width):

            pos = Vect(x, y)
            if elem_at_pos(grid, pos) == "@" and can_access_pos(pos):
                removed += 1
                set_elem_at_pos_str(grid, pos, ".")
                # print(x, y, removed)
    return removed


def can_access_pos(v: Vect):
    rolls = 0
    for dv in EIGHT_NEIGHBOURHOOD:
        new_pos = v+dv
        if inbounds(grid, new_pos) and elem_at_pos(grid, new_pos) == "@":
            rolls += 1

    return rolls < 4


print(solve())
