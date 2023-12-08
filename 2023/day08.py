from tools.aoc import AOCDay
from typing import Any

def steps_from(path, node_map, start):
    steps = 0
    pos = start
    while not pos[2] == "Z":
        rl = 1 if path[steps % len(path)] == "R" else 0
        steps += 1
        pos = node_map[pos][rl]
            
    return steps
    
def lcm(numbers):
    numbers = sorted(numbers, reverse = True)
    
    t = 0
    while len(numbers) > 1:
        t += 1
        if (numbers[0] * t) % numbers[1] == 0:
            numbers[0] *= t
            numbers.pop(1)
            t = 0
            continue
        
    return numbers[0]
    
def parse(input):
    node_map = {line[0:3]: (line[7:10], line[12:15]) for line in input[2:]}
    return input[0], node_map
    
class Day(AOCDay):
    inputs = [
        [
            (6, "input8-test"),
            (18023, "input8"),
        ],
        [
            (6, "input8-testp2"),
            (14449445933179, "input8"),
        ]
    ]

    def part1(self) -> Any:
        path, node_map = parse(self.getInput())
        return steps_from(path, node_map, 'AAA')

    def part2(self) -> Any:
        path, node_map = parse(self.getInput())
        
        start_nodes = [node for node in node_map if node[2] == "A"]
        steps = [steps_from(path, node_map, node) for node in start_nodes]
        return lcm(steps)

if __name__ == '__main__':
    day = Day(2023, 8)
    day.run(verbose=True)
