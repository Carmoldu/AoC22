INPUT_FILE = 'Day14/input.txt'

SAND_SOURCE = 500

GRID_X_MARGIN = 2
GRID_DEPTH_MARGIN = 2

MAX_ITER = 100000000000

def process_input(file):
    with open(file) as f:
        raw_rock_formations = [
            [tuple(map(int, node.split(',')[::-1])) for node in rock_formation.replace('\n', '').split(' -> ')] 
            for rock_formation in f.readlines()
        ]
    
    return raw_rock_formations

def initialize_cave(raw_rock_formations, grid_x_margin, grid_depth_margin, spawn_floor=False):
    if spawn_floor:
        raw_rock_formations.append(generate_floor(raw_rock_formations))

    # Find min x and depth 
    min_x = min([x for raw_rock_formation in raw_rock_formations for depth, x in raw_rock_formation]) - grid_x_margin
    min_depth =  0 # min([depth for raw_rock_formation in raw_rock_formations for depth, x in raw_rock_formation]) - grid_depth_margin

    # We will set all values with respect to the min for simplicity.
    rock_formations = [[(depth - min_depth, x - min_x) for depth, x in raw_rock_formation] for raw_rock_formation in raw_rock_formations]

    # Find max x and depth to initialize the grid
    max_x = max([x for rock_formation in rock_formations for depth, x in rock_formation]) + grid_x_margin
    max_depth = max([depth for rock_formation in rock_formations for depth, x in rock_formation]) + grid_depth_margin

    # Initialize the cave
    cave =  [['.' for x in range(max_x + 1)] for depth in range(max_depth + 1)]
    cave = spawn_rock_formations(cave, rock_formations)

    return cave, min_x, min_depth


def generate_floor(raw_rock_formations):
    # Since we cannot generate an infinite floor, we compute the maximum and minimum theoretical x the sand can get to,
    # which is equal to the min_x - depth and max_x + depth
    min_x = min([x for raw_rock_formation in raw_rock_formations for depth, x in raw_rock_formation])
    max_x = max([x for raw_rock_formation in raw_rock_formations for depth, x in raw_rock_formation])
    min_depth =  0
    max_depth = max([depth for raw_rock_formation in raw_rock_formations for depth, x in raw_rock_formation])

    floor_min_x = min_x - (max_depth - min_depth)
    floor_max_x = max_x + (max_depth - min_depth)
    floor_depth = max_depth + 2

    return [(floor_depth, floor_min_x), (floor_depth, floor_max_x)]

def spawn_rock_formations(cave, rock_formations):
    # Populate the grid with rock formations
    for rock_formation in rock_formations:
        cave = spawn_rock_formation(cave, rock_formation)

    return cave


def spawn_rock_formation(cave, rock_formation):
    for i in range(len(rock_formation)-1):
        start_depth, start_x = (rock_formation[i])
        end_depth, end_x = rock_formation[i+1]

        if (start_x == end_x) and (start_depth != end_depth): 
            cave = spawn_vertical_rock_formation(cave, start_x, start_depth, end_depth)
        elif (start_x != end_x) and (start_depth == end_depth):
            cave = spawn_horizontal_rock_formation(cave, start_depth, start_x, end_x)

    return cave


def spawn_vertical_rock_formation(cave, x, start_depth, end_depth):
    min_depth = min((start_depth, end_depth))
    max_depth = max((start_depth, end_depth))
    for depth in range(min_depth, max_depth + 1):
        cave[depth][x] = '#'
    return cave


def spawn_horizontal_rock_formation(cave, depth, start_x, end_x):
    min_x = min((start_x, end_x))
    max_x = max((start_x, end_x))
    for x in range(min_x, max_x + 1):
        cave[depth][x] = '#'
    return cave


def drop_n_sand_grains(n, cave, x_drop):
    for i in range(n):
        cave, unobstructed = drop_one_sand_grain(cave, x_drop)
        if unobstructed:
            break

    return cave, i

def drop_one_sand_grain(cave, x_drop):
    current_x = x_drop
    current_depth = 0
    while True:
        # Look for the index of the first obstacle
        obstacle_depth = find_first_column_obstacle(current_x, current_depth, cave)

        # If an obstacle was found, we check the column on the left. if it is lower,
        # the sand slips towards that column
        left_obstacle_depth = find_first_column_obstacle(current_x - 1, current_depth, cave)

        # If no obstacle was found, we return the cave and flag set to true
        if left_obstacle_depth == None:
            return cave, True

        if left_obstacle_depth > obstacle_depth:
            current_x -= 1#
            current_depth = left_obstacle_depth - 1
            continue

        # We do the same for the right column 
        right_obstacle_depth = find_first_column_obstacle(current_x + 1, current_depth, cave)

        if right_obstacle_depth == None:
            return cave, True

        if right_obstacle_depth > obstacle_depth:
            current_x += 1
            current_depth = right_obstacle_depth - 1
            continue

        # If right and left columns are the same level or higher, The sand gets stuck
        cave[obstacle_depth - 1][current_x] = 'o'

        # stop if the  sand gets stuck at depth 0
        if (obstacle_depth - 1) == 0:
            return cave, True

        return cave, False


def find_first_column_obstacle(column_idx, current_depth, cave):
    column = [row[column_idx] for row in cave][current_depth + 1:]

    # Look for a non empty space
    for i, val in enumerate(column):
        if val != '.':
            break
    
    # Manage the case where the sand does not find any obstacle
    if i == len(column) - 1:
        return None

    return i + current_depth + 1

def print_cave(cave, min_x=0, min_depth=0):
    x_values =  [str(x) for x in range(min_x, min_x + len(cave[0]))]

    for i in range(len(max(x_values))+1):
        x_val = [x[i] if i < len(str(x)) else ' ' for x in x_values ]
        print(f'\t{" ".join(x_val)}')

    for i, depth in enumerate(cave):
        print(f"{min_depth + i}\t{' '.join(depth)}")


def save_cave_to_file(savefile, cave, min_x=0, min_depth=0):
    with open(savefile, 'w') as f:
        x_values =  [str(x) for x in range(min_x, min_x + len(cave[0]))]

        for i in range(len(max(x_values))+1):
            x_val = [x[i] if i < len(str(x)) else ' ' for x in x_values ]
            f.write(f'\t{" ".join(x_val)}\n')

        for i, depth in enumerate(cave):
            f.write(f"{min_depth + i}\t{' '.join(depth)}\n")


def main(input_file):
    raw_rock_formations = process_input(input_file)

    # cave1, min_x, min_depth = initialize_cave(raw_rock_formations, GRID_X_MARGIN, GRID_DEPTH_MARGIN)
    # cave1, iterations1 = drop_n_sand_grains(MAX_ITER, cave1, SAND_SOURCE - min_x)
    # print_cave(cave1)
    # print(iterations1)

    cave2, min_x, min_depth = initialize_cave(raw_rock_formations, GRID_X_MARGIN, GRID_DEPTH_MARGIN, True)
    cave2, iterations2 = drop_n_sand_grains(MAX_ITER, cave2, SAND_SOURCE - min_x)
    save_cave_to_file('cave2.txt', cave2)
    print(iterations2)


if __name__ == '__main__':
    main(INPUT_FILE)

