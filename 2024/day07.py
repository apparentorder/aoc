from tools.aoc import AOCDay
from tools.coordinate import Coordinate, DistanceAlgorithm
from tools.grid import Grid
from typing import Any, Dict

class Day(AOCDay):
	def solve_line(self, input: str):
		nums = list(map(int, input.replace(":", "").split()))
		test_value = nums[0]
		return test_value if self.possibly_true(test_value, nums[1], nums[2:]) else 0

	def possibly_true(self, test_value: int, value_so_far: int, remaining_operands: [int]) -> bool:
		if value_so_far > test_value:
			return False

		if not remaining_operands:
			return test_value == value_so_far

		result = self.possibly_true(test_value, value_so_far + remaining_operands[0], remaining_operands[1:])
		result = result or self.possibly_true(test_value, value_so_far * remaining_operands[0], remaining_operands[1:])

		if self.allow_concat:
			concat = int(f"{value_so_far}{remaining_operands[0]}")
			result = result or self.possibly_true(test_value, concat, remaining_operands[1:])

		return result

	def part1(self) -> Any:
		self.allow_concat = False
		return sum(self.solve_line(line) for line in self.getInput())

	def part2(self) -> Any:
		self.allow_concat = True
		return sum(self.solve_line(line) for line in self.getInput())

	inputs = [
		[
			(3749, "input7-test"),
			(1298103531759, "input7"),
		],
		[
			(11387, "input7-test"),
			(140575048428831, "input7"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 7)
	day.run(verbose=True)
