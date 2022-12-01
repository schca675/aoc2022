def get_puzzle_input(filepath):
    a_list = []
    with open(filepath) as f:
        for line in f:
            a_list.append(line.rstrip())
    return a_list