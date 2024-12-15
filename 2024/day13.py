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

	def min_tokens(self, is_part2: bool) -> int | None:
		a_press = 0
		b_press = 0

		if is_part2:
			if button_presses := self.relocate_prize():
				(a_press, b_press) = button_presses
			else:
				return None

		# TODO: set limits dynamically instead of hard-coding random values; same in relocate_prize()
		for try_a_press in range(3_000 if is_part2 else 100):
			remaining_x = self.prize.x - (try_a_press * self.button_a.x)

			if remaining_x % self.button_b.x != 0:
				continue

			try_b_press = remaining_x//self.button_b.x

			pos_x = try_a_press*self.button_a.x + try_b_press*self.button_b.x
			pos_y = try_a_press*self.button_a.y + try_b_press*self.button_b.y

			# n.b.: avoid Coordinate in heavy-duty loop
			if pos_x == self.prize.x and pos_y == self.prize.y:
				a_press += try_a_press
				b_press += try_b_press
				return a_press * 3 + b_press

		return None

	def relocate_prize(self) -> tuple[int, int] | None:
		self.prize += Coordinate(10000000000000, 10000000000000)

		# find a combination of button presses that will advance x,y at the same rate.
		for try_a_press in range(max(self.button_b.x, self.button_b.y)):
			for try_b_press in range(max(self.button_a.x, self.button_a.y)):
				pos_x = try_a_press*self.button_a.x + try_b_press*self.button_b.x
				pos_y = try_a_press*self.button_a.y + try_b_press*self.button_b.y

				if pos_x == pos_y and pos_x > 0:
					max_offset_xy = 10000000000000 - 30_000
					single_offset_xy = try_a_press*self.button_a.x + try_b_press*self.button_b.x
					offset_count = max_offset_xy // single_offset_xy
					self.prize -= Coordinate(single_offset_xy * offset_count, single_offset_xy * offset_count)
					a_press = try_a_press * offset_count
					b_press = try_b_press * offset_count
					# print(f"balanced presses at ap {try_a_press} bp {try_b_press} (correct by {single_offset_xy * offset_count})")
					return a_press, b_press

		return None

class Day(AOCDay):
	def part1(self) -> Any:
		self.machines = list(map(Machine, self.getMultiLineInputAsArray()))
		return sum(m.min_tokens(is_part2 = False) or 0 for m in self.machines)

	def part2(self) -> Any:
		self.machines = list(map(Machine, self.getMultiLineInputAsArray()))
		return sum(m.min_tokens(is_part2 = True) or 0 for m in self.machines)

	inputs = [
		[
			(480, "input13-test"),
			(29438, "input13"),
		],
		[
			(875318608908, "input13-test"),
			(104958599303720, "input13"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 13)
	day.run(verbose=True)
