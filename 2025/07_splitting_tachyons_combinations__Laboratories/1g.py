from utils.grid_utils import elem_at_pos, Vect, load_grid_str


def load_grid():
    # file = "./1.in"
    file = "./2.in"
    return load_grid_str(file)



grid = load_grid()
height = len(grid)
width = len(grid[0])

def is_inbounds(x):
    return 0 <= x <= width


def solve():
    s = 0

    first_line = grid[0]
    beams = {first_line.index("S")}

    for y in range(1, len(grid)):
        next_beams = set()
        for b in beams:
            match elem_at_pos(grid, Vect(b, y)):
                case ".":
                    next_beams.add(b)
                case "^":
                    s+=1
                    for i in [-1, 1]:
                        if is_inbounds(b+i):
                            next_beams.add(b+i)
        beams = next_beams

    return s

print(solve())
