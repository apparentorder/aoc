from tools.aoc import AOCDay
from typing import Any
import re

class Card:
    value_map = {
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }
    def __init__(self, input, is_part2):
        self.label = input
        if is_part2: self.value_map["J"] = 1
        self.value = self.value_map.get(input) or int(input)
        
    def __repr__(self):
        return self.label
        
    def __str__(self):
        return self.label        
        
class Hand:
    def __init__(self, input, is_part2):
        self.cards = list(map(lambda cs: Card(cs, is_part2), input))
        self.joker = is_part2
        self.value  = 1_000_000_000_000 * self.find_primary_value()
        self.value += self.find_secondary_value()
        
    def find_secondary_value(self):
        v = 0
        
        for i, card in enumerate(self.cards):
            pos = len(self.cards) - i
            v += card.value * 100**pos
            
        return v
        
    def find_primary_value(self):
        counts = {}
        for c in self.cards:
            counts[c.label] = counts.get(c.label, 0) + 1
            
        count_j = counts.get('J', 0)
        count_max_other = max([0] + [value for label, value in counts.items() if label != 'J'])
        
        # ----------------------------------------------------------------------
        # five of a kind?
        
        if self.joker and count_j + count_max_other == 5:
            # always five of a kind
            return 7
            
        if 5 in counts.values():
            return 7
            
        # ----------------------------------------------------------------------
        # four of a kind?
        
        if self.joker and count_j + count_max_other == 4:
            return 6
            
        if 4 in counts.values():
            return 6

        # ----------------------------------------------------------------------
        # full house?
        
        if self.joker and count_j == 1 and len(list(filter(lambda cv: cv == 2, counts.values()))) == 2:
            return 5
            
        if 3 in counts.values() and 2 in counts.values():
            return 5
            
        # ----------------------------------------------------------------------
        # three of a kind
         
        if self.joker and count_j + count_max_other == 3:
            return 4
            
        if 3 in counts.values():
            return 4
            
        # ----------------------------------------------------------------------
        # two pair
        
        if self.joker and count_j == 1 and count_max_other == 2:
            return 3
            
        if len(list(filter(lambda cv: cv == 2, counts.values()))) == 2:
            return 3
            
        # ----------------------------------------------------------------------
        # one pair
        
        if self.joker and count_j == 1:
            return 2
            
        if 2 in counts.values():
            return 2
            
        # all high-card hands have the same primary value, regardless
        # of the highest card's value
        return 1
        
    def __repr__(self):
        return "".join(str(self.cards))
        
def parse(input, is_part2):
    for line in input:
        parts = line.split()
        yield Hand(parts[0], is_part2), int(parts[1])
        
class Day(AOCDay):
    inputs = [
        [
            (6440, "input7-test"),
            (249483956, "input7"),
        ],
        [
            (5905, "input7-test"),
            (252137472, "input7"),
        ]
    ]

    def part1(self) -> Any:
        hands_and_bids = list(parse(self.getInput(), is_part2 = False))
        hands_and_bids.sort(key = lambda hb: hb[0].value)
        
        total_winnings = 0
        for i, (_, bid) in enumerate(hands_and_bids):
            #print(f"rank {i + 1} hand {hand} value {hand.value} bid {bid}")
            total_winnings += bid * (i + 1)
        
        return total_winnings
        
    def part2(self) -> Any:
        hands_and_bids = list(parse(self.getInput(), is_part2 = True))
        hands_and_bids.sort(key = lambda hb: hb[0].value)
        
        total_winnings = 0
        for i, (hand, bid) in enumerate(hands_and_bids):
            #if "J" in str(hand): print(f"rank {i + 1} hand {hand} value {hand.value} bid {bid}")
            total_winnings += bid * (i + 1)
        
        return total_winnings
        
if __name__ == '__main__':
    day = Day(2023, 7)
    day.run(verbose=True)
