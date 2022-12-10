
from dataclasses import dataclass


def import_input(file: str) -> list[str]:
    with open(file) as f:
        return [line.replace('\n', '') for line in f.readlines()]


@dataclass
class RopeEnd():
    x: int
    y: int

    @staticmethod
    def vector_distance(tail, head):
        return head.x - tail.x, head.y - tail.y


def execute_command(head: RopeEnd, tail: RopeEnd, command: str):
    # Break down commands into direction and number of moves in that direction
    head_move_direction = command[0]
    number_of_movements = int(command[2:])

    # Execute the rope movement
    tail_positions_visited = set()
    for _ in range(number_of_movements):
        head = move(head, head_move_direction)
        tail = tail_movement(tail, head)

        tail_positions_visited.add((tail.x, tail.y))

    return head, tail, tail_positions_visited


def move(rope_end: RopeEnd, move_direction: str):
    if move_direction == 'U':
        rope_end.y += 1
    elif move_direction == 'D':
        rope_end.y -= 1
    elif move_direction == 'R':
        rope_end.x += 1
    elif move_direction == 'L':
        rope_end.x -= 1

    return rope_end


def tail_movement(tail, head):
    x_diff, y_diff = RopeEnd.vector_distance(tail, head)

    if x_diff > 1:
        tail.x += 1
        tail.y = head.y
    elif x_diff < -1:
        tail.x -= 1
        tail.y = head.y
    
    if y_diff > 1:
        tail.y += 1
        tail.x = head.x
    elif y_diff < -1:
        tail.y -= 1
        tail.x = head.x

    return tail



def main():
    input_file = 'Day9/input.txt'
    input = import_input(input_file)

    head = RopeEnd(0, 0)
    tail = RopeEnd(0, 0)

    total_positions_visited = set()
    for command in input:
        head, tail, command_positions_visited = execute_command(head, tail, command)
        total_positions_visited = total_positions_visited.union(command_positions_visited)

    print(len(total_positions_visited))


if __name__ == '__main__':
    main()