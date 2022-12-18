from tools.coordinate import Coordinate
from tools.grid import Grid
from tools.aoc import AOCDay
from typing import Any
import re

def parse(input):
	grid = Grid()

	for line in input:
		x, y, z = line.split(",")
		grid.set(Coordinate(int(x), int(y), int(z)))

	return grid

def count_sides(grid):
	sum = 0

	for c in grid.getActiveCells():
		sum += 6 - len(grid.getNeighboursOf(c, False, False))

	return sum

def mark_enclosed(grid):
	cubes_checked = set()

	for c in grid.getActiveCells():
		# for each cube's empty neighbors, try to expand as much as possible. if the resulting
		# area touches any edge, it's not enclosed.

		for neigh in set(grid.getNeighboursOf(c, True, False)) - cubes_checked:
			area, touches_edge = get_area(grid, neigh)
			cubes_checked |= area

			if not touches_edge:
				for enclosed_cube in area:
					grid.set(enclosed_cube, "known_enclosed")

def get_area(grid, startpos):
	if grid.isSet(startpos):
		return set(), False

	area = set()
	touches_edge = False
	minX, minY, maxX, maxY, minZ, maxZ = grid.getBoundaries()

	cubes_to_add = set([startpos])
	while len(cubes_to_add) > 0:
		area |= cubes_to_add
		cubes_to_add.clear()

		for c in area:
			for neigh in grid.getNeighboursOf(c, True, False):
				if not neigh in area and not grid.isSet(neigh):
					cubes_to_add.add(neigh)

	for c in area:
		if (c.x in [minX, maxX] or c.y in [minY, maxY] or c.z in [minZ, maxZ]):
			# this is a cube on the outer edge, so this area cannot be enclosed
			touches_edge = True

	#print(f"area from start {startpos} of {len(area)} touches_edge {touches_edge}")
	return area, touches_edge

class Day(AOCDay):
	inputs = [
		[
			(10, '18-test-small')
			,(64, '18-test')
			,(3526, '18')
		],
		[
			(58, '18-test')
			,(2090, '18')
		]
	]

	def part1(self) -> Any:
		grid = parse(self.getInput())
		return count_sides(grid)

	def part2(self) -> Any:
		grid = parse(self.getInput())
		mark_enclosed(grid)
		return count_sides(grid)

