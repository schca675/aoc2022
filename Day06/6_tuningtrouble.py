# --- Day 6: Tuning Trouble ---


def are_chars_different(tested_chars, how_many_chars_we_want=4):
    return len(set(tested_chars)) == how_many_chars_we_want


def get_first_start_of_packet_marker(signal, how_many_chars_we_want=4):
    for i in range(how_many_chars_we_want, len(signal)+2):
        if are_chars_different(signal[i-how_many_chars_we_want:i], how_many_chars_we_want=how_many_chars_we_want):
            return i #when i's charachter arrived.
    return -1

def solve_part_1_and_2(filepath):
    with open(filepath) as f:
        for line in f:
            print("Part 1")
            print(line,"\n", get_first_start_of_packet_marker(line.rstrip(), how_many_chars_we_want=4))
            print("Part 2")
            print(line,"\n", get_first_start_of_packet_marker(line.rstrip(), how_many_chars_we_want=14))

print("Test")
solve_part_1_and_2("test_data.txt")
print("\nData")
solve_part_1_and_2("data.txt")
