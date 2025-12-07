from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any

class Day(AOCDay):
	SPLITTER = -1

	def solve(self, is_part2: bool) -> Any:
		manifold = self.parse()

		split_count = 0
		for row in range(len(manifold) - 1):
			for col in range(len(manifold[0])):
				value = manifold[row][col]
				if value == 0 or value == self.SPLITTER:
					continue

				if manifold[row + 1][col] == self.SPLITTER:
					manifold[row + 1][col - 1] += value
					manifold[row + 1][col + 1] += value
					split_count += 1
				else:
					manifold[row + 1][col] += value

		return sum(manifold[-1]) if is_part2 else split_count

	def parse(self):
		input = self.getInput()
		manifold = [[0 for _ in range(len(input[0]))] for _ in range(len(input))]
		for row, line in enumerate(input):
			for col, char in enumerate(line):
				if char == "S": manifold[row][col] = 1
				elif char == "^": manifold[row][col] = self.SPLITTER

		return manifold

	def part1(self) -> Any:
		return self.solve(is_part2 = False)

	def part2(self) -> Any:
		return self.solve(is_part2 = True)

	inputs = [
		[
			(21, "input7-test"),
			(1703, "input7-penny"),
			(1560, "input7"),
		],
		[
			(40, "input7-test"),
			(171692855075500, "input7-penny"),
			(25592971184998, "input7"),
		]
	]

if __name__ == '__main__':
	day = Day(2025, 7)
	day.run(verbose=True)
