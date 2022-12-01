# --- Day 1: Calorie Counting ---

def solve_part_1(filepath):
    highest_cals = -1
    current_elf = 0
    with open(filepath) as f:
        for line in f:
            # the calories of the elfs are done
            if line == "\n":
                # check if current elf has the highest calories
                if current_elf > highest_cals:
                    # then set 
                    highest_cals = current_elf
                # reset counter for next elf
                current_elf = 0
            else:
                current_elf += int(line.strip())
        # also check whether the last elf is one of the highest
        if current_elf > highest_cals:
            return current_elf
    return highest_cals

def solve_part_2(filepath):
    highest_cals = []
    lowest_of_highest = -1
    current_elf = 0
    with open(filepath) as f:
        for line in f:
            # the calories of the elfs are done
            if line == "\n":
                # new value having the calories of the current elf
                # to be able to reset counter in advance
                new_value = current_elf
                # reset counter for current elf
                current_elf = 0
                # if we have already 3 and the new elf is not one of the highest continue on to the next elf
                if new_value < lowest_of_highest and len(highest_cals) == 3:
                    continue
                # reached if current elf is one of the top 3 carriers
                # if we had already 3 elfs, we need to remove the one with the lowest calories
                if len(highest_cals) == 3:
                    highest_cals.remove(lowest_of_highest)
                # add the new elf
                highest_cals.append(new_value)
                # determine the new threshold to join the elfs with the most carriers.
                lowest_of_highest = min(highest_cals)
            # the elf has more calories
            else:
                current_elf += int(line.strip())
        # also check whether the last elf is one of the highest
        if current_elf > lowest_of_highest:
            highest_cals.remove(lowest_of_highest)
            highest_cals.append(current_elf)
    return sum(highest_cals)


print("Part 1")
print("test:", solve_part_1("test_data.txt"))
print("data:", solve_part_1("data.txt"))

print("\nPart 2")
print("test:", solve_part_2("test_data.txt"))
print("data:", solve_part_2("data.txt"))