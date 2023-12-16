from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any
    
class Beam:
    def __init__(self, cavern, start, heading):
        self.cavern = cavern
        self.pos = start
        self.heading = heading
        self.energize()
        
    def energize(self):
        while self.cavern.isWithinBoundaries(self.pos):
            epbh = self.cavern.energized_pos_by_heading.setdefault(self.pos, set())
            if self.heading in epbh:
                # BTDT
                break
            
            epbh.add(self.heading)
            self.cavern.energized_pos_by_heading[self.pos] = epbh
                
            c = self.cavern.get(self.pos)
            if c == "|" and self.heading.y == 0:
                self.cavern.add_beam(self.pos, Coordinate(0, -1))
                self.cavern.add_beam(self.pos, Coordinate(0, 1))
                break
            elif c == "-" and self.heading.x == 0:
                self.cavern.add_beam(self.pos, Coordinate(-1, 0))
                self.cavern.add_beam(self.pos, Coordinate(1, 0))
                break
            elif c == "/":
                self.heading = Coordinate(-self.heading.y, -self.heading.x)
            elif c == "\\":
                self.heading = Coordinate( self.heading.y,  self.heading.x)
                
            self.pos += self.heading
                
class Cavern(Grid):
    def add_beam(self, start, heading):
        self.beams += [Beam(self, start, heading)]
        return self.beams[-1]
        
    def initialize(self):
        self.beams = []
        self.energized_pos_by_heading = {}
        
class Day(AOCDay):
    inputs = [
        [
            (46, "input16-test"),
            (8539, "input16"),
        ],
        [
            (51, "input16-test"),
            (8674, "input16"),
        ]
    ]

    def part1(self) -> Any:
        cavern = Cavern.from_data(self.getInput())
        cavern.initialize()
        cavern.add_beam(start = Coordinate(0, 0), heading = Coordinate(1, 0))
        # cavern.print(mark = cavern.energized_pos_by_heading)
        return len(cavern.energized_pos_by_heading)

    def part2(self) -> Any:
        cavern = Cavern.from_data(self.getInput())
        
        max_tiles = 0
        edge_pos = set()
        for x in cavern.rangeX(): edge_pos.add(Coordinate(x, 0))
        for x in cavern.rangeX(): edge_pos.add(Coordinate(x, cavern.maxY))
        for y in cavern.rangeY(): edge_pos.add(Coordinate(0, y))
        for y in cavern.rangeY(): edge_pos.add(Coordinate(cavern.maxX, y))
        
        for ep in edge_pos:
            try_headings = []
            if ep.x == 0:           try_headings += [Coordinate( 1, 0)]
            if ep.x == cavern.maxX: try_headings += [Coordinate(-1, 0)]
            if ep.y == 0:           try_headings += [Coordinate( 0, 1)]
            if ep.y == cavern.maxY: try_headings += [Coordinate( 0,-1)]
            
            for heading in try_headings:
                cavern.initialize()
                cavern.add_beam(start = ep, heading = heading)
                max_tiles = max(max_tiles, len(cavern.energized_pos_by_heading))
                    
        return max_tiles


if __name__ == '__main__':
    day = Day(2023, 16)
    day.run(verbose=True)
