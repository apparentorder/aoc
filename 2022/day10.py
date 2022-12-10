from tools.aoc import AOCDay
from tools.ocr_ascii import AsciiOcr
from typing import Any

def parse(input):
	cycles = []
	x = 1

	for parts in [line.split() for line in input]:
		cycles += [x]

		if parts[0] == "addx":
			cycles += [x] # again
			x += int(parts[1])

	return cycles

def screen(cycles):
	s = ""

	for cycle_number, x in enumerate(cycles):
		if cycle_number > 0 and cycle_number % 40 == 0:
			s += "\n"

		is_lit = x in range((cycle_number%40)-1, (cycle_number%40)+2)
		s += "#" if is_lit else "."

	return s

test_screen = (
	"##..##..##..##..##..##..##..##..##..##..\n"
	"###...###...###...###...###...###...###.\n"
	"####....####....####....####....####....\n"
	"#####.....#####.....#####.....#####.....\n"
	"######......######......######......####\n"
	"#######.......#######.......#######....."
)

class Day(AOCDay):
	inputs = [
		[
			(13140, '10-test')
			,(14620, '10')
		],
		[
			("test_ok", '10-test')
			,("BJFRHRFU", '10')
		]
	]

	def part1(self) -> Any:
		cycles = parse(self.getInput())
		x20 = [x * (i+1) for i, x in enumerate(cycles) if (i+21) % 40 == 0]
		return sum(x20)

	def part2(self) -> Any:
		cycles = parse(self.getInput())
		s = screen(cycles)
		if s == test_screen:
			return "test_ok"
		else:
			grid = [list(line) for line in s.split("\n")]
			return(str(AsciiOcr(grid, 4, 1)))

