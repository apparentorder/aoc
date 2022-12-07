from tools.aoc import AOCDay
from typing import Any

def parse(input):
	dir_size = {}
	cwd = []

	for line in input:
		elem = line.split()

		if elem[0] == "$":
			if elem[1] == "cd":
				if elem[2] == "..":
					cwd.pop()
				elif elem[2] == "/":
					cwd = []
				else:
					cwd += [elem[2]]

		# files always start with the size
		if not elem[0].isnumeric():
			continue

		size = int(elem[0])
		# update/set size for this path and all parent paths
		for i in range(len(cwd) + 1):
			cwd_string = "/" + "/".join(cwd[:i])
			dir_size[cwd_string] = size + dir_size.get(cwd_string, 0)

	return dir_size

class Day(AOCDay):
	inputs = [
		[
			(95_437, '07-test')
			,(1_844_187, '07')
		],
		[
			(24_933_642, '07-test')
			,(4_978_279, '07')
		]
	]

	def part1(self) -> Any:
		ds = parse(self.getInput())
		return sum(size for dir, size in ds.items() if size <= 100_000)

	def part2(self) -> Any:
		ds = parse(self.getInput())

		free = 70_000_000 - ds['/']
		needed = 30_000_000

		return min(size for dir, size in ds.items() if free+size > needed)

