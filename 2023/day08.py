from tools.aoc import AOCDay
from typing import Any
import re

def steps_from_to(path, node_map, start, end):
    steps = 0
    path_len = len(path)
    pos = start
    while pos != end:
        rl = 1 if path[steps % path_len] == "R" else 0
        steps += 1
        #print(f"{pos} -> {node_map[pos][rl]}")
        pos = node_map[pos][rl]
            
    return steps

def steps_z_nodes(path, node_map):
    start_nodes = list(filter(lambda s: s.endswith('A'), node_map))
    pos = {}
    z_nodes = {}
  
    for sn in start_nodes:
        pos[sn] = sn
        
    steps = 0
    path_len = len(path)
    while len(pos) > len(z_nodes):
        rl = 1 if path[steps % path_len] == "R" else 0
        steps += 1
        
        for sn in [sn for sn in pos if sn not in z_nodes]:
            pos[sn] = node_map[pos[sn]][rl]
            if pos[sn].endswith('Z'):
                print(f"{sn} at {pos[sn]} after {steps}")
                z_nodes[sn] = steps
                pos[sn] = None
                
    return lcm(z_nodes.values())
    
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
        return steps_from_to(path, node_map, 'AAA', 'ZZZ')

    def part2(self) -> Any:
        path, node_map = parse(self.getInput())
        return steps_z_nodes(path, node_map)

if __name__ == '__main__':
    day = Day(2023, 8)
    day.run(verbose=True)
