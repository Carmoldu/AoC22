def load_input(file):
    with open(file) as f:
        datastream = f.readline()
    return datastream


def find_marker(datastream, marker_len=4):
    pointer = 0
    while pointer <= (len(datastream) - marker_len):
        chars_analysed = datastream[pointer:pointer + marker_len] 
        if len(set(chars_analysed)) == marker_len:
            return pointer + marker_len

        pointer += 1
    return None


def main():
    file = 'Day6/input.txt'
    datastream = load_input(file)

    marker = find_marker(datastream)
    print(marker)

    marker = find_marker(datastream, 14)
    print(marker)


if __name__ == '__main__':
    main()