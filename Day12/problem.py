import numpy as np


INPUT_FILE = 'Day12/input.txt'

STARTING_POSITION_MARKER = 'S'
STARTING_POSITION_HEIGHT = 'a'
ENDING_POSITION_MARKER = 'E'
ENDIGN_POSITION_HEIGHT = 'z'


def process_input(input_file):
    with open(input_file) as f:
        return np.array([list(line.replace('\n', '')) for line in f.readlines()])
    

def process_height_map(height_map_str):
    # Find starting and ending positions
    starting_pos = np.where(height_map_str == STARTING_POSITION_MARKER) 
    ending_pos = np.where(height_map_str == ENDING_POSITION_MARKER)
    
    # We convert these to tuples because it will be easier to work with that in the long run
    starting_pos = (starting_pos[0][0], starting_pos[1][0])
    ending_pos = (ending_pos[0][0], ending_pos[1][0])

    # Replace starting and ending positions with their height
    height_map_str[starting_pos] = STARTING_POSITION_HEIGHT
    height_map_str[ending_pos] = ENDIGN_POSITION_HEIGHT
    
    # Translate the height map to numbers to make it easier to work with
    height_map_int = height_map_str.view(np.int32) - np.full(height_map_str.shape, ord('a'))

    return starting_pos, ending_pos, height_map_int


def find_neightboring_cells(current_cell, grid_shape):
    row, column = current_cell

    neightbor_cells = []
    if row > 0:
        neightbor_cells.append((row - 1, column))
    if row < grid_shape[0] - 1:
        neightbor_cells.append((row + 1, column))
    if column > 0:
        neightbor_cells.append((row, column - 1))
    if column < grid_shape[1] - 1:
        neightbor_cells.append((row, column + 1))

    return neightbor_cells


def valid_paths_uphill(active_cell, neightboring_cells, height_map):
    return [neightboring_cell for neightboring_cell in neightboring_cells if height_map[neightboring_cell] <= (height_map[active_cell] + 1)]


def valid_paths_downhill(active_cell, neightboring_cells, height_map):
    return [neightboring_cell for neightboring_cell in neightboring_cells if height_map[neightboring_cell] >= (height_map[active_cell] -1)]


def unvisited_neightboring_cells(cells_evaluated, visited_cells):
    return [cell for cell in cells_evaluated if cell not in visited_cells.keys()]


def evaluate_active_cell_neightbors(active_cell, height_map, visited_cells, valid_path_strategy):
    neightboring_cells = find_neightboring_cells(active_cell, height_map.shape)    
    valid_neightboring_cells = valid_path_strategy(active_cell, neightboring_cells, height_map)
    valid_unvisited_neightboring_cells = unvisited_neightboring_cells(valid_neightboring_cells, visited_cells)

    return valid_unvisited_neightboring_cells


def update_visited_cells(active_cell, new_cells, visited_cells):
    path_to_new_cells = visited_cells[active_cell] + [active_cell]

    for new_cell in new_cells:
        visited_cells[new_cell] = path_to_new_cells


def find_all_paths_given_starting_point(starting_pos, height_map, valid_paths_strategy, iter_limit=10000):
    visited_cells = {starting_pos: []}
    active_cells = [starting_pos]

    for _ in range(iter_limit):
        while len(active_cells) > 0:
            active_cell = active_cells.pop(0)
            new_cells = evaluate_active_cell_neightbors(active_cell, height_map, visited_cells, valid_paths_strategy)
            update_visited_cells(active_cell, new_cells, visited_cells)
            active_cells += new_cells

    return visited_cells


def main(input_file):
    starting_pos, ending_pos, height_map = process_height_map(process_input(input_file))
    paths = find_all_paths_given_starting_point(starting_pos, height_map, valid_paths_uphill)
    print(len(paths[ending_pos]))

    paths = find_all_paths_given_starting_point(ending_pos, height_map, valid_paths_downhill)
    shortest_path = float('inf')
    for cell in zip(*np.where(height_map == 0)):
        if (cell in list(paths.keys())) and (len(paths[cell]) < shortest_path):
            shortest_path = int(len(paths[cell]))
    print(shortest_path)


if __name__ == '__main__':
    main(INPUT_FILE)