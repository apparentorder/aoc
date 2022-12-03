from tools.aoc import AOCDay
from typing import Any

def rucksacks(input):
	sum = 0

	for line in input:
		split = int(len(line)/2)
		comp1 = set([c for c in line[:split]])
		comp2 = set([c for c in line[split:]])

		intersect = comp1 & comp2
		intersect_char = intersect.pop()

		prio = ord(intersect_char) - (96 if intersect_char.islower() else 38)
		#print("is %s@%d" % (intersect_char, prio))
		sum += prio

	return sum

def rucksacks2(input):
	sum = 0
	groups = []

	for i in range(int(len(input)/3)):
		r1 = set([c for c in input[i*3]])
		r2 = set([c for c in input[i*3+1]])
		r3 = set([c for c in input[i*3+2]])

		intersect = r1 & r2 & r3
		intersect_char = intersect.pop()

		prio = ord(intersect_char) - (96 if intersect_char.islower() else 38)
		print("is %s@%d" % (intersect_char, prio))
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
			,(None, '03')
		]
	]

	def part1(self) -> Any:
		return rucksacks(self.getInput())

	def part2(self) -> Any:
		return rucksacks2(self.getInput())

