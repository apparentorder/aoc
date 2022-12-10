from tools.aoc import AOCDay
from typing import Any

def parse(input):
	cycles = []
	reg = { "x": 1 }

	for line in input:
		e = line.split()

		match e[0]:
			case "noop":
				cycles += [dict(reg)]
			case "addx":
				cycles += [dict(reg)]
				cycles += [dict(reg)]
				reg["x"] += int(e[1])
			case _:
				raise Exception("bad input: %s" % (line))

	return cycles

def printscreen(cycles):
	s = ""

	for cycle, register in enumerate(cycles):
		if cycle % 40 == 0:
			s += "\n"

		if register["x"] in range((cycle%40)-1, (cycle%40)+2):
			s += "#"
		else:
			s += "."

	print(s)

class Day(AOCDay):
	inputs = [
		[
			(13140, '10-test')
			,(14620, '10')
		],
		[
			(None, '10')
		]
	]

	def part1(self) -> Any:
		cycles = parse(self.getInput())
		x20 = [e["x"] * (i+1) for i, e in enumerate(cycles) if (i+21) % 40 == 0]
		return sum(x20)

	def part2(self) -> Any:
		cycles = parse(self.getInput())
		printscreen(cycles)
		return "BJFRHRFU"

