from tqdm import tqdm


INPUT_FILE = 'Day15/input.txt'

MARGIN = 50

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

class Map:
    def __init__(self, sensors_data):
        
        # Note that sensors_data in is in the form of {(x_sensor, y_sensor): (x_beacon, y_beacon)}
        # while the normalized sensors data is in the form of {(y_sensor, x_sensor): (y_beacon, x_beacon)}
        self.sensors_data = sensors_data
        self.sensors_data_norm, self.min_y, self.min_x, self.size, self.sensor_non_norm_to_norm = self.normalize_sensors_data(sensors_data)
        self.grid = self.generate_grid()


    @staticmethod
    def normalize_sensors_data(sensors_data):
        # find minimum_x and minimum_y
        min_x = min([min([sensor_pos[0], beacon_pos[0]]) for sensor_pos, beacon_pos in sensors_data.items()])
        min_y = min([min([sensor_pos[1], beacon_pos[1]]) for sensor_pos, beacon_pos in sensors_data.items()])

        # normalize_sensors_data
        sensors_data_norm = dict()
        sensor_dict_non_norm_to_norm = dict()
        for sensor_data in sensors_data.items():
            sensor_pos, beacon_pos = sensor_data
            sensors_pos_norm = (sensor_pos[1] - min_y + MARGIN, sensor_pos[0] - min_x + MARGIN)
            beacon_pos_norm = (beacon_pos[1] - min_y + MARGIN, beacon_pos[0] - min_x + MARGIN)

            sensors_data_norm[sensors_pos_norm] = beacon_pos_norm
            sensor_dict_non_norm_to_norm[sensor_pos] = sensors_pos_norm

        # find the length in y and x
        len_y = max([max([sensor_pos[0], beacon_pos[0]]) for sensor_pos, beacon_pos in sensors_data_norm.items()]) + 1 + MARGIN
        len_x = max([max([sensor_pos[1], beacon_pos[1]]) for sensor_pos, beacon_pos in sensors_data_norm.items()]) + 1 + MARGIN

        return sensors_data_norm, min_y, min_x, (len_y, len_x), sensor_dict_non_norm_to_norm


    def generate_grid(self):
        # Initialize an empty grid
        grid =  [['.' for column in range(self.size[1])] for row in range(self.size[0])]

        # Fill in sensors and beacons
        for sensor_position, beacon_position in self.sensors_data_norm.items():
            grid[sensor_position[0]][sensor_position[1]] = 'S'
            grid[beacon_position[0]][beacon_position[1]] = 'B'

        return grid


    def compute_all_coverage(self):
        for sensor_pos in tqdm(self.sensors_data.keys()):
            self.compute_sensor_coverage(sensor_pos)


    def compute_sensor_coverage(self, sensor_pos_non_norm):
        sensor_pos =  self.sensor_non_norm_to_norm[sensor_pos_non_norm]
        beacon_pos = self.sensors_data_norm[sensor_pos]

        distance = abs(sensor_pos[0] - beacon_pos[0]) + abs(sensor_pos[1] - beacon_pos[1])

        for row in range(self.size[0]):
            # the number of cells covered at this row
            n_cells_covered = (distance - abs(sensor_pos[0] - row)) * 2 + 1

            if n_cells_covered <= 0:
                continue

            # Define the positions in the row that are covered
            for column in range(sensor_pos[1] - n_cells_covered//2, sensor_pos[1] + n_cells_covered//2 + 1):
                if (column >= 0) and (column<self.size[1]) and (self.grid[row][column] == '.'):
                    self.grid[row][column] = '#'


    def print_grid(self):
        column_idxs =  [str(x) for x in range(self.min_x - MARGIN, self.min_x - MARGIN + self.size[1])]

        for i in range(len(max(column_idxs))+1):
            x_val = [x[i] if i < len(str(x)) else ' ' for x in column_idxs ]
            print(f'\t{" ".join(x_val)}')

        for i, row in enumerate(self.grid):
            print(f"{self.min_y - MARGIN + i}\t{' '.join(row)}")


def main(file):
    sensor_data = import_input(file)
    map = Map(sensor_data)
    map.compute_all_coverage()
    map.print_grid()


if __name__ == '__main__':
    main(INPUT_FILE)