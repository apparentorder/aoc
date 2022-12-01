from tools.aoc import AOCDay
from typing import Any

class Day(AOCDay):
	inputs = [
		[
			(24_000, '01-test'),
			(72_070, '01')
		],
		[
			(45_000, '01-test'),
			(211_805, '01')
		]
	]

	def part1(self) -> Any:
		return max(elfcal(self.input))

	def part2(self) -> Any:
		e = elfcal(self.input)
		e.sort(reverse = True)
		return sum(e[0:3])

def elfcal(input):
	elfcal = [0]

	for line in input:
		try:
			v = int(line)
			elfcal[-1] += v
		except:
			elfcal.append(0)

	return elfcal

