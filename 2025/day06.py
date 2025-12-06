from math import prod
from tools.aoc import AOCDay
from typing import Any, Tuple

class Day(AOCDay):
	def solve(self, right_to_left = False) -> int:
		op_list, value_list = self.parse_input(right_to_left)

		return sum(
			sum(value_list[i]) if op == "+" else prod(value_list[i])
			for i, op in enumerate(op_list)
		)

	def parse_input(self, right_to_left = False) -> Tuple[list[str], list[list[int]]]:
		input = self.getInput()
		op_list = input.pop().split()
		value_list = [[] for _ in range(len(op_list))]

		if not right_to_left: # for part 1
			for line in input:
				for i, value in enumerate(line.split()):
					value_list[i].append(int(value))

			return op_list, value_list

		# for part 2
		input = list(map(list, input))
		value_i = len(value_list) - 1
		while len(input[0]) > 0:
			value_s = "".join(digit for digit in [line.pop() for line in input] if digit != " ")

			if value_s != "":
				value_list[value_i].append(int(value_s))
			else:
				value_i -= 1

		return op_list, value_list

	def part1(self) -> Any:
		return self.solve(right_to_left = False)

	def part2(self) -> Any:
		return self.solve(right_to_left = True)

	inputs = [
		[
			(4277556, "input6-test"),
			# (997, "input6-penny"),
			(5171061464548, "input6"),
		],
		[
			(3263827, "input6-test"),
			# (5978, "input6-penny"),
			(10189959087258, "input6"),
		]
	]

if __name__ == '__main__':
	day = Day(2025, 6)
	day.run(verbose=True)
