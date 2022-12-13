
def compare_two_pairs(left, right):
    # check if it is mixed type -> then transform int to list
    if type(left) != type(right):
        if type(left) is int:
            left = [left]
        else:
            right = [right]
    # if it is an integer
    if type(left) is int:
        if left < right:
            return 1 # right
        if left > right:
            return -1 #wrong
        return 0 # then they are equal, continue checking
    # if it is a list
    res = 0
    i = 0
    while res == 0 and i < len(left):
        if i >= len(right):
            return -1 # right side is shorter
        res = compare_two_pairs(left[i], right[i])
        i += 1
    if i == len(left) and res == 0:
        if len(right) > i:
            # left side ran out of items, while right still has some, so correct
            return 1
        else:
            return 0
    # undefined
    return res



class Packet(object):

    def __init__(self, packet_string):
        self.p_s = packet_string

    def __lt__(self, other):
        # -1 if right is lower, 0 if they are equal, 1 if left is lower
        res = compare_two_pairs(self.p_s, other.p_s)
        return res == 1

    def __le__(self, other):
        # -1 if right is lower, 0 if they are equal, 1 if left is lower
        res = compare_two_pairs(self.p_s, other.p_s)
        return res != -1

    def __eq__(self, other):
        res = compare_two_pairs(self.p_s, other.p_s)
        return res == 0

    def __ne__(self, other):
        res = compare_two_pairs(self.p_s, other.p_s)
        return res != 0

    def __gt__(self, other):
        res = compare_two_pairs(self.p_s, other.p_s)
        return res == -1

    def __ge__(self, other):
        res = compare_two_pairs(self.p_s, other.p_s)
        return res != 1

    def __str__(self):
        return "P{}".format(self.p_s)

    def __repr__(self):
        return self.__str__()

def get_pairs_from_file(filepath):
    pairs = []
    current_pair = []
    with open(filepath) as f:
        for line in f:
            if line == "\n":
                # new pair begins
                pairs.append((current_pair[0], current_pair[1]))
                current_pair = []
                continue
            line.rstrip()
            # parse the packet --> more entries = levels of incursion
            packet = [[]]

            i = 0
            d = ""
            while i < len(line):
                if line[i].isdigit():
                    d += line[i]
                    i += 1
                    continue
                if line[i] == ",":
                    # next item is starting
                    if d != "":
                        # then we have <int>,
                        d = int(d)
                        packet[-1].append(d)
                        d = ""
                    # then we had ],

                if line[i] == "]":
                    if d != "":
                        # then we have <int>]
                        d = int(d)
                        packet[-1].append(d)
                        d = ""
                    # if i ==
                    # current item is done so add it to previous
                    p = packet.pop()
                    packet[-1].append(p)  # add it to latest list
                    # do nothing else, because list is closed with the komma
                if line[i] == "[":
                    # create new list in packet, nee element is starting
                    # can never have <int>[ so we dont need to check
                    packet.append([])
                i +=1
            # fix last ?
            current_pair.append(packet[0][0])
        # add last pair
        pairs.append((current_pair[0], current_pair[1]))
    return pairs


def get_all_packets_from_file_as_packets(filepath):
    pairs = []
    current_pair = []
    with open(filepath) as f:
        for line in f:
            if line == "\n":
                # new pair begins
                pairs.append(Packet(current_pair[0]))
                pairs.append(Packet(current_pair[1]))
                current_pair = []
                continue
            line.rstrip()
            # parse the packet --> more entries = levels of incursion
            packet = [[]]

            i = 0
            d = ""
            while i < len(line):
                if line[i].isdigit():
                    d += line[i]
                    i += 1
                    continue
                if line[i] == ",":
                    # next item is starting
                    if d != "":
                        # then we have <int>,
                        d = int(d)
                        packet[-1].append(d)
                        d = ""
                    # then we had ],

                if line[i] == "]":
                    if d != "":
                        # then we have <int>]
                        d = int(d)
                        packet[-1].append(d)
                        d = ""
                    # if i ==
                    # current item is done so add it to previous
                    p = packet.pop()
                    packet[-1].append(p)  # add it to latest list
                    # do nothing else, because list is closed with the komma
                if line[i] == "[":
                    # create new list in packet, nee element is starting
                    # can never have <int>[ so we dont need to check
                    packet.append([])
                i +=1
            # fix last ?
            current_pair.append(packet[0][0])
        # add last pair
        pairs.append(Packet(current_pair[0]))
        pairs.append(Packet(current_pair[1]))
    return pairs


def solve_part_1(pairs):
    pairs_ind = 0
    result_sum = 0
    while pairs_ind < len(pairs):
        [left, right] = pairs[pairs_ind]
        res = compare_two_pairs(left, right)
        if res == 1:
            # then it must be correct
            result_sum += pairs_ind + 1 # since in puzzle index starts with 1
        pairs_ind += 1
    return result_sum

def solve_part_2(pairs):
    pairs.extend([Packet([[6]]),Packet([[2]])])
    pairs.sort()
    # indexes start with 1 in the puzzle that is why we add 1
    return (1+pairs.index(Packet([[6]]))) * (1+pairs.index(Packet([[2]])))

print("Part 1", "\n")
# print("test:", solve_part_1(get_pairs_from_file("test_data.txt")), "\n")
# print("data:", solve_part_1(get_pairs_from_file("data.txt")), "\n")

print("\nPart 2")

print("test:", solve_part_2(get_all_packets_from_file_as_packets("test_data.txt")))
print("data:", solve_part_2(get_all_packets_from_file_as_packets("data.txt")))