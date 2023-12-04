from tools.aoc import AOCDay
from typing import Any
import re

def match_count(line):
    # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    m = re.match(r'^Card +(\d+):(( +\d+)+) *\|(( +\d+)+)', line)
    card_id = int(m.group(1))
    winning_numbers = set([int(s.strip()) for s in m.group(2).split(' ') if s != ""])
    numbers = set([int(s.strip()) for s in m.group(4).split(' ') if s != ""])
    
    return len(winning_numbers.intersection(numbers)), card_id
    
class Day(AOCDay):
    inputs = [
        [
            (13, "input4-test"),
            (24706, "input4"),
        ],
        [
            (30, "input4-test"),
            (13114317, "input4"),
        ]
    ]

    def part1(self) -> Any:
        def score(line):
            c, _ = match_count(line)
            return 2**(c - 1) if c > 0 else 0
            
        return sum(map(score, self.getInput()))

    def part2(self) -> Any:
        card_count = 0
        extra_cards = {}
        for card_line in self.getInput():
            matches, this_card_id = match_count(card_line)
            this_card_count = extra_cards.get(this_card_id, 0) + 1
            
            for extra_card_id in range(this_card_id + 1, this_card_id + matches + 1):
                extra_cards[extra_card_id] = extra_cards.get(extra_card_id, 0) + this_card_count
                
            card_count += this_card_count
            
        return card_count


if __name__ == '__main__':
    day = Day(2023, 4)
    day.run(verbose=True)
