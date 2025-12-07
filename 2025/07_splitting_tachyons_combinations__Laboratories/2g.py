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

# d = []
def solve():
    # global d
    splits = 0

    first_line = grid[0]
    beams = {first_line.index("S"): 1}
    # debug grid
    # d = [first_line]

    for y in range(1, len(grid)):
        # d.append(list(grid[y]))
        # print(f"{y:2}", beams)
        next_beams = {}
        for b, n_combs in beams.items():
            match elem_at_pos(grid, Vect(b, y)):
                case ".":
                    next_beams[b]=next_beams.get(b, 0) + n_combs
                case "^":
                    splits+=1
                    for i in [-1, 1]:
                        if is_inbounds(b+i):  #not even in the data!
                            next_beams[b+i]=next_beams.get(b+i, 0) + n_combs
        beams = next_beams

        # for b, n_combs in beams.items():
        #     d[y][b] = n_combs%10

    return splits, sum(beams.values())

print(solve())

# print_grid(d)