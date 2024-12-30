from tools.aoc import AOCDay
from collections import deque
from typing import Any

class Day(AOCDay):
	def parse(self):
		patterns, designs = self.getMultiLineInputAsArray()
		self.patterns = set(p.strip(",") for p in patterns[0].split())
		self.designs = designs
		self.cache = {}

	def count_ways(self, design: str) -> int:
		if design == "":
			return 1

		if (c := self.cache.get(design)) is not None:
			return c

		count = 0
		for p in self.patterns:
			if design.startswith(p):
				count += self.count_ways(design[len(p):])

		self.cache[design] = count
		return count

	def part1(self) -> Any:
		self.parse()
		return sum(int(bool(self.count_ways(design))) for design in self.designs)

	def part2(self):
		self.parse()
		return sum(self.count_ways(design) for design in self.designs)

	inputs = [
		[
			(6, "input19-test"),
			(296, "input19-penny"),
			(206, "input19"),
		],
		[
			(16, "input19-test"),
			(619970556776002, "input19-penny"),
			(622121814629343, "input19"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 19)
	day.run(verbose=True)
