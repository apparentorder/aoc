from tools.aoc import AOCDay
from typing import Any
import re

class Day(AOCDay):
	def parse_mul(self, input: str, parse_do_dont: bool):
		p = 0
		mul_enabled = True

		for re_match in re.findall(r'(do\(\)|don\'t\(\)|mul\((\d+),(\d+)\))', input):
			if mul_enabled and re_match[1]:
				p += int(re_match[1]) * int(re_match[2])
			elif parse_do_dont and re_match[0] == "don't()":
				mul_enabled = False
			elif parse_do_dont and re_match[0] == "do()":
				mul_enabled = True

		return p

	inputs = [
		[
			(161, "input3-test"),
			(174561379, "input3"),
		],
		[
			(48, "input3-testp2"),
			(106921067, "input3"),
		]
	]

	def part1(self) -> Any:
		return self.parse_mul("".join(self.getInput()), False)

	def part2(self) -> Any:
		return self.parse_mul("".join(self.getInput()), True)

if __name__ == '__main__':
	day = Day(2024, 3)
	day.run(verbose=True)
