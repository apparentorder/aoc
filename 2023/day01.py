from tools.aoc import AOCDay
from typing import Any
import re

def extract_numbers(input):
    for line in input:
        s = re.sub(r'[^0-9]', '', line)
        yield int(f"{s[0]}{s[-1]}")
        
def extract_numbers_with_words(input):
    lookup = {
        1: ["one", "1"],
        2: ["two", "2"],
        3: ["three", "3"],
        4: ["four", "4"],
        5: ["five", "5"],
        6: ["six", "6"],
        7: ["seven", "7"],
        8: ["eight", "8"],
        9: ["nine", "9"],
    }
    
    for line in input:
        first_digit_index = 2**31
        first_digit_value = 0
        last_digit_index = -1
        last_digit_value = 0
        
        for digit, words in lookup.items():
            for word in words:
                first_match_index = line.find(word)
                last_match_index = line.rfind(word)
                
                if first_match_index == -1:
                    continue
                
                if first_match_index < first_digit_index:
                    first_digit_index = first_match_index
                    first_digit_value = digit
                
                if last_match_index > last_digit_index:
                    last_digit_index = last_match_index
                    last_digit_value = digit            
                    
        yield first_digit_value * 10 + last_digit_value
        
class Day(AOCDay):
    inputs = [
        [
            (142, "input1-test"),
            (55017, "input1"),
        ],
        [
            (281, "input1-testp2"),
            (53539, "input1"),
        ]
    ]

    def part1(self) -> Any:
        return sum(extract_numbers(self.input))

    def part2(self) -> Any:
        return sum(extract_numbers_with_words(self.input))


if __name__ == '__main__':
    day = Day(2023, 1)
    day.run(verbose=True)
