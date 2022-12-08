# --- Day 7: No Space Left On Device ---

class Folder(object):

    def __init__(self, parent, name):
        self.contains_folders = dict()  # list of folders it contains
        self.contains_files = list()  # set of sizes
        self.parent = parent
        self.name = name
        while parent is not None: #root
            name = parent.name + "/" + name
            parent = parent.parent
        self.full_name = name

    def __eq__(self, other):
        return other.full_name == self.full_name

    def __hash__(self):
        return self.full_name

    def __repr__(self):
        return "{}".format(self.full_name)


def get_size_of_folder(of_folder, known_sizes):
    if of_folder.full_name in known_sizes:
        return known_sizes[of_folder.full_name]
    # otherwise calculate it
    tot = sum(of_folder.contains_files)
    # now add directories
    for folder in of_folder.contains_folders.values():
        tot += get_size_of_folder(folder, known_sizes)
    # save it in dict
    known_sizes[of_folder.full_name] = tot
    return tot



def solve_part_1_and_2(filepath):
    root_folder = Folder(None, "/")
    all_folders = [root_folder]
    current_folder = root_folder #
    ls_active = True
    with open(filepath) as f:
        for line in f:
            if line[0] == "$":
                # it is a command:
                line_parts = line.rstrip().split(" ")
                # check command
                if line_parts[1] == "cd":
                    ls_active = False
                    # go to directory
                    if line_parts[2] == "/":
                        # should only happen the first time?
                        current_folder = root_folder
                    elif line_parts[2] == "..":
                        # go up one folder:
                        # requires folder to know its parent
                        current_folder = current_folder.parent
                    else:
                        # go deeper on level into line_parts[2]
                        if line_parts[2] in current_folder.contains_folders.keys():
                            # ls has been called and we know this folder is in current_folder
                            current_folder = current_folder.contains_folders[line_parts[2]]
                        else:
                            # ls has not been called so we add that this folder belongs to
                            print("Is this even reached XXAOP - hten fix it")
                elif line_parts[1] == "ls":
                    # list
                    ls_active = True
                    pass
                else:
                    print("unknown command: ", line_parts)
            elif not ls_active:
                print("This should never happen: XXlsacrive: ", line)
            else:
                #ls active and list going on.
                # check if it is a file or fodler:
                line_parts = line.rstrip().split(" ")
                if line_parts[0] == "dir":
                    # directory, so create new directory
                    new_dir = Folder(current_folder, line_parts[1])
                    all_folders.append(new_dir)
                    current_folder.contains_folders[line_parts[1]] = new_dir
                else:
                    # file: add size to current folder TODO now without name
                    current_folder.contains_files.append(int(line_parts[0]))
    folder_size_dict = dict()

    # for folder in all_folders:
    total_size = get_size_of_folder(of_folder=root_folder, known_sizes=folder_size_dict)
    # how much space is left on disK
    space_left = total_disk_space - total_size
    min_folder_giving_enough_space = total_size + 1 # size of that folder
    res_p1 = 0
    for folder, size in folder_size_dict.items():
        if size <= 100000:
                res_p1 += size
        if space_left + size >= needed_disk_space and size < min_folder_giving_enough_space:
            min_folder_giving_enough_space = size
    print(folder_size_dict)
    return "part1, all smaller than 10000: ", res_p1, "part2, smallest to delete: ", min_folder_giving_enough_space

total_disk_space = 70000000
needed_disk_space = 30000000
print("Part 1 and 2")
print("Test\n", solve_part_1_and_2("test_data.txt"))
print("Data\n", solve_part_1_and_2("data.txt"))
