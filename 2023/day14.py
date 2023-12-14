from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any

tilt_directions = {
    "north": {
        "movement": Coordinate(0, -1),
        "sort": lambda p: p.y,
    },
    "west": {
        "movement": Coordinate(-1, 0),
        "sort": lambda p: p.x,
    },
    "south": {
        "movement": Coordinate(0, 1),
        "sort": lambda p: -p.y,
    },
    "east": {
        "movement": Coordinate(1, 0),
        "sort": lambda p: -p.x,
    },
}

def tilt(grid, direction):
    pos_move = tilt_directions[direction]["movement"]
    all_pos = sorted(grid.getActiveCells(), key = tilt_directions[direction]["sort"])
    
    for pos in all_pos:
        if grid.get(pos) == "O":
            try_pos = pos + pos_move
            while grid.get(try_pos) == ".":
                grid.set(try_pos, "O")
                grid.set(try_pos - pos_move, ".")
                try_pos += pos_move
            
def run_cycle(grid):
    for dir in ["north", "west", "south", "east"]:
        tilt(grid, dir)    
        
def load_after_cycles(grid, cycle_count):
    grid_configurations = []
    
    cycle = 1
    match = False
    while cycle <= cycle_count:
        run_cycle(grid)
        
        conf = [grid.get(pos) for pos in sorted(grid.getActiveCells())]
        grid_configurations += [conf]
        
        cycle += 1
        
        if not match and grid_configurations.count(conf) == 2:
            i1, i2 = [i for i, c in enumerate(grid_configurations) if c == conf]
            print(f"repeat from {i1} to {i2}")
        
            cycle_len = i2 - i1
            skip = (cycle_count - cycle) // cycle_len
            print(f"skip cycle from {cycle} to {cycle + cycle_len * skip}")
            cycle += cycle_len * skip
            match = True
        
    return load(grid)
            
def load(grid):
    return sum(
        (grid.maxY + 1) - pos.y
        for pos in grid.getActiveCells()
        if grid.get(pos) == "O"
    )
    
class Day(AOCDay):
    inputs = [
        [
            (136, "input14-test"),
            (110565, "input14"),
        ],
        [
            (64, "input14-test"),
            (89845, "input14"),
        ]
    ]

    def part1(self) -> Any:
        grid = Grid.from_data(self.getInput(), default = "X")
        tilt(grid, "north")
        return load(grid)

    def part2(self) -> Any:
        grid = Grid.from_data(self.getInput(), default = "X")
        return load_after_cycles(grid, 1_000_000_000)


if __name__ == '__main__':
    day = Day(2023, 14)
    day.run(verbose=True)
