from tools.aoc import AOCDay
from typing import Any

def foo():
    return 23

class Day(AOCDay):
    inputs = [
        [
            (142, "input1-test"),
            (None, "input1"),
        ],
        [
            (281, "input1-testp2"),
            (None, "input1"),
        ]
    ]

    def part1(self) -> Any:
        return foo()

    def part2(self) -> Any:
        return foo()

if __name__ == '__main__':
    day = Day(2024, 1)
    day.run(verbose=True)
