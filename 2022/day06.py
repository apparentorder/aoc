from tools.aoc import AOCDay
from typing import Any

def marker_pos(input, size):
	buffer = list(input[:size])

	for i in range(size, len(input)):
		if len(set(buffer)) == size:
			return i

		buffer.pop(0)
		buffer += [input[i]]

	raise Exception("found nothing")

class Day(AOCDay):
	inputs = [
		[
			(7, '06-test1')
			,(5, '06-test2')
			,(6, '06-test3')
			,(10, '06-test4')
			,(11, '06-test5')
			,(1034, '06')
		],
		[
			(19, '06-test1')
			,(23, '06-test2')
			,(23, '06-test3')
			,(29, '06-test4')
			,(26, '06-test5')
			,(2472, '06')
		]
	]

	def part1(self) -> Any:
		return marker_pos(self.getInput(), 4)

	def part2(self) -> Any:
		return marker_pos(self.getInput(), 14)

