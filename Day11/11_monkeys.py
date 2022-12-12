import math
import heapq
import time

class Monkey(object):
    all_monkeys = [] # every monkey has access to this monkey list

    def __init__(self, id, starting_items:list, lambda_operation, operation_value,
                                    test_divide_value, if_false_monkey_id, if_true_monkey_id):
        self.id = id # id of monkey is number in the monkey list
        self.current_items = starting_items
        self.operation = lambda_operation
        self.op_value = operation_value
        self.test_divide_by = test_divide_value
        self.ifTrue_throw_to = if_true_monkey_id
        self.ifFalse_throw_to = if_false_monkey_id

        self.hasinspected_items = 0

    def receive_item(self, item):
        self.current_items.append(item)

    def inspect_item(self):
        # inspect the items it has
        for worry_level in self.current_items: # take them one by one, first entered, first taken out
            # inspect it
            if self.op_value == "old":
                worry_level = self.operation(worry_level, worry_level) # new worry level
            else:
                worry_level = self.operation(worry_level, self.op_value) # new worry level
            # increase inspected counter
            self.hasinspected_items += 1
            # undamaged, so divide by three, rounded down to nearest integer
            # worry_level = worry_level // 3 #TODO: only used for part 1
            # test and throw
            if worry_level % self.test_divide_by == 0:
                # throw to true monkey, id of that monkey = place in list
                self.all_monkeys[self.ifTrue_throw_to].receive_item(worry_level)
            else:
                #throw to false monkey.
                self.all_monkeys[self.ifFalse_throw_to].receive_item(worry_level)
        self.current_items = [] # it never keeps any items (manual inspection)

    def __str__(self):
        return "{}_{}".format(self.id, self.current_items)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.hasinspected_items < other.hasinspected_items

    def __le__(self, other):
        return self.hasinspected_items <= other.hasinspected_items

    def __eq__(self, other):
        return self.hasinspected_items == other.hasinspected_items

    def __ne__(self, other):
        return self.hasinspected_items != other.hasinspected_items

    def __gt__(self, other):
        return self.hasinspected_items > other.hasinspected_items

    def __ge__(self, other):
        return self.hasinspected_items >= other.hasinspected_items




def get_monkeys_from_file(filepath):
    monkeys = []
    monkey = []
    with open(filepath) as f:
        for line in f:
            line = line.replace(",", " ")
            parts = line.rstrip().split()
            if len(parts) == 0:
                # assume that lines were read consecutively so it corresponds to what is in monkey
                # create monkey
                new_monkey = Monkey(id=len(Monkey.all_monkeys),
                                    starting_items=monkey[0],
                                    lambda_operation=monkey[1],
                                    operation_value= monkey[2],
                                    test_divide_value=monkey[3],
                                    if_true_monkey_id=monkey[4],
                                    if_false_monkey_id=monkey[5])
                Monkey.all_monkeys.append(new_monkey)
                monkeys.append(new_monkey)
                monkey = []
                continue
            if parts[0] == "Starting":
                monkey.append([int(x) for x in parts[2:]])
                continue
            if parts[0] == "Operation:":
                #get operator
                if parts[-2] == "+":
                    monkey.append(lambda a,b: a + b)
                elif parts[-2] == "*":
                    monkey.append(lambda a,b: a*b)
                # get first second argument: (first argument is always old)
                if parts[-1] == "old":
                    monkey.append("old")
                else:
                    monkey.append(int(parts[-1]))
                # if parts[-2] == "-":
                #     monkey.append(lambda old:old - number)
                continue
            if parts[0] == "Test:":
                # data inspection shows all have "divisible by"
                # monkey.append(lambda worry_level, number: worry_level % number == 0)
                monkey.append(int(parts[-1]))
                continue
            if "If true:" in line:
                monkey.append(int(parts[-1])) # throw to monkey with id xx
                continue
            if "If false:" in line:
                monkey.append(int(parts[-1]))  # throw to monkey with id xx
                continue
    # create last monkey
    new_monkey = Monkey(id=len(Monkey.all_monkeys),
                        starting_items=monkey[0],
                        lambda_operation=monkey[1],
                        operation_value=monkey[2],
                        test_divide_value=monkey[3],
                        if_true_monkey_id=monkey[4],
                        if_false_monkey_id=monkey[5])
    Monkey.all_monkeys.append(new_monkey)
    monkeys.append(new_monkey)
    return monkeys


def monkeys_play_around(monkeys, xtimes):
    for _ in range(0, xtimes):
        for monkey in monkeys:
            monkey.inspect_item()
    # get two max values
    return math.prod([m.hasinspected_items for m in heapq.nlargest(2, monkeys)])

print("Part 1", "\n")
now=time.time()
# print("test:", monkeys_play_around(get_monkeys_from_file("test_data.txt"), 20), "\n time needed: ", time.time()-now)
now = time.time()
# print("data:", monkeys_play_around(get_monkeys_from_file("data.txt"), 20), "\n time needed: ", time.time()-now)

print("\nPart 2")

# print("test:", solve_part_2("test_data.txt"))
# print("data:", solve_part_2("data.txt"))




