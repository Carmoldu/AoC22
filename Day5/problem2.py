import re

def process_initial_state(file):
    stacks = {n:[] for n in range(1,10)}
    with open(file) as f:
        for line in f.readlines():
            for stack in stacks:
                stack_content = line[(stack - 1) * 3 + stack]

                if stack_content == ' ':
                    continue

                stacks[stack].insert(0, stack_content)

    return stacks


def process_planned_moves(file):
    with open(file) as f:
        moves = [tuple(map(int, re.findall(r'\d+', line))) for line in f.readlines()]

    return moves


def remove_blocks(stack, n_blocks):
    return stack[:-n_blocks], stack[-n_blocks:]


def add_blocks(stack, blocks):
    return stack + blocks


def execute_moves(stacks, moves):
    for n_blocks, from_stack, to_stack in moves:
        stacks[from_stack], blocks_being_moved = remove_blocks(stacks[from_stack], n_blocks)
        stacks[to_stack] = add_blocks(stacks[to_stack], blocks_being_moved)

    return stacks
        

def main():
    stacks = process_initial_state('Day5/input_stacks.txt')
    moves = process_planned_moves('Day5/input_moves.txt')

    stacks = execute_moves(stacks, moves)

    print([stack[-1] for stack in stacks.values()])


if __name__ == '__main__':
    main()