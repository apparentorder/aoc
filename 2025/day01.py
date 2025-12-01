from tools.aoc import AOCDay
from typing import Any

class Day(AOCDay):
	def part1(self) -> Any:
		dial = 50
		count0 = 0
		for line in self.getInput():
			clicks = int(line[1:])
			clicks *= -1 if line[0] == "L" else 1

			dial = (dial + clicks) % 100
			if dial == 0:
				count0 += 1

		return count0

	def part2(self) -> Any:
		dial = 50
		count0 = 0
		for line in self.getInput():
			clicks = int(line[1:])

			count0 += clicks // 100
			clicks %= 100
			clicks *= -1 if line[0] == "L" else 1

			if dial != 0 and not 0 < (dial + clicks) < 100:
				count0 += 1

			dial = (dial + clicks) % 100

		return count0

	inputs = [
		[
			(3, "input1-test"),
			(997, "input1-penny"),
			(1123, "input1"),
		],
		[
			(6, "input1-test"),
			(5978, "input1-penny"),
			(6695, "input1"),
		]
	]

if __name__ == '__main__':
	day = Day(2025, 1)
	day.run(verbose=True)
