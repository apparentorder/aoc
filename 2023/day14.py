from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any

def tilt(grid, direction):
    all_pos = grid.getActiveCells()
    all_pos.sort()
    
    for pos in all_pos:
        if grid.get(pos) == "O":
            try_pos = pos + direction
            while grid.get(try_pos) == ".":
                grid.set(try_pos, "O")
                grid.set(try_pos - direction, ".")
                try_pos += direction
                
def load(grid):
    l = 0
    for pos in grid.getActiveCells():
        if grid.get(pos) == "O":
            l += (grid.maxY + 1) - pos.y
        
    return l
    
class Day(AOCDay):
    inputs = [
        [
            (136, "input14-test"),
            (110565, "input14"),
        ],
        [
            (64, "input14-test"),
            (None, "input14"),
        ]
    ]

    def part1(self) -> Any:
        grid = Grid.from_data(self.getInput(), default = "X")
        tilt(grid, Coordinate(0, -1))
        grid.print()
        return load(grid)

    def part2(self) -> Any:
        return ""


if __name__ == '__main__':
    day = Day(2023, 14)
    day.run(verbose=True)
