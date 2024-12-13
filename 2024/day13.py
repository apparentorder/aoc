from tools.aoc import AOCDay
from tools.coordinate import Coordinate
from typing import Any
import re

class Machine:
	def __init__(self, input_lines):
		for line in input_lines:
			re_match = re.match(r'([^:]+): X=?([0-9+]+), Y=?([0-9+]+)', line)

			if re_match.group(1) == "Button A":
				self.button_a = Coordinate(int(re_match.group(2)), int(re_match.group(3)))
			elif re_match.group(1) == "Button B":
				self.button_b = Coordinate(int(re_match.group(2)), int(re_match.group(3)))
			elif re_match.group(1) == "Prize":
				self.prize = Coordinate(int(re_match.group(2)), int(re_match.group(3)))

	def min_tokens(self, button_limit: int) -> int | None:
		r = None

		for press_count_a in range(button_limit):
			a = self.button_a * press_count_a

			remaining = self.prize - a
			if remaining.x % self.button_b.x == 0 and remaining.y % self.button_b.y == 0:
				press_b_x = remaining.x // self.button_b.x
				press_b_y = remaining.y // self.button_b.y

				if press_b_x == press_b_y and press_b_x <= button_limit:
					tokens = press_count_a * 3 + press_b_x
					r = tokens if r is None else min(tokens, r)

		return r

class Day(AOCDay):
	def parse(self):
		self.machines: list[Machine] = []

		for machine_spec in self.getMultiLineInputAsArray():
			self.machines += [Machine(machine_spec)]

	def part1(self) -> Any:
		self.parse()
		return sum(m.min_tokens(button_limit = 100) or 0 for m in self.machines)

	def part2(self) -> Any:
		self.parse()
		for m in self.machines:
			m.prize += Coordinate(10000000000000, 10000000000000)

		return 0

	inputs = [
		[
			(480, "input13-test"),
			(29438, "input13"),
		],
		[
			(None, "input13"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 13)
	day.run(verbose=True)
