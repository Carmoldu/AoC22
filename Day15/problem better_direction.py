from tqdm import tqdm

INPUT_FILE = 'Day15/input.txt'


def import_input(file):
    with open(file) as f:
        raw_sensors_data = [line.replace('\n', '') for line in f.readlines()]

    sensors_data = dict()
    for raw_sensor_data in raw_sensors_data:
        raw_sensor_info, raw_beacon_info = tuple(raw_sensor_data.replace('Sensor at x=', '').replace('closest beacon is at x=', '').split(': '))

        sensor_info = tuple([int(coord_info) for coord_info in raw_sensor_info.split(', y=')])
        beacon_info = tuple([int(coord_info) for coord_info in raw_beacon_info.split(', y=')])

        sensors_data[sensor_info] = beacon_info

    return sensors_data


def compute_sensor_distance(sensor_pos, beacon_pos):
    return abs(sensor_pos[0] - beacon_pos[0]) + abs(sensor_pos[1] - beacon_pos[1])


def compute_sensors_distance(sensors_data):
    sensors_distances = dict()
    for sensor_pos, beacon_pos in sensors_data.items():
        sensors_distances[sensor_pos] = compute_sensor_distance(sensor_pos, beacon_pos)

    return sensors_distances


def compute_positions_occupied_in_row(row, sensors_data, sensors_distance):
    # First, record if the objects are in that row
    beacons_and_sensors = set()
    for sensor_pos, beacon_pos in sensors_data.items():
        if sensor_pos[1] == row:
            beacons_and_sensors.add(sensor_pos[0])

        if beacon_pos[1] == row:
            beacons_and_sensors.add(beacon_pos[0])


    # Now, compute based on the distance how many positions would eqach sensor cover
    positions_occupied = set()
    for sensor_pos, beacon_pos in sensors_data.items():
        
        n_cells_covered = (sensors_distance[sensor_pos] - abs(sensor_pos[1] - row)) * 2 + 1

        if n_cells_covered <= 0:
            continue

        # Define the positions in the row that are covered
        positions_occupied = positions_occupied.union(set(range(sensor_pos[0] - n_cells_covered//2, sensor_pos[0] + n_cells_covered//2 + 1)).difference(beacons_and_sensors))

    return positions_occupied


def main(file):
    sensors_data = import_input(file)
    sensors_distance = compute_sensors_distance(sensors_data)
    print(len(compute_positions_occupied_in_row(2000000, sensors_data, sensors_distance)))

    # this obviously takes too long
    x_range = set(range(0, 4000001))
    possible_positions = []
    for row in tqdm(range(0, 4000000)):
        free_spaces_in_x_range = compute_positions_occupied_in_row(row, sensors_data, sensors_distance).difference(x_range)

        possible_positions += [(row, x) for x in free_spaces_in_x_range]

    print(possible_positions)


if __name__ == '__main__':
    main(INPUT_FILE)