from tools.aoc import AOCDay
from typing import Any

def find_next(line, is_part2):
    value_lists = []
    value_lists += [list(map(int, line.split()))]

    while any(v != 0 for v in value_lists[-1]):
        new_list = []
        for i in range(1, len(value_lists[-1])):
            diff = value_lists[-1][i] - value_lists[-1][i-1]
            new_list += [diff]
            
        value_lists += [new_list]
    
    for vi in reversed(range(0, len(value_lists) - 1)):
        if is_part2:
            new_value = value_lists[vi][0] - value_lists[vi + 1][0]
            value_lists[vi].insert(0, new_value)
        else:
            new_value = value_lists[vi + 1][-1] + value_lists[vi][-1]
            value_lists[vi] += [new_value]
        
    return value_lists[0][0] if is_part2 else value_lists[0][-1]
    
class Day(AOCDay):
    inputs = [
        [
            (114, "input9-test"),
            (1684566095, "input9"),
        ],
        [
            (2, "input9-test"),
            (1136, "input9"),
        ]
    ]

    def part1(self) -> Any:
        return sum(find_next(line, is_part2 = False) for line in self.getInput())

    def part2(self) -> Any:
        return sum(find_next(line, is_part2 = True) for line in self.getInput())


if __name__ == '__main__':
    day = Day(2023, 9)
    day.run(verbose=True)
