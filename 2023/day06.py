from tools.aoc import AOCDay
from typing import Any
import re

def parse(input, is_part2):
    if not is_part2:
        times = list(map(int, input[0].split()[1:]))
        distances = list(map(int, input[1].split()[1:]))
    else:
        times = [int("".join(input[0].split()[1:]))]
        distances = [int("".join(input[1].split()[1:]))]
        
    return times, distances
    
def distances_possible(max_time):
    distances = []
    
    for speed in range(1, max_time):
        distance = (max_time - speed) * speed
        distances += [distance]
        
    return distances
    
class Day(AOCDay):
    inputs = [
        [
            (288, "input6-test"),
            (219849, "input6"),
        ],
        [
            (71503, "input6-test"),
            (29432455, "input6"),
        ]
    ]

    def part1(self) -> Any:
        times, distances = parse(self.getInput(), is_part2 = False)
        
        r = 1
        for i in range(len(distances)):
            dp = distances_possible(times[i])
            winning = [d for d in dp if d > distances[i]]
            r *= len(winning)
            
        return r
        
    def part2(self) -> Any:
        times, distances = parse(self.getInput(), is_part2 = True)
        
        r = 1
        for i in range(len(distances)):
            dp = distances_possible(times[i])
            winning = [d for d in dp if d > distances[i]]
            r *= len(winning)
            
        return r

if __name__ == '__main__':
    day = Day(2023, 6)
    day.run(verbose=True)
