from tools.aoc import AOCDay
from typing import Any
import re

def steps_from(path, node_map, start, is_part2):
    is_end_node = lambda node: node == "ZZZ" or (node.endswith("Z") and is_part2)
    
    steps = 0
    pos = start
    while not is_end_node(pos):
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
    path = []
    node_map = {}
    
    path = list(input[0])
    
    for line in input[2:]:
        m = re.match(r'(\S+) = \((\S+), (\S+)\)', line)
        node_map[m.group(1)] = (m.group(2), m.group(3))
        
    return path, node_map
    
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
        return steps_from(path, node_map, 'AAA', is_part2 = False)

    def part2(self) -> Any:
        path, node_map = parse(self.getInput())
        
        start_nodes = filter(lambda node: node.endswith('A'), node_map)
        steps = map(lambda node: steps_from(path, node_map, node, is_part2 = True), start_nodes)
        return lcm(steps)

if __name__ == '__main__':
    day = Day(2023, 8)
    day.run(verbose=True)
