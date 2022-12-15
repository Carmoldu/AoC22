import re
from typing import Callable
from tqdm import tqdm

ROUNDS = 10000
FILE = 'Day11/input.txt'

class Monkey():
    def __init__(self, description: str):
        self.id = self.define_id(description)
        self.items = self.initialize_items(description)
        self.operation = self.define_operation(description)
        self.test = self.define_test(description)
        self.inspect_count = 0

    @staticmethod
    def define_id(description: str) -> int:
        id_str = re.findall(r'Monkey \d', description)[0]
        return int(id_str[-1])

    @staticmethod
    def initialize_items(description: str) -> list[int]:
        items_str = re.findall(r'Starting items: ((\d+\,? ?)+)', description)[0][0]
        return [int(item_str) for item_str in items_str.split(', ')]

    @staticmethod
    def define_operation(description: str) -> Callable[[int], int]:
        operator, mod = re.findall(r'Operation: new = old (\+|\*) (\d+|old)', description)[0]

        def operation(value):
            if mod == 'old':
                modd = value
            else:
                modd = int(mod)
                
            if operator == '*':
                #print(f'\t\tWorry level is multiplied by {modd} to {value * modd}')
                return value * modd
            elif operator == '+':
                #print(f'\t\tWorry level is increased by {modd} to {value * modd}')
                return value + modd
            else:
                raise ValueError(f'{operator} is not a supported operation')

        return operation

    @staticmethod
    def define_test(description:str) -> Callable[[int], int]:
        condition = int(re.findall(r'Test: divisible by (\d+)', description)[0])

        outcome_true = int(re.findall(r'If true: throw to monkey (\d+)', description)[0])
        outcome_false = int(re.findall(r'If false: throw to monkey (\d+)', description)[0])

        def test(item: int) -> int:
            if item % condition == 0:
                return outcome_true
            else:
                #print(f'\t\tCurrent worry level is not divisible by {condition}.')
                return outcome_false

        return test

    def inspect(self, item: int) -> int:
        item = self.operation(item)
        self.inspect_count += 1
        return item

    def get_bored_of(self, item:int) -> int:
        item = item // 3
        #print(f'\t\tMonkey gets bored with item. Worry level is divided by 3 to {item}')
        return item

    def pass_to(self, item, monkeys):
        receiving_monkey_id = self.test(item)
        #print(f'\t\tItem with worry level {item} is thrown to monkey {receiving_monkey_id}.')
        receiving_monkey = [monkey for monkey in monkeys if monkey.id == receiving_monkey_id][0]
        receiving_monkey.receive_item(item)

    def receive_item(self, item):
        self.items.append(item)

    def process_item(self, item, monkeys):
        #print(f'\tMonkey inspects an item with a worry level of {item}.')
        item = self.inspect(item)
        #item = self.get_bored_of(item)
        self.pass_to(item, monkeys)

    def take_turn(self, monkeys):
        #print(f'Monkey {self.id}:')
        for item in self.items:
            self.process_item(item, monkeys)

        self.items = []

    def __repr__(self):
        return f'Monkey {self.id}'


def process_input(file):
    with open(file) as f:
        lines = f.read()

    monkey_descriptions = lines.split("\n\n")
    return monkey_descriptions


def generate_monkeys(monkey_descriptions):
    monkeys = []
    for description in monkey_descriptions:
        monkeys.append(Monkey(description))

    return monkeys


def round(monkeys):
    for monkey in monkeys:
        monkey.take_turn(monkeys)


def main(file, rounds = 20):
    monkey_descriptions = process_input(file)
    monkeys = generate_monkeys(monkey_descriptions)

    for _ in tqdm(range(rounds)):
        round(monkeys)

    inspection_counts = []
    for monkey in monkeys:
        inspection_counts.append(monkey.inspect_count)

    inspection_counts = sorted(inspection_counts)
    monkey_business = inspection_counts[-1] * inspection_counts[-2]
    print(monkey_business)


if __name__ == '__main__':
    main(FILE, ROUNDS)