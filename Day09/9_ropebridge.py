# --- Day 9: Rope Bridge ---
from numpy.core._multiarray_umath import sign

direction_translater = {
    'R':(+1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1)
}


def get_new_tail_position(current_pos_head, current_pos_tail):
    # already know they are split
    (difference_x, difference_y) = (current_pos_head[0] - current_pos_tail[0], current_pos_head[1] - current_pos_tail[1])
    if difference_x == 0:
        # horizontally in same line, so move vertically
        return (current_pos_tail[0], current_pos_tail[1] + sign(difference_y))
    if difference_y == 0:
        return (current_pos_tail[0]+sign(difference_x), current_pos_tail[1])
    # go diagonally towards
    return (current_pos_tail[0]+sign(difference_x), current_pos_tail[1] + sign(difference_y))


def solve_part_1(filepath):
    visited_pos = {(0,0)}
    current_pos_head = (0,0)
    current_pos_tail = (0,0)
    with open(filepath) as f:
        for line in f:
            # move the head
            [direction, count] = line.rstrip().split(" ")
            for _ in range(0, int(count)):
                # move head:
                changing_pos = direction_translater[direction]
                current_pos_head = (current_pos_head[0] + changing_pos[0], current_pos_head[1]+changing_pos[1])
                if abs(current_pos_head[0]-current_pos_tail[0]) > 1 or abs(current_pos_head[1]-current_pos_tail[1]) > 1: # not touching
                    #change tails spot:
                    current_pos_tail = get_new_tail_position(current_pos_head, current_pos_tail)
                    visited_pos.add(current_pos_tail)
    return len(visited_pos)


def solve_part_2(filepath):
    visited_pos_nod10 = {(0,0)}
    current_pos_rope = [(0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0), (0,0)]
    with open(filepath) as f:
        for line in f:
            # move the head
            [direction, count] = line.rstrip().split(" ")
            for _ in range(0, int(count)):
                # move head:
                changing_pos = direction_translater[direction]
                current_pos_rope[0] = [current_pos_rope[0][0] + changing_pos[0], current_pos_rope[0][1] + changing_pos[1]]
                moved = True
                tail_index = 1
                while moved: # not touching
                    if (abs(current_pos_rope[tail_index-1][0]-current_pos_rope[tail_index][0]) > 1
                                 or abs(current_pos_rope[tail_index-1][1]-current_pos_rope[tail_index][1]) > 1 ):
                        #change tails spot:
                        current_pos_rope[tail_index] = get_new_tail_position(current_pos_head=current_pos_rope[tail_index -1],
                                                                             current_pos_tail=current_pos_rope[tail_index])
                        tail_index +=1
                    else:
                        moved = False
                    if tail_index == 10:
                        # we just looked at 9
                        moved = False
                        visited_pos_nod10.add(current_pos_rope[-1])
    return len(visited_pos_nod10)

print("Part 1")
print("test:", solve_part_1("test_data.txt"))
print("data:", solve_part_1("data.txt"))

print("\nPart 2")

print("test:", solve_part_2("test_data.txt"))
print("data:", solve_part_2("data.txt"))