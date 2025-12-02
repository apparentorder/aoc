from tools.aoc import AOCDay
from typing import Any, Generator
import math

class Day(AOCDay):
	def part1(self) -> Any:
		sum_invalid = 0
		for range in self.parse_input():
			sum_invalid += sum(id for id in range if not self.is_valid_id(id, max_repeat = 2))

		return sum_invalid

	def part2(self) -> Any:
		sum_invalid = 0
		for range in self.parse_input():
			sum_invalid += sum(id for id in range if not self.is_valid_id(id))

		return sum_invalid

	def is_valid_id(self, id: int, max_repeat: int | None = None) -> bool:
		s = str(id)

		min_slen = 1
		if max_repeat:
			min_slen = math.ceil(len(s) / max_repeat)

		for slen in range(min_slen, len(s)//2 + 1):
			sequence = s[:slen]
			need_repeat = len(s) // slen

			if sequence * need_repeat == s:
				return False

		return True

	def parse_input(self) -> Generator[range]:
		for range_s in "".join(self.getInput()).split(","):
			s = str(range_s).split("-")
			yield range(int(s[0]), int(s[1]) + 1)

	inputs = [
		[
			(1227775554, "input2-test"),
			# (997, "input2-penny"),
			(30608905813, "input2"),
		],
		[
			(4174379265, "input2-test"),
			# (5978, "input2-penny"),
			(31898925685, "input2"),
		]
	]

if __name__ == '__main__':
	day = Day(2025, 2)
	day.run(verbose=True)
