from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any

class Brick:
    def __init__(self, id, line):
        self.id = id
        
        start_s, end_s = line.split("~")
        self.start, self.end = [
            Coordinate(int(x),int(y),int(z))
            for x,y,z
            in [start_s.split(","), end_s.split(",")]
        ]
            
        if self.start == self.end:
            # workaround; can be removed after release of
            # https://git.domainforge.de/public/py-tools/commit/fb3bef0153b31af5cb2e15ee9c7536020faec926
            self.cubes = [self.start]
        else:
            self.cubes = self.start.getLineTo(self.end)
            
        self.minZ = min([c.z for c in self.cubes])
        self.maxZ = max([c.z for c in self.cubes])
        
    def __contains__(self, other):
        return other in self.cubes
        
    def footprint(self):
        # x,y coordinates for lowest z
        return [Coordinate(c.x, c.y) for c in self.cubes if c.z == self.minZ]
        
    def move_down(self, count):
        move = Coordinate(0, 0, -count)
        self.start += move
        self.end += move
        self.cubes = [c + move for c in self.cubes]
        
        self.minZ = min([c.z for c in self.cubes])
        self.maxZ = max([c.z for c in self.cubes])
        
    def __repr__(self):
        return f"{self.id}{self.start}~{self.end}"
        
class BrickStack(Grid):
    def __init__(self, input):
        self.bricks = {}
        
        for i, line in enumerate(input):
            brick_id = chr(ord("A") + i) if len(input) < 20 else i
            self.bricks[brick_id] = Brick(brick_id, line)
    
    def bricks_disintegrated_by(self, first_brick):
        disintegrated = set([first_brick])
        
        added = 1
        while added > 0:
            added = 0
            
            remaining = [
                (b,s) for b,s in self.supporters_by_brick.items()
                if b not in disintegrated and b.minZ > 1
            ]
            
            for brick, supporters in remaining:
                if len(set(supporters) - disintegrated) == 0:
                    disintegrated.add(brick)
                    added += 1
                    
        disintegrated.remove(first_brick)
        return disintegrated
        
    def bricks_below_z(self, z, direct):
        return [
            b for b in self.bricks.values()
            if (not direct and b.maxZ < z) or (direct and b.maxZ == z - 1)
        ]        
        
    def supporters_of(self, brick):
        supporters = []
        
        for other_brick in self.bricks_below_z(brick.minZ, direct = True):
            for xy in brick.footprint():
                check_pos = Coordinate(xy.x, xy.y, brick.minZ - 1)
                if check_pos in other_brick:
                    supporters += [other_brick]
                    break
        
        return supporters
        
    def settle(self):
        bricks_by_z = sorted(
            [b for b in self.bricks.values()],
            key = lambda b: b.minZ,
        )
        
        for candidate_brick in bricks_by_z:
            movable_by = self.brick_movable_count(candidate_brick)
                
            if movable_by > 0:
                candidate_brick.move_down(movable_by)
        
        self.supporters_by_brick = {
            brick: self.supporters_of(brick)
            for brick in self.bricks.values()
        }                
        
    def brick_movable_count(self, brick):
        # for each x,y occupied on the current z level, check lower z
        # levels for matches; note the highest occupied z position
        
        max_occupied_z = 0
        
        for other_brick in self.bricks_below_z(brick.minZ, direct = False):
            if other_brick.maxZ < max_occupied_z: continue
            
            for fp in brick.footprint():
                matching_z = [
                    c.z for c in other_brick.cubes
                    if (c.x, c.y) == (fp.x, fp.y)
                ]
                
                if matching_z:
                    max_occupied_z = max(max_occupied_z, *matching_z)
                        
        return brick.minZ - (max_occupied_z + 1)
        
    def print(self):
        grid = Grid(default = ".")
        
        for id, b in self.bricks.items():
            for pos in b.cubes:
                grid.set(pos, id)
                
        for z in reversed(grid.rangeZ()):
            print(f"z = {z}")
            grid.print(z_level = z)
            print()
            
class Day(AOCDay):
    inputs = [
        [
            (5, "input22-test"),
            (490, "input22"),
        ],
        [
            (7, "input22-test"),
            (96356, "input22"),
        ]
    ]

    def part1(self) -> Any:
        bs = BrickStack(self.getInput())
        bs.settle()
        assert all([len(bs.supporters_of(b)) > 0 for b in bs.bricks.values() if b.minZ > 1])
        
        only_supporters = set([
            supporters[0]
            for supporters in bs.supporters_by_brick.values()
            if len(supporters) == 1
        ])
        
        return len(bs.bricks) - len(only_supporters)

    def part2(self) -> Any:
        bs = BrickStack(self.getInput())
        bs.settle()
        
        sum_falling_bricks = sum(
            len(bs.bricks_disintegrated_by(brick))
            for brick in bs.bricks.values()
        )
            
        return sum_falling_bricks


if __name__ == '__main__':
    day = Day(2023, 22)
    day.run(verbose=True)
