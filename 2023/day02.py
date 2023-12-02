from tools.aoc import AOCDay
from typing import Any
import re

class Game:
    def is_possible(self, possible_if):
        max_counts = self.max_counts()
        
        for check_color, check_count in possible_if.items():
            if max_counts[check_color] > check_count:
                return False
                
        return True
        
    def minimum_cubes_power(self):
        p = 1
        for c in self.max_counts().values():
            p *= c
            
        return p
        
    def max_counts(self):
        r = {}
        
        for turn in self.turns:
            for color, count in turn.items():
                r[color] = max(r.get(color, 0), count)        
                
        return r

    def __init__(self, line):
        parts_game = line.split(':')
        turns_input = parts_game[1].split(';')
        
        self.id = int(parts_game[0].split()[1])
        self.turns = []
        
        for s in turns_input:
            cubes_input = s.split(',')
            
            turn = {}
            for c in cubes_input:
                parts = c.split()
                turn[parts[1]] = int(parts[0])
                
            self.turns += [turn]
            
class Day(AOCDay):
    inputs = [
        [
            (8, "input2-test"),
            (1734, "input2"),
        ],
        [
            (2286, "input2-test"),
            (70387, "input2"),
        ]
    ]

    def part1(self) -> Any:
        games = map(lambda line: Game(line), self.getInput())
        
        possible_if = {
            "red": 12,
            "green": 13,
            "blue": 14,
        }
        
        return sum([game.id for game in games if game.is_possible(possible_if)])

    def part2(self) -> Any:
        games = map(lambda line: Game(line), self.getInput())
        return sum([game.minimum_cubes_power() for game in games])

if __name__ == '__main__':
    day = Day(2023, 2)
    day.run(verbose=True)
