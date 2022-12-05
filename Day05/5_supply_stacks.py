
#  Test stacks
#     [D]
# [N] [C]
# [Z] [M] [P]
#  1   2   3

# # Actual stacks:
# [P]     [C]         [M]
# [D]     [P] [B]     [V] [S]
# [Q] [V] [R] [V]     [G] [B]
# [R] [W] [G] [J]     [T] [M]     [V]
# [V] [Q] [Q] [F] [C] [N] [V]     [W]
# [B] [Z] [Z] [H] [L] [P] [L] [J] [N]
# [H] [D] [L] [D] [W] [R] [R] [P] [C]
# [F] [L] [H] [R] [Z] [J] [J] [D] [D]
#  1   2   3   4   5   6   7   8   9
#
# [P]' , '[D]' , '[Q]' , '[R]' , '[V]' , '[B]' , '[H]' , '[F]
# 		[V]' , '[W]' , '[Q]' , '[Z]' , '[D]' , '[L]
# [C]' , '[P]' , '[R]' , '[G]' , '[Q]' , '[Z]' , '[L]' , '[H]
# 	[B]' , '[V]' , '[J]' , '[F]' , '[H]' , '[D]' , '[R]
# 				[C]' , '[L]' , '[W]' , '[Z]
# [M]' , '[V]' , '[G]' , '[T]' , '[N]' , '[P]' , '[R]' , '[J]
# 	[S]' , '[B]' , '[M]' , '[V]' , '[L]' , '[R]' , '[J]
# 					[J]' , '[P]' , '[D]
# 			[V]' , '[W]' , '[N]' , '[C]' , '[D]


# def get_crates(filepath, nr_crates=9):
#     crates = dict()
#     for j in range(1, nr_crates+1):
#         crates[j] = []
#     with open(filepath) as f:
#         for line in f:
#             i = 1
#             while i<nr_crates:
#                 c = line[1+(i-1)*4]
#                 if c != '\t':
#                     crates[i].append(c)
#                 i+=4
#     return crates
test_crates = {
    1:['[Z]', '[N]'],
    2:['[M]', '[C]', '[D]'],
    3:['[P]']
}
crates = {1: ['[P]','[D]','[Q]','[R]','[V]','[B]','[H]','[F]'],
		2:['[V]','[W]','[Q]','[Z]','[D]','[L]'],
3:['[C]' , '[P]' , '[R]' , '[G]' , '[Q]' , '[Z]' , '[L]' , '[H]'],
	4:['[B]' , '[V]' , '[J]' , '[F]' , '[H]' , '[D]' , '[R]'],
			5:	['[C]' , '[L]' , '[W]' , '[Z]'],
6:['[M]' , '[V]' , '[G]' , '[T]' , '[N]' , '[P]' , '[R]' , '[J]'],
	7:['[S]' , '[B]' , '[M]' , '[V]' , '[L]' , '[R]' , '[J]'],
					8:['[J]' , '[P]' , '[D]'],
			9:['[V]' , '[W]' , '[N]' , '[C]' , '[D]'] }
for i,crate in crates.items():
    crate.reverse()

def print_crates(these_crates):
    TOP = ""
    # print crates
    for it, crate in these_crates.items():
        print("{:02d}: {}".format(it, crate))
        if len(crate) == 0:
            TOP +=' '
        else:
            TOP += crate[-1][1]
    return TOP

def solve_part_1(start_crates, filepath, p1_rearrange_individually=True):
    with open(filepath) as f:
        for line in f:
            # parse instruction
            parts = line.rstrip().split(' ')
            amount = int(parts[1])
            from_stack = int(parts[3])
            to_stack = int(parts[5])
            # execute instructions
            if p1_rearrange_individually:
                for _ in range(0, amount):
                    crate = start_crates[from_stack].pop()
                    start_crates[to_stack].append(crate)
            else:
                start_crates[to_stack].extend(start_crates[from_stack][-amount:])
                start_crates[from_stack] = start_crates[from_stack][:-amount]

    return print_crates(start_crates)

print("Part 1")
# print("test", solve_part_1(test_crates, "test_data.txt"))
print("solution: ", solve_part_1(crates, "data.txt"))

test_crates = {
    1:['[Z]', '[N]'],
    2:['[M]', '[C]', '[D]'],
    3:['[P]']
}
crates = {1: ['[P]','[D]','[Q]','[R]','[V]','[B]','[H]','[F]'],
		2:['[V]','[W]','[Q]','[Z]','[D]','[L]'],
3:['[C]' , '[P]' , '[R]' , '[G]' , '[Q]' , '[Z]' , '[L]' , '[H]'],
	4:['[B]' , '[V]' , '[J]' , '[F]' , '[H]' , '[D]' , '[R]'],
			5:	['[C]' , '[L]' , '[W]' , '[Z]'],
6:['[M]' , '[V]' , '[G]' , '[T]' , '[N]' , '[P]' , '[R]' , '[J]'],
	7:['[S]' , '[B]' , '[M]' , '[V]' , '[L]' , '[R]' , '[J]'],
					8:['[J]' , '[P]' , '[D]'],
			9:['[V]' , '[W]' , '[N]' , '[C]' , '[D]'] }
for i,crate in crates.items():
    crate.reverse()
print("Part 1")
print("test", solve_part_1(test_crates, "test_data.txt", p1_rearrange_individually=False))
print("solution: ", solve_part_1(crates, "data.txt", p1_rearrange_individually=False))