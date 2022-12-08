# --- Day 8: Treetop Tree House ---
import copy

import numpy as np


def get_trees(filepath):
    trees = []
    with open(filepath) as f:
        for line in f:
            trees.append([int(s) for s in line.rstrip()])
    return trees

def solve_p1(trees):
    width = len(trees[0])
    isvisible = np.zeros((len(trees), width))
    # outside is always visible
    isvisible[0] = [1]*width
    isvisible[-1] = [1]*width
    for i in range(1, len(trees)):
        isvisible[i][0] = 1
        isvisible[i][-1] = 1
    #from top
    c = copy.deepcopy(trees[0])
    for i in range(1, width):
        for j in range(1, len(trees)-1):
            if trees[j][i] > c[i]:
                # tree is higher, so visible
                isvisible[j][i] = 1
                c[i] = trees[j][i]
            if c[i] == 9:
                # if a nine is reached, stop because nothing can be seen anymore
                break
    # from bottom
    c = copy.deepcopy(trees[-1])
    for i in range(1, width):
        for j in range(len(trees)-1, 0, -1):
            if trees[j][i] > c[i]:
                # tree is higher, so visible
                isvisible[j][i] = 1
                c[i] = trees[j][i]
            if c[i] == 9:
                # if a nine is reached, stop because nothing can be seen anymore
                break

    # from right
    c = [row[-1] for row in trees]
    for j in range(1, len(trees)-1):
        for i in range(width-2, 0, -1):
            if trees[j][i] > c[j]:
                # tree is higher, so visible
                isvisible[j][i] = 1
                c[j] = trees[j][i]
            if c[j] == 9:
                # if a nine is reached, stop because nothing can be seen anymore
                break
    # from left
    c = [row[0] for row in trees]
    for j in range(1, len(trees) - 1):
        for i in range( 1, width - 1):
            if trees[j][i] > c[j]:
                # tree is higher, so visible
                isvisible[j][i]= 1
                c[j] = trees[j][i]
            if c[j] == 9:
                # if a nine is reached, stop because nothing can be seen anymore
                break

    # return number of visible trees
    return sum([sum(row) for row in isvisible])



def solve_p2(trees):
    width = len(trees[0])
    #from top
    top = np.zeros((len(trees), width))
    for i in range(0, width):
        prev = None
        for j in range(0, len(trees)):
            if prev is None:
                # cannot see any trees
                top[j][i] = 0
            elif trees[j][i] <= prev:
                # can only see neighbor
                top[j][i] = 1
            else:
                # tree is bigger than previous: can also see how far that tree sees + then check whether we even see over the consecutive one
                top[j][i] = 1
                prev_biggest_i = 1
                while j - prev_biggest_i > 0 and trees[j][i] >  trees[j-prev_biggest_i][i]:
                    top[j][i] += top[j-prev_biggest_i][i]
                    prev_biggest_i += int(top[j-prev_biggest_i][i])
            prev = trees[j][i]

    # from bottom
    bottom = np.zeros((len(trees), width))
    for i in range(0, width):
        prev = None
        for j in range(len(trees)-1, -1, -1):
            if prev is None:
                # cannot see any trees
                bottom[j][i] = 0
            elif trees[j][i] <= prev:
                # can only see neighbor
                bottom[j][i] = 1
            else:
                # tree is bigger than previous: can also see how far that tree sees + then check whether we even see over the consecutive one
                bottom[j][i] = 1
                prev_biggest_i = 1
                while j + prev_biggest_i < len(trees) - 1 and trees[j][i] > trees[j + prev_biggest_i][i]:
                    bottom[j][i] += bottom[j + prev_biggest_i][i]
                    prev_biggest_i += int(bottom[j + prev_biggest_i][i])
            prev = trees[j][i]

    # from right
    right = np.zeros((len(trees), width))
    for j in range(0, len(trees)):
        prev = None
        for i in range(width - 1, -1, -1):
            if prev is None:
                # cannot see any trees
                right[j][i] = 0
            elif trees[j][i] <= prev:
                # can only see neighbor
                right[j][i] = 1
            else:
                # tree is bigger than previous: can also see how far that tree sees + then check whether we even see over the consecutive one
                right[j][i] = 1
                prev_biggest_i = 1
                while i + prev_biggest_i < width - 1 and trees[j][i] > trees[j][i + prev_biggest_i]:
                    right[j][i] += right[j][i + prev_biggest_i]
                    prev_biggest_i += int(right[j][i + prev_biggest_i])
            prev = trees[j][i]


    # from left
    left = np.zeros((len(trees), width))
    for j in range(0, len(trees)):
        prev = None
        for i in range(0, width):
            if prev is None:
                # cannot see any trees
                left[j][i] = 0
            elif trees[j][i] <= prev:
                # can only see neighbor
                left[j][i] = 1
            else:
                # tree is bigger than previous: can also see how far that tree sees + then check whether we even see over the consecutive one
                left[j][i] = 1
                prev_biggest_i = 1
                while i - prev_biggest_i > 0 and trees[j][i] > trees[j][i - prev_biggest_i]:
                    left[j][i] += left[j][i - prev_biggest_i]
                    prev_biggest_i += int(left[j][i - prev_biggest_i])
            prev = trees[j][i]

    # return number of visible trees
    result = np.ones((len(trees), width))
    for i in range(0, width):
        for j in range(0, len(trees)):
            result[i][j] = top[i][j] * bottom[i][j] * left[i][j] * right[i][j]

    return max([max(row) for row in result])

print("Part 1")
print('test', print(solve_p1(get_trees("test_data.txt"))))
print('data', print(solve_p1(get_trees("data.txt"))))

print("Part 1")
print('test', print(solve_p2(get_trees("test_data.txt"))))
print('data', print(solve_p2(get_trees("data.txt"))))
