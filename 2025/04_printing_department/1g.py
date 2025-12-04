from utils.grid_utils import elem_at_pos, inbounds, Vect, load_grid_str, EIGHT_NEIGHBOURHOOD, print_grid


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

    for y in range(height):
        for x in range(width):

            if elem_at_pos(grid, Vect(x,y)) == "@" and can_access_pos(x, y):
                s+=1
                print(x,y, s)

    return s


def can_access_pos(x, y):
    v = Vect(x, y)
    # 8-neighbourhood
    rolls = 0

    for dv in EIGHT_NEIGHBOURHOOD:
        new_pos = v+dv
        if inbounds(grid, new_pos) and elem_at_pos(grid, new_pos) == "@":
            rolls += 1

    return rolls < 4



print(solve())