class QuickMonkey(object):
    all_monkeys = [] # every monkey has access to this monkey list
    all_divisors = []

    def __init__(self, id, starting_items:list, str_operation, operation_value,
                                    test_divide_value, if_false_monkey_id, if_true_monkey_id):
        self.id = id # id of monkey is number in the monkey list
        self.current_items = starting_items
        self.operation = str_operation
        self.op_value = operation_value
        self.test_divide_by = test_divide_value
        self.all_divisors.append(test_divide_value)
        self.ifTrue_throw_to = if_true_monkey_id
        self.ifFalse_throw_to = if_false_monkey_id

        self.hasinspected_items = 0

    def convert_item_list_to_being_modulo_friendly(self):
        # can only be called if all divisors of the monkeys are known
        self.current_items = [[item % divisor for divisor in self.all_divisors] for item in self.current_items]

    def receive_item(self, item):
        self.current_items.append(item)

    def inspect_item(self):
        # inspect the items it has
        for worry_level in self.current_items: # take them one by one, first entered, first taken out
            # inspect it
            if self.operation == "+":
                # monkeys divisor is on the spot of its id; from the order of adding divisors
                if self.op_value == "old":
                    # add with self: then just add modulos
                    worry_level = [(level + level) % self.all_divisors[i] for level, i in zip(worry_level, range(0, len(worry_level)))]
                else:
                    worry_level = [(level + self.op_value)  % self.all_divisors[i] for level, i in zip(worry_level, range(0, len(worry_level)))]
            elif self.operation == "*":
                if self.op_value == "old":
                    worry_level = [(level * level) % self.all_divisors[i] for level, i in zip(worry_level, range(0, len(worry_level)))]
                else:
                    worry_level = [(level * self.op_value) % self.all_divisors[i] for level, i in zip(worry_level, range(0, len(worry_level)))]

            # increase inspected counter
            self.hasinspected_items += 1
            # undamaged, so divide by three, rounded down to nearest integer
            # test and throw
            if worry_level[self.id] == 0: # then modulo is 0, so divisible
                # throw to true monkey, id of that monkey = place in list
                self.all_monkeys[self.ifTrue_throw_to].receive_item(worry_level)
            else:
                #throw to false monkey.
                self.all_monkeys[self.ifFalse_throw_to].receive_item(worry_level)
        self.current_items = [] # it never keeps any items (manual inspection)

    def __str__(self):
        return "{}_{}".format(self.id, self.current_items)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.hasinspected_items < other.hasinspected_items

    def __le__(self, other):
        return self.hasinspected_items <= other.hasinspected_items

    def __eq__(self, other):
        return self.hasinspected_items == other.hasinspected_items

    def __ne__(self, other):
        return self.hasinspected_items != other.hasinspected_items

    def __gt__(self, other):
        return self.hasinspected_items > other.hasinspected_items

    def __ge__(self, other):
        return self.hasinspected_items >= other.hasinspected_items


def get_quick_monkeys_from_file(filepath):
    monkeys = []
    monkey = []
    with open(filepath) as f:
        for line in f:
            line = line.replace(",", " ")
            parts = line.rstrip().split()
            if len(parts) == 0:
                # assume that lines were read consecutively so it corresponds to what is in monkey
                # create monkey
                new_monkey = QuickMonkey(id=len(QuickMonkey.all_monkeys),
                                    starting_items=monkey[0],
                                    str_operation=monkey[1],
                                    operation_value= monkey[2],
                                    test_divide_value=monkey[3],
                                    if_true_monkey_id=monkey[4],
                                    if_false_monkey_id=monkey[5])
                QuickMonkey.all_monkeys.append(new_monkey)
                monkeys.append(new_monkey)
                monkey = []
                continue
            if parts[0] == "Starting":
                monkey.append([int(x) for x in parts[2:]])
                continue
            if parts[0] == "Operation:":
                #get operator
                monkey.append(parts[-2])
                # get first second argument: (first argument is always old)
                if parts[-1] == "old":
                    monkey.append("old")
                else:
                    monkey.append(int(parts[-1]))
                # if parts[-2] == "-":
                #     monkey.append(lambda old:old - number)
                continue
            if parts[0] == "Test:":
                # data inspection shows all have "divisible by"
                # monkey.append(lambda worry_level, number: worry_level % number == 0)
                monkey.append(int(parts[-1]))
                continue
            if "If true:" in line:
                monkey.append(int(parts[-1])) # throw to monkey with id xx
                continue
            if "If false:" in line:
                monkey.append(int(parts[-1]))  # throw to monkey with id xx
                continue
    # create last monkey
    new_monkey = QuickMonkey(id=len(QuickMonkey.all_monkeys),
                        starting_items=monkey[0],
                        str_operation=monkey[1],
                        operation_value=monkey[2],
                        test_divide_value=monkey[3],
                        if_true_monkey_id=monkey[4],
                        if_false_monkey_id=monkey[5])
    QuickMonkey.all_monkeys.append(new_monkey)
    monkeys.append(new_monkey)
    for m in monkeys:
        m.convert_item_list_to_being_modulo_friendly()
    return monkeys

print("Part 2", "\n")
now=time.time()
# print("test:", monkeys_play_around(get_quick_monkeys_from_file("test_data.txt"), 10000), "\n time needed: ", time.time()-now)
now = time.time()
print("data:", monkeys_play_around(get_quick_monkeys_from_file("data.txt"), 10000), "\n time needed: ", time.time()-now)

print("\nPart 2")

# print("test:", solve_part_2("test_data.txt"))
# print("data:", solve_part_2("data.txt"))