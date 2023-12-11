from tools.grid import Grid
from tools.coordinate import (Coordinate, DistanceAlgorithm)
from tools.aoc import AOCDay
from typing import Any

class Universe(Grid):
    def insert_column(self, insert_x, new_column_count):
        affected_pos = sorted(
            [pos for pos in self.getActiveCells() if pos.x >= insert_x],
            key = lambda pos: pos.x,
            reverse = True,
        )
        
        for pos in affected_pos:
            self.move(pos, Coordinate(new_column_count - 1, 0))
            
    def insert_row(self, insert_y, new_row_count):
        affected_pos = sorted(
            [pos for pos in self.getActiveCells() if pos.y >= insert_y],
            key = lambda pos: pos.y,
            reverse = True,
        )
        
        for pos in affected_pos:
            self.move(pos, Coordinate(0, new_row_count - 1))
            
    def expand(self, replace_empty_with_count):
        galaxies = self.getActiveCells()
        
        for x in reversed(self.rangeX()):
            if len([g for g in galaxies if g.x == x]) == 0:
                self.insert_column(x, replace_empty_with_count)
        
        for y in reversed(self.rangeY()):
            if len([g for g in galaxies if g.y == y]) == 0:
                self.insert_row(y, replace_empty_with_count) 
        
    def path_sum(self):
        path_sum = 0
        started_from = set()
        
        for start in self.getActiveCells():
            started_from.add(start)
            for end in set(self.getActiveCells()) - started_from:
                path_sum += start.getDistanceTo(end, algorithm = DistanceAlgorithm.MANHATTAN)

        return path_sum                
        
class Day(AOCDay):
    inputs = [
        [
            (374, "input11-test"),
            (9686930, "input11"),
        ],
        [
            (8410, "input11-test"),
            (630728425490, "input11"),
        ]
    ]

    def part1(self) -> Any:
        universe = Universe.from_data(self.getInput(), default = '.')
        universe.expand(replace_empty_with_count = 2)
        return universe.path_sum()
        
    def part2(self) -> Any:
        universe = Universe.from_data(self.getInput(), default = '.')
        rewc = 1_000_000 if universe.getOnCount() > 10 else 100 # lower count for test
        universe.expand(replace_empty_with_count = rewc)
        return universe.path_sum()
        
if __name__ == '__main__':
    day = Day(2023, 11)
    day.run(verbose=True)
