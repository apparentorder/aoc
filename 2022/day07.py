from tools.aoc import AOCDay
from typing import Any

def parse(input):
	dir_size = {}
	cwd = []

	for line in input:
		elem = line.split()

		#print("cwd %s\nline %s\n" % (cwd, line))
		if elem[0] == "$":
			if elem[1] == "cd":
				if elem[2] == "..":
					cwd.pop()
				elif elem[2] == "/":
					cwd = []
				else:
					cwd += [elem[2]]

		elif elem[0].isnumeric():
			# file
			size = int(elem[0])

			for i in range(len(cwd) + 1):
				cwd_string = "/".join(cwd[:i])
				s = dir_size.get(cwd_string, 0)
				dir_size[cwd_string] = size + s

	return dir_size

class Day(AOCDay):
	inputs = [
		[
			(95437, '07-test')
			,(1844187, '07')
		],
		[
			(24933642, '07-test')
			,(4978279, '07')
		]
	]

	def part1(self) -> Any:
		ds = parse(self.getInput())
		return sum(s for (dir, s) in ds.items() if s <= 100000)

	def part2(self) -> Any:
		ds = parse(self.getInput())

		total_size = 70000000
		free = 70000000 - ds['']
		needed = 30000000

		candidates = []
		for dir, s in ds.items():
			if free + s > needed:
				candidates += [s]

		return min(candidates)

