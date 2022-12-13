# --- Day 12: Hill Climbing Algorithm ---
import copy
import re


def get_grid(filepath):
    start_coords = []
    grid = []
    ord_a = ord('a')
    start_coord = None
    end_coord = None
    with open(filepath) as f:
        for line in f:
            s = line.find("S")
            e = line.find("E")
            if s >= 0:
                start_coord = (len(grid), s)
                line = line.replace("S", 'a')
            if e >= 0:
                end_coord = (len(grid), e)
                line = line.replace("E", "z")

            start_coords.extend([(len(grid), x.start()) for x in re.finditer("a", line)])
            grid.append([ord(c) - ord_a for c in line.rstrip()])
    return grid, start_coord, end_coord, start_coords

#  01234567
#0 Sabqponm
#1 abcryxxl
#2 accszExk
#3 acctuvwj
#4 abdefghi


def get_quickest_path_non_rec(grid, start_coord, end_coord):
    # Find smallest path in a breadth first search
    # So put lowest levels firsts, so all possibilities are stored.
    # The first time  that the source node is reached must be the shortest, because all paths are in
    # the list, according to depteness lebels, so all remaining items must take longer.
    # store all nodes from higher levels in explored (because we explore n+1 for all n-depth nodes),
    # so all repetitions of such nodes must be loops.
    explored = []
    other_paths_to_try = [[[end_coord], -1]]
    while len(other_paths_to_try) > 0:
        [visited, current_score] = other_paths_to_try.pop(0)
        # go from end to start, find possible ways
        end_coord = visited[-1]
        current_score += 1
        if end_coord not in explored:
            neighbours = []
            for (x, y) in [(end_coord[0]-1, end_coord[1]),
                            (end_coord[0]+1, end_coord[1]),
                            (end_coord[0], end_coord[1]+1),
                            (end_coord[0], end_coord[1]-1)]:
                if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and (x, y) not in visited \
                        and grid[x][y] >= grid[end_coord[0]][end_coord[1]]-1:
                    # can go on to current_coord, so being at most 1 height smaller
                    neighbours.append((x,y))
            if start_coord in neighbours:
                return current_score + 1
            else:
                for position in neighbours:
                    visited = list(visited)
                    visited.append(position)
                    other_paths_to_try.append([visited, current_score])
            explored.append(end_coord)
    return -1


def solve_part_1(grid, start_coord, end_coord):
    n= get_quickest_path_non_rec(grid, start_coord, end_coord)
    return n


def get_quickest_path_non_rec_arbitrary_start(grid, end_coord):
    # Find smallest path in a breadth first search
    # So put lowest levels firsts, so all possibilities are stored.
    # The first time  that the source node is reached must be the shortest, because all paths are in
    # the list, according to depteness lebels, so all remaining items must take longer.
    # store all nodes from higher levels in explored (because we explore n+1 for all n-depth nodes),
    # so all repetitions of such nodes must be loops.
    explored = []
    other_paths_to_try = [[[end_coord], -1]]
    while len(other_paths_to_try) > 0:
        [visited, current_score] = other_paths_to_try.pop(0)
        # go from end to start, find possible ways
        end_coord = visited[-1]
        current_score += 1
        if end_coord not in explored:
            neighbours = []
            for (x, y) in [(end_coord[0]-1, end_coord[1]),
                            (end_coord[0]+1, end_coord[1]),
                            (end_coord[0], end_coord[1]+1),
                            (end_coord[0], end_coord[1]-1)]:
                if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and (x, y) not in visited \
                        and grid[x][y] >= grid[end_coord[0]][end_coord[1]]-1:
                    # can go on to current_coord, so being at most 1 height smaller
                    neighbours.append((x,y))
            for position in neighbours:
                if grid[position[0]][position[1]] == 0:
                    # "so there is a a and we can stop"
                    return current_score + 1
                visited = list(visited)
                visited.append(position)
                other_paths_to_try.append([visited, current_score])
            explored.append(end_coord)
    return -1


def solve_part_2(grid, end_coord):
    n = get_quickest_path_non_rec_arbitrary_start(grid, end_coord)
    return n


print("Part 1", "\n")
g, s, e, _ = get_grid("test_data.txt")
print("test:", solve_part_1(g, s, e), "\n")
g, s, e, _ = get_grid("data.txt")
print("data:", solve_part_1(g, s, e), "\n")

print("\nPart 2")
# list of all starting locations not needed in the end
g, s, e, _ = get_grid("test_data.txt")
print("data:", solve_part_2(g, e))
g, s, e, _ = get_grid("data.txt")
print("data:", solve_part_2(g, e))