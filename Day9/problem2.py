NUMBER_OF_KNOTS = 10

def import_input(file: str) -> list[str]:
    with open(file) as f:
        return [line.replace('\n', '') for line in f.readlines()]


class Knot:
    def __init__(self, x: int = 0, y: int = 0, parent_knot = None):
        self.x = x
        self.y = y
        self.parent_knot = parent_knot
        self.child_knot = None

        if parent_knot is not None:
            parent_knot._add_child(self)
            self.repr = 1 if parent_knot.repr == 'H' else parent_knot.repr + 1
        else:
            self.repr = 'H'


    def _add_child(self, knot):
        self.child_knot = knot


    def move(self, move_direction):
        if move_direction == 'U':
            self.y += 1
        elif move_direction == 'D':
            self.y -= 1
        elif move_direction == 'R':
            self.x += 1
        elif move_direction == 'L':
            self.x -= 1

        if self.child_knot is not None:
            self.child_knot.follow_parent()


    def follow_parent(self):
        if self.parent_knot is None:
            raise ValueError('This knot does not have a parent knot.')

        x_diff = self.parent_knot.x - self.x
        y_diff = self.parent_knot.y - self.y

        #move_x = x_diff > 1
        #move_y = y_diff > 1

        if x_diff > 1:
            self.x += 1
            if y_diff > 0:
                self.y += 1
            elif y_diff < 0:
                self.y -= 1
        elif x_diff < -1:
            self.x -= 1
            if y_diff > 0:
                self.y += 1
            elif y_diff < 0:
                self.y -= 1
        elif y_diff > 1:
            self.y += 1
            if x_diff > 0:
                self.x += 1
            elif x_diff < 0:
                self.x -= 1
        elif y_diff < -1:
            self.y -= 1
            if x_diff > 0:
                self.x += 1
            elif x_diff < 0:
                self.x -= 1

        if self.child_knot is not None:
            self.child_knot.follow_parent()

    def current_position(self):
        return self.x, self.y

    def __repr__(self):
        return f'{self.repr}, {self.current_position()}'


class Rope:
    def __init__(self, number_of_knots, x_init=0, y_init=0):
        self.knots = []
        for _ in range(number_of_knots):
            if len(self.knots) == 0:
                self.knots.append(Knot(x_init,y_init))
            else:
                self.knots.append(Knot(x_init,y_init, self.knots[-1]))

        self.head = self.knots[0]
        self.tail = self.knots[-1]

        self.x_init = x_init
        self.y_init = y_init


    def find_coordinate_limits(self):
        max_x = self.x_init
        min_x = self.x_init
        max_y = self.y_init
        min_y = self.y_init

        for knot in self.knots:
            if knot.x > max_x:
                max_x = knot.x
            elif knot.x < min_x:
                min_x = knot.x

            if knot.y > max_y:
                max_y = knot.y
            elif knot.y > min_y:
                min_y = knot.y

        return min_x, max_x, min_y, max_y


    def print_rope(self, grid_size: tuple[int] = (20, 20), start_pos=None):

        if start_pos == None:
            start_pos = grid_size[0] // 2 , grid_size[1] // 2
        start_x, start_y = start_pos

        grid = [['.' for row in range(grid_size[0])] for column in range(grid_size[1])]

        for knot in reversed(self.knots):
            knot_row = knot.y + start_y
            knot_col = knot.x + start_x

            if knot_row >= 0 and knot_col >= 0 and knot_row < grid_size[0] and knot_col < grid_size[1]:
               grid[knot_row][knot_col] = str(knot.repr)

        # Paint the starting position
        grid[start_y][start_x] = 'S'

        # Print the grid. We reverse it because we want increasing y going up
        print('\n==================================================')
        for row in reversed(grid):
            print(' '.join(row))
        print('==================================================\n')

    
    def print_positions(self):
        for knot in self.knots:
            print(knot.repr, knot.current_position())



def execute_command(rope, command: str):
    # Break down commands into direction and number of moves in that direction
    head_move_direction = command[0]
    number_of_movements = int(command[2:])

    # Execute the rope movement
    tail_positions_visited = set()
    for _ in range(number_of_movements):
        rope.head.move(head_move_direction)
        #rope.print_rope((100,100))
        tail_positions_visited.add(rope.tail.current_position())

    return tail_positions_visited



def main():
    input_file = 'Day9/input.txt'
    input = import_input(input_file)

    rope = Rope(NUMBER_OF_KNOTS)

    tail_positions_visited = set()
    for command in input:
        command_positions_visited = execute_command(rope, command)
        tail_positions_visited = tail_positions_visited.union(command_positions_visited)


    print(len(tail_positions_visited))


if __name__ == '__main__':
    main()