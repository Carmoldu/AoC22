# Rules definition
rules = {
    'X': {'wins':'C', 'draw': 'A', 'points': 1},
    'Y': {'wins':'A', 'draw': 'B', 'points': 2},
    'Z': {'wins':'B', 'draw': 'C', 'points': 3},
}

outcome_points = {
    'win': 6,
    'draw': 3,
    'loss': 0
}

# Import the hands
with open('Day2/input.txt') as f:
    hands = [line.replace('\n', '').split(' ') for line in f.readlines()]

# Compute the score
score = 0
for hand in hands:
    hand_played_rules = rules[hand[1]]

    score += hand_played_rules['points']
    if hand_played_rules['draw'] == hand[0]:
        score += outcome_points['draw']
    elif hand_played_rules['wins'] == hand[0]:
        score += outcome_points['win']
    else:
        score += outcome_points['loss']

print(f'Total score: {score}')

# New tules (problem 2)
new_rules = {
    'Z': {'A': outcome_points['win'] + 2, 'B': outcome_points['win'] + 3, 'C': outcome_points['win'] + 1},
    'Y': {'A': outcome_points['draw'] + 1, 'B': outcome_points['draw'] + 2, 'C': outcome_points['draw'] + 3},
    'X': {'A': outcome_points['loss'] + 3, 'B': outcome_points['loss'] + 1, 'C': outcome_points['loss'] + 2},
}

score = 0
for hand in hands:
    score += new_rules[hand[1]][hand[0]]

print(f'Total score: {score}')