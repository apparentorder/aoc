from tools.aoc import AOCDay
from typing import Any

def parse(input):
	grid = {}

	for line in input:
		coords_str = line.split(" -> ")
		coords_int = [list(map(int, c.split(","))) for c in coords_str]
		coords = [(c[0], c[1]) for c in coords_int]

		for i in range(1, len(coords)):
			fromx, fromy = coords[i - 1]
			tox, toy = coords[i]

			sorted_x = sorted([fromx, tox])
			sorted_y = sorted([fromy, toy])

			for x in range(sorted_x[0], sorted_x[1] + 1):
				for y in range(sorted_y[0], sorted_y[1] + 1):
					grid[(x,y)] = "#"

	return grid

def fill_sand(grid, virtual_floor):
	max_y = max([p[1] for p in grid])

	if virtual_floor:
		max_y += 2
		for x in range(-max_y, max_y+1):
			grid[(500+x, max_y)] = "#"

	sand_path = [(500, 0)]
	while len(sand_path) > 0:
		sx, sy = sand_path.pop()

		while True:
			try_pos = [
				(sx,   sy+1), # down
				(sx-1, sy+1), # down/left
				(sx+1, sy+1), # down/right
			]

			for p in try_pos:
				#print(f"try sand at {p} path {sand_path}")
				if not p in grid:
					# position is not blocked, so sand keeps falling
					sand_path += [(sx, sy)]
					sx, sy = p
					break
			else:
				# didn't find a valid next position, so sand will rest here.
				grid[(sx, sy)] = "o"

				if (sx, sy) == (500, 0):
					# start position is now sand, we're done.
					return

				break

			if sy > max_y:
				# sand flows into the endless void
				return

class Day(AOCDay):
	inputs = [
		[
			(24, '14-test')
			,(994, '14')
		],
		[
			(93, '14-test')
			,(26283, '14')
		]
	]

	def part1(self) -> Any:
		grid = parse(self.getInput())
		fill_sand(grid, False)
		return list(grid.values()).count("o")

	def part2(self) -> Any:
		grid = parse(self.getInput())
		fill_sand(grid, True)
		return list(grid.values()).count("o")

