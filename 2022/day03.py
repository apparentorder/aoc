from tools.aoc import AOCDay
from typing import Any

def rucksacks(groups):
	sum = 0

	for group in groups:
		sets = [set(member) for member in group]
		intersect = sets[0].intersection(*sets[1:])
		intersect_char = intersect.pop()

		prio = ord(intersect_char) - (96 if intersect_char.islower() else 38)
		#print("is %s@%d" % (intersect_char, prio))
		sum += prio

	return sum

class Day(AOCDay):
	inputs = [
		[
			(157, '03-test')
			,(7742, '03')
		],
		[
			(70, '03-test')
			,(2276, '03')
		]
	]

	def part1(self) -> Any:
		groups = []
		for line in self.getInput():
			split = len(line)//2
			groups += [[line[:split], line[split:]]]

		return rucksacks(groups)

	def part2(self) -> Any:
		groups = []
		input = self.getInput()
		for i in range(len(input)//3):
			groups += [[input[i*3], input[i*3+1], input[i*3+2]]]

		return rucksacks(groups)

