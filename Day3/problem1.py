with open('Day3/input.txt') as f:
    rucksacks = [line.replace('\n', '') for line in f.readlines()]

misplaced_objects = []
for rucksack in rucksacks:
    n_items = len(rucksack)
    left_compartment = set(rucksack[:n_items//2])
    right_compartment = set(rucksack[n_items//2:])

    misplaced_objects.append(list(left_compartment.intersection(right_compartment))[0])

print(misplaced_objects)


def priority_lowercase(letter):
    return ord(letter) - ord('a') + 1


def priority_uppercase(letter):
    return ord(letter) - ord('A') + 27


def priority_score(letter):
    if letter.isupper():
        return priority_uppercase(letter)
    else:
        return priority_lowercase(letter)

total_priority = sum(map(priority_score, misplaced_objects))

print(total_priority)
