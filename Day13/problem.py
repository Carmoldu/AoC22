import re
from itertools import zip_longest
from functools import cmp_to_key

INPUT_FILE = 'Day13/input.txt'

DIVIDER_PACKET_1 = '[[2]]'
DIVIDER_PACKET_2 = '[[6]]'

def process_input(file):
    with open(file) as f:
        file_content = f.read()

    lines_pairs = file_content.split("\n\n")
    for i, lines_pair in enumerate(lines_pairs):
        lines_pairs[i] = lines_pair.split('\n')

    return lines_pairs


def process_input2(file):
    with open(file) as f:
        file_content = f.read()

    lines_pairs = file_content.replace("\n\n", '\n').split('\n')

    return lines_pairs


def evaluate_lists(left, right):
    for left_element, right_element in zip_longest(left, right):
        # Check if the left list has elements and the right one doesn't
        if left_element is None and not right_element is None:
            return -1
        elif not left_element is None and right_element is None:
            return 1

        # if one element is a list and the other is an int, the int shall be changed to a
        # list containing the int
        if isinstance(left_element, list) and not isinstance(right_element, list):
            right_element = [right_element]
        elif isinstance(right_element, list) and not isinstance(left_element, list):
            left_element = [left_element]

        # If both lists still have elements, compare them
        if isinstance(left_element, int) and isinstance(right_element, int):
            if left_element < right_element:
                return -1
            elif left_element > right_element:
                return 1
            else:
                continue

        if isinstance(left_element, list) and isinstance(right_element, list):
            out = evaluate_lists(left_element, right_element)
            if not out is None:
                return out
            else:
                continue
    # If we go through all elements and we could not make a decision, return none
    # so that we can go thorugh the analysis in upper levels
    return None


def compare_codes(left, right):
    return evaluate_lists(eval(left), eval(right))

def main(file):
    lines_pairs = process_input(file)

    ordered_pairs = []
    for i, pair in enumerate(lines_pairs):
        if compare_codes(pair[0], pair[1]) > 0:
            ordered_pairs.append(i+1)

    print(sum(ordered_pairs), ordered_pairs)

    lines_pairs = process_input2(file)
    lines_pairs.append(DIVIDER_PACKET_1)
    lines_pairs.append(DIVIDER_PACKET_2)
    sorted_lines_pairs = sorted(lines_pairs, key=cmp_to_key(compare_codes))

    idx_1 = sorted_lines_pairs.index(DIVIDER_PACKET_1) + 1
    idx_2 = sorted_lines_pairs.index(DIVIDER_PACKET_2) + 1

    print(idx_1, idx_2, idx_1 * idx_2)

if __name__ == '__main__':
    main(INPUT_FILE)