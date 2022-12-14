from tools.aoc import AOCDay
from typing import Any

def parse(input):
	points = {}

	for line in input:
		coords = []
		for coord in line.split(" -> "):
			x,y = list(map(int, coord.split(",")))
			coords += [(x,y)]

		pos = coords[0]
		for cx, cy in coords:
			sorted_x = sorted([cx, pos[0]])
			sorted_x[1] += 1
			for line_x in range(sorted_x[0], sorted_x[1]):
				points[(line_x, pos[1])] = "#"

			sorted_y = sorted([cy, pos[1]])
			sorted_y[1] += 1
			for line_y in range(sorted_y[0], sorted_y[1]):
				points[(pos[0], line_y)] = "#"

			pos = (cx, cy)

	return points

def fill_sand(points_in):
	points = dict(points_in)

	max_y = max([p[1] for p in points])
	print(f"maxy {max_y}")

	while True:
		sx, sy = (500, 0)

		while True:
			try_pos = [(sx, sy+1), (sx-1, sy+1), (sx+1, sy+1)]
			for p in try_pos:
				print(f"try sand at {p}")
				if not p in points:
					sx, sy = p
					break

			if (sx, sy) not in try_pos:
				# sand could not move and now rests
				if (sx, sy) in points:
					# this already had resting sand!
					return points

				points[(sx, sy)] = "o"
				break

			if sy > max_y:
				return points

class Day(AOCDay):
	inputs = [
		[
			(24, '14-test')
			,(994, '14')
		],
		[
			(93, '14-test')
			,(None, '14')
		]
	]

	def part1(self) -> Any:
		points = parse(self.getInput())
		points = fill_sand(points)
		#print(points)
		return sum([1 for p in points if points[p] == "o"])

	def part2(self) -> Any:
		points = parse(self.getInput())
		print("parsed:\n" + str(points))

		max_y = max([p[1] for p in points]) + 2

		for x in range(-max_y, max_y+1):
			points[(500+x, max_y)] = "#"

		print("added:\n" + str(points))

		points = fill_sand(points)
		print(points)
		return sum([1 for p in points if points[p] == "o"])
