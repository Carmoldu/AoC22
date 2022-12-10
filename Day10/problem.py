def read_input(input_file):
    with open(input_file) as f:
        return [line.replace('\n', '') for line in f.readlines()]


class Cpu:
    def __init__(self, crt):
        self.cycle = 0
        self.x = 1
        self.x_history = [self.x]

        self.crt = crt

    def process_input(self, command):
        if command[:4] == 'noop':
            self.execute_noop()
        elif command[:4] == 'addx':
            self.execute_addx(int(command[5:]))
        else:
            raise ValueError(f'{command} could not be interpreted')

    def execute_noop(self):
        self.register_cycle_x()
        self.execute_cycle()


    def execute_addx(self, val: int, cicles: int = 2):
        for _ in range(cicles):  
            self.register_cycle_x()
            self.execute_cycle()
        
        self.x += val


    def execute_cycle(self):
        self.crt.process_cycle(self.cycle, self.x)
        self.cycle += 1
        

    def register_cycle_x(self):
        self.x_history.append(self.x)


    def retrieve_cycles_strength(self, cycles: list[int]) -> list[int]:
        return [x * cycle for cycle, x in enumerate(self.x_history) if cycle in cycles]


class Crt():
    def __init__(self, pixel_size=(6, 40)):
        self.rows = pixel_size[0]
        self.columns = pixel_size[1]
        self.grid = [['.' for column in range(self.columns)] for row in range(self.rows)]

    
    def active_pixel_from_cycle(self, cycle: int):
        row = cycle // self.columns
        column = cycle % self.columns# -1 because we are using 0 - index

        return row, column


    def process_cycle(self, cycle, cpu_x):
        active_pixel_row, active_pixel_column = self.active_pixel_from_cycle(cycle)

        if active_pixel_row >= self.rows:
            return

        if (cpu_x - 1) <= active_pixel_column <= (cpu_x + 1):
            self.grid[active_pixel_row][active_pixel_column] = '#'
        else:
            self.grid[active_pixel_row][active_pixel_column] = '.'


    def print_grid(self):
        print('\n==================================================')
        for row in self.grid:
            print(' '.join(row))
        print('==================================================\n')


def main(input_file):
    input = read_input(input_file)
    crt = Crt()
    cpu = Cpu(crt=crt)

    for command in input:
        cpu.process_input(command)

    cycles_of_interest = [20 + 40*i for i in range(0, 50)]
    print(sum(cpu.retrieve_cycles_strength(cycles_of_interest)))

    crt.print_grid()


if __name__ == '__main__':
    input_file = 'Day10/input.txt'
    main(input_file)