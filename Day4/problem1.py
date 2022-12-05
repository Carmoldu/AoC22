
from typing import Callable


def separate_assignments(input_line: str) -> tuple[str]:
    return tuple(input_line.replace('\n', '').split(','))


def extract_assignment_range_limits(assignment: str) -> tuple[int]:
    return tuple(map(int, assignment.split('-')))


CheckFunction = Callable[[tuple[int], tuple[int]], bool]


def assignment_contained_within(assignment_limits: tuple[int], reference_limits: tuple[int]) -> bool:
    return (assignment_limits[0] >= reference_limits[0]) and (assignment_limits[1] <= reference_limits[1])


def assignments_overlap(assignment1_limits: tuple[int], assignment2_limits: tuple[int]) -> bool:
    return (
        ((assignment1_limits[0] >= assignment2_limits[0]) and (assignment1_limits[0] <= assignment2_limits[1]))
        | ((assignment1_limits[1] >= assignment2_limits[0]) and (assignment1_limits[1] <= assignment2_limits[1]))
    )


def process_input_line(assignment_pair: str, check_function: CheckFunction) -> tuple[tuple[int]]:
    # Separate pairs of assignments
    assignment1, assignment2 = separate_assignments(assignment_pair)

    # Extract min and max area assigned
    assignment1_limits = extract_assignment_range_limits(assignment1)
    assignment2_limits= extract_assignment_range_limits(assignment2)

    return (
        check_function(assignment1_limits, assignment2_limits)
        | check_function(assignment2_limits, assignment1_limits)
    )

def process_input(input_file, check_function: CheckFunction) -> list[bool]:
    processed_input = []
    with open(input_file) as f:
        for assignment_pair in f.readlines():
            processed_input.append(process_input_line(assignment_pair, check_function))

    return processed_input
        


def main(input_file):
    processed_input1 = process_input(input_file, assignment_contained_within)
    print(sum(processed_input1))

    processed_input2 = process_input(input_file, assignments_overlap)
    print(sum(processed_input2))

if __name__ == '__main__':
    input_file = 'Day4/input.txt'
    main(input_file)