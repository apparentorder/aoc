from tools.aoc import AOCDay
from typing import Any

def parse(input):
	pairs = []

	for line in input:
		pair = []
		for sections in line.split(","):
			low, high = sections.split("-")
			pair += [range(int(low), int(high) + 1)]

		pairs += [pair]

	#print(pairs)
	return pairs

def overlap(pair, fully: bool):
	s1 = set(pair[0])
	s2 = set(pair[1])
	intersection = s1.intersection(s2)

	if fully:
		return intersection == s1 or intersection == s2
	else:
		return len(intersection) > 0

class Day(AOCDay):
	inputs = [
		[
			(2, '04-test')
			,(538, '04')
		],
		[
			(4, '04-test')
			,(792, '04')
		]
	]

	def part1(self) -> Any:
		pairs = parse(self.getInput())
		return sum([1 for pair in pairs if overlap(pair, True)])

	def part2(self) -> Any:
		pairs = parse(self.getInput())
		return sum([1 for pair in pairs if overlap(pair, False)])

