# --- Day 15: Beacon Exclusion Zone ---
import re
import textwrap
import time


def get_manhatten_distance(closest_beacon, sensor):
    return abs(closest_beacon[0] - sensor[0]) + abs(closest_beacon[1]-sensor[1])


def get_puzzle_input(filepath):
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    beacon_rad = dict()
    beacon_list = set()
    for line in open(filepath).read().split('\n'):
        match = re.findall(r'x=(-?\d+), y=(-?\d+)', line)
        [sensor, closest_beacon] = [(int(m[0]), int(m[1])) for m in match]
        beacon_list.add(closest_beacon)
        beacon_rad[sensor] = get_manhatten_distance(closest_beacon, sensor)
        min_x = min(min_x, min(sensor[0], closest_beacon[0]))
        min_y = min(min_y, min(sensor[1], closest_beacon[1]))
        max_x = max(max_x, max(sensor[0], closest_beacon[0]))
        max_y = max(max_y, max(sensor[1], closest_beacon[1]))

    return beacon_rad, (min_x, min_y), (max_x, max_y), beacon_list

def solve_p1(beacon_rad, min_pos, max_pos, beacon_list, row=10):
    sensors = list(beacon_rad.keys())
    sensors.sort(key = lambda x: x[1])
    reached_x_start_sorted = []
    reached_x_end = []
    reached_xses = set()
    nbr_occupied = 0
    for s in sensors:
        n_inline = 0
        # check manhatten distance from entire row
        d = abs(row - s[1])
        if d <= beacon_rad[s]:
            n_inline = 1+(beacon_rad[s]-d)*2
            new_set = set()
            for i in range(0,n_inline//2+1):
                new_set.add(s[0]+i)
                new_set.add(s[0]-i)
            nbr_occupied += n_inline - len(new_set.intersection(reached_xses))
            reached_xses = reached_xses.union(new_set)
        # have to see whether we are counting some double
        # check index of saved lines
        # index_first_match = next(
        #     (index for index, item in enumerate(reached_x_start_sorted) if item > s[0]),
        #     None
        # )
        # n_inline = n_inline - reached_x_end
        # if s[0] < reached_x_end[index_first_match]:
    # remove all beacons from count
    a = sum([1 for b in beacon_list if b[1] == row])
    b = sum([1 for s in sensors if s[1] == row])
    return nbr_occupied - a - b

def solve_p2(beacon_rad, min_pos, max_pos, beacon_list, pmin=0, pmax=4000000):
    " need sorted list of sensors according to what row they can reach maximally --> done on second line"
    sensors = list(beacon_rad.keys())
    sensors.sort(key=lambda x: x[1]-beacon_rad[x])
    # my = [(s[1] - d, s, d) for s, d in beacon_rad.items()]
    # my.sort()
    lines = {} # does not include end
    # #

    for s in sensors:
        # check if rows can be removed, because sensors ordered according to reach (from reaching low y indexes to higher)
        # for all rows in between the last reached and this reached:
        rows_before_this_one = [rowi for rowi in lines.keys() if rowi < s[1]-beacon_rad[s]]
        # check if row is completed and can be removed
        for rowi in rows_before_this_one:
            if len(lines[rowi]) == 1 and lines[rowi][0][0] <= pmin and lines[rowi][0][1] >= pmax:
                # only a single row that is all filled.
                lines.pop(rowi)
        # check manhatten distance from entire row
        # sensor reaches all lines up to -d to d:
        a = 0
        for row in range(max(0, s[1]-beacon_rad[s]), s[1]+beacon_rad[s]+1):
            d = abs(row - s[1])
            n_inline_besides = (1 + (beacon_rad[s] - d) * 2) // 2
            n_line = [s[0] - n_inline_besides, s[0] + n_inline_besides] # including bounds
            # check if row already in lines
            if row in lines.keys(): #
                # have already stored this row, add new sensor input:
                # check whether line is behind existing lines:
                row_wlines = lines[row]
                if n_line[0] >= row_wlines[-1][1]: # check last line and see if begin is behind that end
                    # --- a--b c---d x--y
                    # since it is stored, there is at least one line present (one item present in list)
                    # start of this line is beyond previously recorded end indexes --> entirely new line, add all points in between to holes set
                    row_wlines.append([n_line[0], n_line[1]+1])
                elif n_line[1] <= row_wlines[0][0]:
                    # x--y a--b c--d
                    # entirely to left of previously recorded
                    # shift beginning of existing line to beginning of this sensor's row, including
                    if n_line[1]+1 >= row_wlines[0][0]:
                        row_wlines[0][0] = n_line[0]
                    else:
                        row_wlines.insert(0,[n_line[0], n_line[1]+1])
                else:
                    # overlaps or between previously recorded lines; get line parts where x_start is between
                    # get first index where n_line[0] is larger than
                    # [a,b] x [c, d] where a <= nline[0] <=c
                    c_i = -1
                    for i in range(0, len(row_wlines)):
                        if n_line[0] <= row_wlines[i][0]:
                            c_i = i
                            break
                    if c_i <0:
                        # then we must have .... e-x-f--y for last item
                        if n_line[1] >= row_wlines[-1][1]:
                            row_wlines[-1][1] = n_line[1] + 1
                    # check whether end nline[1] >b
                    elif c_i == 0:
                        # x ---a-y---b or x---a---b--y
                        # will start at n_line[0] then ; already checked that end is not before first begin
                        end = max(row_wlines[c_i][1], n_line[1]+1)
                        to_del = []
                        j = c_i + 1
                        while j < len(row_wlines) and n_line[1]+1 >= row_wlines[j][0]:
                            # remove this one and add it to prev
                            end = max(n_line[1]+1, row_wlines[j][1])
                            to_del.append(j)
                            j+=1
                        for j in to_del:
                            row_wlines.pop(j)
                            # x---a---b--y
                            # change end too:
                        row_wlines[c_i][1] = end
                        row_wlines[c_i][0] = n_line[0]
                    # a---x--b---y c---d  or   a---x--b-----c-y--d or a---x--b--c--d--y or
                    #  a--b x--y c--d    or a--b x--c-y-d or  a--b x--c--d--y
                    # a--x--y--b c--d
                    elif n_line[1] < row_wlines[c_i-1][1]:
                        # a--x--y--b c--d
                        pass
                    elif  n_line[0] <= row_wlines[c_i-1][1]:
                        # a---x--b---y c---d  or   a---x--b-----c-y--d or a---x--b--c--d--y
                        if n_line[1] >= row_wlines[c_i][1]:
                            #  a---x--b--c--d--y ---> see until where y goes
                            end = max(row_wlines[c_i][1], n_line[1]+1)
                            to_del = [c_i]
                            j = c_i + 1
                            while j < len(row_wlines) and n_line[1]+1 >= row_wlines[j][0]:
                                # remove this one and add it to prev
                                end = max(n_line[1] + 1, row_wlines[j][1])
                                to_del.append(j)
                                j += 1
                            to_del.sort(reverse=True)
                            for j in to_del:
                                row_wlines.pop(j)
                                # change end too:
                            row_wlines[c_i-1][1] = end

                        elif n_line[1] == row_wlines[c_i][0] or n_line[1] + 1 == row_wlines[c_i][0]:
                            #         a---x--b---yc---d
                            row_wlines[c_i - 1][1] = row_wlines[c_i][1]
                            row_wlines.pop(c_i)
                        elif n_line[1] < row_wlines[c_i][0]:
                            #         a---x--b---y c---d
                            row_wlines[c_i-1][1] = n_line[1] + 1
                        else:
                            #  a---x--b-----c-y--d
                            row_wlines[c_i - 1][1] = row_wlines[c_i][1]
                            row_wlines.pop(c_i)
                    #  a--b x--y c--d    or a--b x--c-y-d or  a--b x--c--d--y
                    else:
                        if n_line[1] >= row_wlines[c_i][1]:
                            #  a--b x--c--d--y

                            end = n_line[1] + 1
                            to_del = []
                            j = c_i + 1
                            while j < len(row_wlines) and n_line[1] + 1 >= row_wlines[j][0]:
                                # remove this one and add it to prev
                                end = max(n_line[1] + 1, row_wlines[j][1])
                                to_del.append(j)
                                j += 1
                            for j in to_del:
                                row_wlines.pop(j)
                                # change end too:
                            row_wlines[c_i][1] = end
                            row_wlines[c_i][0] = n_line[0]
                        elif n_line[1] < row_wlines[c_i][0]:
                            # a--b x--y c--d
                            row_wlines.insert(c_i, [n_line[0], n_line[1] + 1])
                        else:
                            # a--b x--c-y-d
                            row_wlines[c_i][0] = n_line[0]
            else:
                #add exactly what this sensor reaches
                lines[row] = [[n_line[0], n_line[1]+1]]
    # take out all lines that are filled:
    remaining = []
    for y, rowi in lines.items():
        if y<=pmax and len(rowi) > 1:
            # should be two:
            remaining.append((y, rowi))
        # if pmin <= y <= pmax:
        #     if not (rowi[0] <= pmin and rowi[1] >= pmax and len(rowi[2]) == 0):
        #         remaining.append((rowi, y))
    res = -1
    if len(remaining) == 1:
        # row = [(y, [[a, x], [x+1, b]])]
        # 130 s
        #must be correct, result = x * + y
        res = remaining[0][1][0][1]*4000000 + remaining[0][0]
    return remaining, res
    # return remaining[0][0][2].pop()*4000000 + remaining[0][1]


        # max=3
 # ..###B###.     0: 1 + (max-0)*2
 # ...#####....   1: 1 + (max-1)*2
 # ....S##....    2: 1 + (max-2)*2
 # .....#....     3: 1 + (max-3)
 # ..........
 # ..........

print("Part 1")
# b_r, mini, maxi, bl = get_puzzle_input("test_data.txt")
# print(solve_p1(b_r, mini, maxi, bl))
# b_r, mini, maxi, bl = get_puzzle_input("data.txt")
# t = time.time()
# print(solve_p1(b_r, mini, maxi, bl, row=2000000))
# print("took: ", time.time()-t,  "s")

print("Part 2")
b_r, mini, maxi, bl = get_puzzle_input("test_data.txt")
t = time.time()
print(solve_p2(b_r, mini, maxi, bl, pmax=20))
print("took: ", time.time()-t,  "s")

b_r, mini, maxi, bl = get_puzzle_input("data.txt")
t = time.time()
print(solve_p2(b_r, mini, maxi, bl))
print("took: ", time.time()-t,  "s")