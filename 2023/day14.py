from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any

class RockMap:
    cycle_directions = [
        (0, -1), # north
        (-1, 0), # west
        (0, 1), # south
        (1, 0), # east
    ]      
    
    def __init__(self, input):
        self.anchor_pos = set()
        self.o_pos = set()
                      
        self.maxX = len(input[0]) - 1
        self.maxY = len(input) - 1
        
        for y in range(len(input)):
            for x in range(len(input[y])):
                if input[y][x] == "O":
                    self.o_pos.add((x, y))
                elif input[y][x] == "#":
                    self.anchor_pos.add((x, y))
                    
        # add borders as anchors
        for y in range(self.maxY + 1): self.anchor_pos.add((-1, y))
        for y in range(self.maxY + 1): self.anchor_pos.add((self.maxX + 1, y))
        for x in range(self.maxX + 1): self.anchor_pos.add((x, -1))
        for x in range(self.maxX + 1): self.anchor_pos.add((x, self.maxY + 1))
                
    def load(self):
        return sum(
            (self.maxY + 1) - pos[1]
            for pos in self.o_pos
        )        
    
    def cycle(self, north_only = False):
        # for each anchor point, count the affected `O`s in the direction and
        # clear them. then, add that number of `O`s at the end of the possible
        # range from anchor to the border (or another anchor)
        
        for direction in ([self.cycle_directions[0]] if north_only else self.cycle_directions):
            for anchor in self.anchor_pos:
                pos = anchor
                o_count = 0
                fields = 0
                while True:
                    pos = (pos[0] + direction[0], pos[1] + direction[1])
                    #print(f"at {pos}")
                    
                    if pos in self.anchor_pos: break
                    if pos[0] < 0 or pos[0] > self.maxX: break
                    if pos[1] < 0 or pos[1] > self.maxY: break
                    fields += 1
                    if pos in self.o_pos:
                        o_count += 1
                        self.o_pos.remove(pos)
        
                for i in range(o_count):
                    new_o = (
                        anchor[0] + direction[0] * (fields - i),
                        anchor[1] + direction[1] * (fields - i),
                    )
                    self.o_pos.add(new_o)
            
    def load_after_cycles(self, cycle_count):
        map_configurations = []
        
        cycle = 1
        skipped = False
        while cycle <= cycle_count:
            # run cycle
            self.cycle()
            
            if skipped or self.o_pos not in map_configurations:
                map_configurations += [self.o_pos.copy()]
                cycle += 1
                continue
            
            prev_cycle = map_configurations.index(self.o_pos) + 1
            print(f"repeat from {prev_cycle} to {cycle}")
        
            cycle_len = cycle - prev_cycle
            skip_cycles = (cycle_count - cycle) // cycle_len
            skip_to = cycle + cycle_len * skip_cycles + 1
            print(f"skip from {cycle} to {skip_to}")
            cycle = skip_to
            skipped = True
            
        return self.load()
        
    def print(self):
        grid = Grid(default = ".")
        for o in self.o_pos: grid.set(o, "O")
        for a in self.anchor_pos: grid.set(a, "#")
        grid.print()
    
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
        map = RockMap(self.getInput())
        map.cycle(north_only = True)
        #map.print()
        return map.load()

    def part2(self) -> Any:
        map = RockMap(self.getInput())
        return map.load_after_cycles(1_000_000_000)


if __name__ == '__main__':
    day = Day(2023, 14)
    day.run(verbose=True)
