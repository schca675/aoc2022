def solve_part_1(filepath):
    overlaps = 0
    with open(filepath) as f:
        for line in f:
            # split into both elves.
            [elf_1, elf_2] = [x.split('-') for x in line.rstrip().split(',')]
            if int(elf_1[0]) <= int(elf_2[0]):
                # yes: elf1's range is lower than elf 2's
                if int(elf_1[1]) >= int(elf_2[1]):
                    # also its upper range is larger than elf2's.
                    overlaps +=1
                    continue
            if int(elf_2[0]) <= int(elf_1[0]):
                # elf 2's range is lower than elf 1's
                if int(elf_2[1]) >= int(elf_1[1]):
                    # also its upper range is larger than elf1's.
                    overlaps += 1
    return overlaps

def solve_part_2(filepath):
    overlaps = 0
    with open(filepath) as f:
        for line in f:
            # split into both elves.
            elves = [[int(n) for n in x.split('-')] for x in line.rstrip().split(',')]
            elves.sort() # now lowest range is first in the list
            if elves[1][0] <= elves[0][1]:
                # if lower bound of second elf (having higher starting range) is lower than the upper bound of the first elf, they overlap.
                overlaps +=1
    return overlaps

print("Part 1")
print("test:", solve_part_1("test_data.txt"))
print("data:", solve_part_1("data.txt"))

print("\nPart 2")

print("test:", solve_part_2("test_data.txt"))
print("data:", solve_part_2("data.txt"))