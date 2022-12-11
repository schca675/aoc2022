
def solve_part_1(filepath):
    sum_reg = 0
    cycle = 0
    register = 1
    line_to_draw = ""
    with open(filepath) as f:
        for line in f:
            # split line into command and register
            line_parts = line.rstrip().split()
            # at least one cycle needed
            cycle += 1
            if abs((cycle % 40 - register -1)) <= 1: # -1 because register starts with 0 and cycle with 1
                line_to_draw += "#"
            else:
                line_to_draw += "."

            #<<<< check if we need to keep it --> PART 1
            if (cycle - 20) % 40 == 0:
                sum_reg += register * cycle
            #<<<<<
            # part 2 check if new line starts
            if cycle % 40 == 0:
                # reached end of the line
                print(line_to_draw)
                line_to_draw = ""

            # if action is noop, we continue and dont use more cycles
            if line_parts[0] == "noop":
                continue

            # else we change register and check the cycle again (adding takes two cycles only on the second the register is changed).
            cycle += 1
            if abs((cycle % 40 - register-1)) <= 1:
                line_to_draw += "#"
            else:
                line_to_draw += "."

            #<<<<< --> part 1
            if (cycle - 20) % 40 == 0:
                sum_reg += register * cycle
            #<<<< --> part 1
            # part 2 check if new line starts
            if cycle % 40 == 0:
                # reached end of the line
                print(line_to_draw)
                line_to_draw = ""
            # register finishes after the two cycles
            register += int(line_parts[1])
    return sum_reg


print("Part 1", "\n")
print("test:", solve_part_1("test_data.txt"), "\n")
print("test2:", solve_part_1("test_data2.txt"), "\n")
print("data:", solve_part_1("data.txt"))

print("\nPart 2")

# print("test:", solve_part_2("test_data.txt"))
# print("data:", solve_part_2("data.txt"))