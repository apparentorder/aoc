from tools.aoc import AOCDay
from typing import Any

class Day(AOCDay):
	def parse(self):
		input_plans = self.getMultiLineInputAsArray()
		self.lock_height = len(input_plans[0]) - 1

		self.locks = [
			[sum(1 for row in plan if row[column] == "#") - 1 for column in range(len(plan[0]))]
			for plan in input_plans if "." in plan[0]
		]

		self.keys = [
			[sum(1 for row in plan if row[column] == "#") - 1 for column in range(len(plan[0]))]
			for plan in input_plans if "." not in plan[0]
		]

	def part1(self) -> Any:
		self.parse()

		return sum(
			int(all(
				key[column] + lock[column] < self.lock_height
				for column in range(len(key))
			))
			for key in self.keys
			for lock in self.locks
		)

	def part2(self):
		return 0

	inputs = [
		[
			(3, "input25-test"),
			(3301, "input25"),
		],
		[
			(0, "input25"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 25)
	day.run(verbose=True)
