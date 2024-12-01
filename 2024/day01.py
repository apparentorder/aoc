from tools.aoc import AOCDay
from typing import Any

def parse(input: [str]):
	l0 = sorted(int(line.split()[0]) for line in input)
	l1 = sorted(int(line.split()[1]) for line in input)
	return (l0, l1)

class Day(AOCDay):
	inputs = [
		[
			(11, "input1-test"),
			(2378066, "input1"),
		],
		[
			(31, "input1-test"),
			(18934359, "input1"),
		]
	]

	def part1(self) -> Any:
		(l0, l1) = parse(self.getInput())
		return sum(abs(i0 - l1[i]) for i, i0 in enumerate(l0))

	def part2(self) -> Any:
		(l0, l1) = parse(self.getInput())
		return sum(i0 * l1.count(i0) for i, i0 in enumerate(l0))

if __name__ == '__main__':
	day = Day(2024, 1)
	day.run(verbose=True)
