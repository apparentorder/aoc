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
    
def winning_distances(max_time, min_distance):
    # distance = (max_time - speed) * speed
    # distance/speed = max_time - speed
    # distance/speed + speed = max_time
    # best at max_time/2

    count = 0
    for speed in range(max_time//2, 0, -1):
        distance = (max_time - speed) * speed
        
        if distance <= min_distance:
            break
        
        count += 1
        
    count *= 2
    if max_time % 2 == 0: count -= 1
    return count

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
            r *= winning_distances(times[i], distances[i])
            
        return r
        
    def part2(self) -> Any:
        times, distances = parse(self.getInput(), is_part2 = True)
        
        r = 1
        for i in range(len(distances)):
            r *= winning_distances(times[i], distances[i])
            
        return r

if __name__ == '__main__':
    day = Day(2023, 6)
    day.run(verbose=True)
