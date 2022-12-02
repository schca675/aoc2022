# --- Day 2: Rock Paper Scissors ---

your_scores = {'X': 1, #rock
               'Y': 2, #paper
               'Z': 3} #scissors}

matches = {"AX":3,  #draw
           "AY":6,  #win
           "AZ":0,  #lost
           "BY": 3,  # draw
           "BZ": 6,  # win
           "BX": 0,  # lost
           "CZ":3, #draw
           "CX":6, #win
           "CY":0, #lost
           }

def solve_part_1(filepath):
    score = 0
    with open(filepath) as f:
        for line in f:
            # convert input line of opponent and your choice: A X to a string
            round = line.rstrip().replace(" ", "")
            # add to score, value of choice and the win/lose score.
            score += your_scores[round[1]] + matches[round]
    return score

# A-rock, x-lose -> scissors-C
# A-rock y-draw -> rock-A
# A-rock z-win -> paper-B
rockpaperscissors = ["ABC"]
end_condition = {"X":0, "Y":1, "Z":2}
abc_scores = {'A': 1, #rock
               'B': 2, #paper
               'C': 3} #scissors}

fix_matches = {"AX":'C',  #lose
           "AY":'A', #draw
           "AZ":'B', #win
           "BY": 'B',  # draw
           "BZ": 'C',  # win
           "BX": 'A',  #lose
           "CZ":'A', #win
           "CX":'B', #lose
           "CY":'C', #draw
           }

def solve_part_2(filepath):
    score = 0
    with open(filepath) as f:
        for line in f:
            round = line.rstrip().replace(" ", "")
            score += 3*end_condition[round[1]]+ abc_scores[fix_matches[round]]
    return score

print("Part 1")
print("test:", solve_part_1("test_data.txt"))
print("data:", solve_part_1("data.txt"))

print("\nPart 2")
print("test:", solve_part_2("test_data.txt"))
print("data:", solve_part_2("data.txt"))