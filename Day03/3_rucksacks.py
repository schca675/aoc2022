def get_priority(character):
    ascii_a = ord('a')
    ascii_char = ord(character)
    if ascii_char >= ascii_a:
        # smaller letter
        return 1 + ascii_char - ascii_a # start with a=1
    else:
        # capitalized letter
        ascii_AA = ord('A')
        return 27 + ascii_char - ascii_AA # start with A=27


def solve_part_1(filepath):
    priorities = 0
    with open(filepath) as f:
        for line in f:
            # every line is one rucksack, transform every compartment into a set
            c1, c2 = set(line[:len(line)//2]), set(line[len(line)//2:-1])
            # find item that is in both compartment = intersection of sets
            wrong_item = c2.intersection(c1)
            # take item from intersection set and get priority
            priorities += get_priority(wrong_item.pop())
    return priorities

def solve_part_2(filepath):
    # get common items of all three
    # print(sum([get_priority(set(x.rstrip()).intersection(set(y.rstrip())).intersection(set(z.rstrip())).pop()) for (x,y,z) in list(zip(*[iter(open(filepath))] * 3))]))
    return sum([get_priority(set(x[:-1]).intersection(set(y[:-1])).intersection(set(z[:-1])).pop()) for (x,y,z) in list(zip(*[iter(open(filepath))] * 3))])


print("Part 1")
print("test:", solve_part_1("test_data.txt"))
print("data:", solve_part_1("data.txt"))

print("\nPart 2")

print("test:", solve_part_2("test_data.txt"))
print("data:", solve_part_2("data.txt"))