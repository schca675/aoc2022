# --- Day 14: Regolith Reservoir ---

#   4     5  5
#   9     0  0
#x\y4     0  3
# 0 ......+...
# 1 ..........
# 2 ..........
# 3 ..........
# 4 ....#...##
# 5 ....#...#.
# 6 ..###...#.
# 7 ........#.
# 8 ........#.
# 9 #########.
#
#
from numpy.core._multiarray_umath import sign


def get_grid_from_file(filepath):
    list_of_rock_lines = []
    min_x = 0# because start position is 0,500 we need at least a x of 0
    min_y = 10000000
    max_x = 0
    max_y = 0
    with open(filepath) as f:
        for line in f:
            this_line = [(int(x.split(',')[1]), int(x.split(',')[0])) for x in line.rstrip().split(" -> ")]
            list_of_rock_lines.append(this_line)
            min_x = min(min([x[0] for x in this_line]), min_x)
            min_y = min(min([x[1] for x in this_line]), min_y)
            max_x = max(max([x[0] for x in this_line]), max_x)
            max_y = max(max([x[1] for x in this_line]), max_y)
    # make grid and draw rocks
    grid = [list(['.']*(1+(max_y - min_y))) for _ in range(0, 1 + (max_x - min_x))] # both bounds included so +1
    for rocks in list_of_rock_lines:
        # make numbers relative to grid
        rocks = [(rock[0]-min_x, rock[1]-min_y) for rock in rocks]
        for i in range(0, len(rocks)-1):
            (sx, sy) = rocks[i]
            (ex, ey) = rocks[i+1]
            # start rock
            # grid[sx][sy] = "#"
            sign_x = sign(ex - sx)
            for diff in range(0, abs(sx-ex)):
                grid[sx + sign_x * diff][sy] = "#"
            sign_y = sign(ey - sy)
            for diff in range(0, abs(sy - ey)):
                grid[sx][sy+sign_y*diff] ="#"
            grid[ex][ey] = "#"
    start_pos = (0-min_x, 500-min_y)
    # grid[start_pos[0]][start_pos[1]] = "+"
    return grid, start_pos

def print_grid(grid):
    formatstring = "{:>1}"*len(grid[0])
    for line in grid:
        print(formatstring.format(*line))

def solve_part_1(grid, s):
    scounts = 0
    prev = [s]
    # nextp = s
    terminate = False
    while not terminate and len(prev) > 0:
        (x,y) = prev[-1]

        # fall down?
        if grid[x+1][y] == ".":
            # can fall here, because no opstacle
            prev.append((x+1,y))
            continue
        # if the above is not true, then cannot fall straight down because either # or o is blocking
        # manual inspection of grid shows, that we cannot fall through the bottom (there always will be stone)

        # fall left down
        # check if it falls out of the box
        if y-1 < 0:
            # so all next sands also fall out of the box, dont stop anymore
            terminate = True
            break
        if grid[x+1][y-1] == ".":
            # can fall here, because no opstacle
            prev.append((x+1, y-1))
            continue

        # fall right down
        # check if it falls out of the box
        if y + 1 >= len(grid[0]):
            # so all next sands also fall out of the box, dont stop anymore
            terminate = True
            break
        if grid[x + 1][y + 1] == ".":
            # can fall here, because no opstacle
            prev.append((x + 1, y + 1))
            continue

        # if we reach here: didnt fall out of the box AND cannot jump down --> ergo the sand rests here
        scounts +=1
        grid[x][y] = "o"
        prev.pop()
        # for debugging:
        # print_grid(grid)
        # print("---------------------------- -", scounts)
    return scounts



def solve_part_2(grid, s):
    # the grid has an extra 2 lines: one where sand can fall and one full of rocks
    grid.append(['.']*len(grid[0]))
    grid.append(['#']*len(grid[0]))
    # the grid can extend to the left and the right -> update grid as needed
    # sand falling
    scounts = 0
    prev = [s]
    # nextp = s
    terminate = False
    while not terminate and len(prev) > 0:
        (x,y) = prev[-1]

        # fall down? --> will never fall out of grid this way
        if grid[x+1][y] == ".":
            # can fall here, because no opstacle
            prev.append((x+1,y))
            continue
        # if the above is not true, then cannot fall straight down because either # or o is blocking
        # manual inspection of grid shows, that we cannot fall through the bottom (there always will be stone)

        # fall left down
        # check if it falls out of the box
        if y-1 < 0:
            # sand would fall out of the box --> make grid larger at the front
            for line in grid:
                line.insert(0,".")
            # last line is the bottom, so always needs to have a rock
            grid[-1][0] = "#"
            # position of all coordinates changes --> update prev list; previous (0,0) is now (0,1)
            prev = [(p[0], p[1]+1) for p in prev]
            continue # start over with extended grid
        if grid[x+1][y-1] == ".":
            # can fall here, because no opstacle
            prev.append((x+1, y-1))
            continue

        # fall right down
        # check if it falls out of the box
        if y + 1 >= len(grid[0]):
            # sand would fall out of the box --> make grid larger at the front
            for line in grid:
                line.append(".")
            # last line is the bottom, so always needs to have a rock
            grid[-1][-1] = "#"
            continue  # start over with extended grid
        if grid[x + 1][y + 1] == ".":
            # can fall here, because no opstacle
            prev.append((x + 1, y + 1))
            continue

        # if we reach here: didnt fall out of the box AND cannot jump down --> ergo the sand rests here
        scounts +=1
        grid[x][y] = "o"
        prev.pop()
        # for debugging:
        # print_grid(grid)
        # print("---------------------------- -", scounts)
    return scounts



print("Part 1", "\n")
g, s = get_grid_from_file("test_data.txt")
print_grid(g)
print("test:", solve_part_1(g, s), "\n")
g, s = get_grid_from_file("data.txt")
# print_grid(g)
print("data:", solve_part_1(g, s), "\n")

print("\nPart 2")
g, s = get_grid_from_file("test_data.txt")
print("test:", solve_part_2(g, s), "\n")
g, s = get_grid_from_file("data.txt")
# print_grid(g)
print("data:", solve_part_2(g, s), "\n")
