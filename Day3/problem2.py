with open('Day3/input.txt') as f:
    rucksacks = [line.replace('\n', '') for line in f.readlines()]

badges = []
group_rucksack = []
for rucksack in rucksacks:
    group_rucksack.append(set(rucksack))

    if len(group_rucksack) == 3:
        badges.append(list(group_rucksack[0].intersection(group_rucksack[1]).intersection(group_rucksack[2]))[0])
        group_rucksack = []

print(badges)


def priority_lowercase(letter):
    return ord(letter) - ord('a') + 1


def priority_uppercase(letter):
    return ord(letter) - ord('A') + 27


def priority_score(letter):
    if letter.isupper():
        return priority_uppercase(letter)
    else:
        return priority_lowercase(letter)

total_priority = sum(map(priority_score, badges))

print(total_priority)
