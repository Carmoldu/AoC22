import numpy as np


def import_input(file: str) -> list[str]:
    with open(file) as f:
        return np.array([[int(tree_height) for tree_height in list(line.replace('\n', ''))] for line in f.readlines()])


def is_visible(y, x, grid):
    # Catch edges
    if (x == 0) or (y == 0) or (x == grid.shape[1]) or (y == grid.shape[0]):
        return True

    trees_north = grid[:y,x]
    trees_south = grid[y+1:,x]
    trees_west = grid[y,:x]
    trees_east = grid[y,x+1:]

    tree_height = grid[y,x]

    return(
        all(trees_north < tree_height)
        or all(trees_south < tree_height)
        or all(trees_west < tree_height)
        or all(trees_east < tree_height)
        )


def scenic_score(y, x, grid):
    # Catch edges
    if (x == 0) or (y == 0) or (x == grid.shape[1]) or (y == grid.shape[0]):
        return True
    
    trees_north = grid[:y,x][::-1] if (y > 0) else np.array([])
    trees_south = grid[y+1:,x] if (y < grid.shape[0]) else np.array([])
    trees_west = grid[y,:x][::-1] if (x > 0) else np.array([])
    trees_east = grid[y,x+1:] if (x < grid.shape[1]) else np.array([])

    tree_height = grid[y, x]

    return (visibility(tree_height, trees_north) 
            * visibility(tree_height, trees_south) 
            * visibility(tree_height, trees_east) 
            * visibility(tree_height, trees_west)
            )


def  visibility(tree_height, view):
    visibility = 0
    for tree in view:
        visibility += 1
        if tree >= tree_height:
            return visibility

    return visibility


def main():
    input_file = 'Day8/input.txt'
    input = import_input(input_file)
    print(input)

    count_visible = 0
    scenic_scores = np.empty(shape=input.shape)
    for y in range(input.shape[0]):
        for x in range(input.shape[1]):
            count_visible += int(is_visible(y, x, input))
            scenic_scores[y,x] = scenic_score(y, x, input)


    print(count_visible, input.size - count_visible)
    print(scenic_scores)
    print(scenic_scores.max())


if __name__ == '__main__':
    main()