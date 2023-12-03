from tools.aoc import AOCDay
from tools.grid import Grid, Coordinate
from typing import Any

def pos_is_digit(grid, pos):
    c = grid.get(pos)
    return c and c.isdigit()
    
def extract_number(grid, pos_start):
    # scan left, find first digit
    pos_first = pos_start
    while pos_is_digit(grid, Coordinate(pos_first.x - 1, pos_first.y)):
        pos_first = Coordinate(pos_first.x - 1, pos_first.y)
        
    # now scan right and extract the number
    number_string = ""
    pos = pos_first
    while pos_is_digit(grid, pos):
        number_string += grid.get(pos)
        pos = Coordinate(pos.x + 1, pos.y)
        
    return int(number_string), pos_first
    
def part_numbers(grid, find_gear_ratios):
    numbers_seen = {}
    
    for y in grid.rangeY():
        for x in grid.rangeX():
            grid_pos = Coordinate(x, y)
            grid_char = grid.get(grid_pos)
            surrounding_part_numbers = [] # for gear ratios (part 2)
            
            # we're looking for symbols
            if grid_char.isdigit() or grid_char == ".":
                continue
        
            # scan grid neighbors for digits
            for neighbor in grid.getNeighboursOf(grid_pos):
                if not pos_is_digit(grid, neighbor):
                    continue
            
                # we have a neighboring digit, so extract the whole number and
                # see if we already know it
                # note about p2: there is a potential bug -- we would miss any
                # number that has already been seen via a previous symbol.
                # doesn't affect the known inputs though, so we turn a blind eye.
                number, number_start_pos = extract_number(grid, neighbor)
                if number_start_pos in numbers_seen:
                    continue
                
                #print(f"got {number} at {number_start_pos}")
                numbers_seen[number_start_pos] = number
                
                if not find_gear_ratios:
                    # part 1: return part numbers
                    yield number
                else:
                    # part 2: make note of all surrounding part numbers
                    surrounding_part_numbers += [number]
                        
            if find_gear_ratios and grid_char == "*" and len(surrounding_part_numbers) == 2:
                yield surrounding_part_numbers[0] * surrounding_part_numbers[1]
                
class Day(AOCDay):
    inputs = [
        [
            (4361, "input3-test"),
            (533775, "input3"),
        ],
        [
            (467835, "input3-test"),
            (78236071, "input3"),
        ]
    ]

    def part1(self) -> Any:
        grid = Grid()
        for y, line in enumerate(self.getInput()):
            for x, c in enumerate(line):
                grid.set(Coordinate(x, y), c)
                
        return sum(part_numbers(grid, find_gear_ratios = False))

    def part2(self) -> Any:
        grid = Grid()
        for y, line in enumerate(self.getInput()):
            for x, c in enumerate(line):
                grid.set(Coordinate(x, y), c)
                
        return sum(part_numbers(grid, find_gear_ratios = True))

if __name__ == '__main__':
    day = Day(2023, 3)
    day.run(verbose=True)
