from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate, DistanceAlgorithm
from heapq import heappop, heappush
from typing import Any, NamedTuple, Self

class PathState(NamedTuple):
	block: Coordinate
	heading: Coordinate
	steps: int
	heat_loss: int

	def __lt__(self, other: Self):
		return self.heat_loss < other.heat_loss

class Day(AOCDay):
	def shortest_path(self, using_ultra_crucibles: bool):
		city_map = Grid.from_data(self.getInput())
		city_block_heat = {block: int(city_map.get(block)) for block in city_map.getActiveCells()}

		min_steps = 4 if using_ultra_crucibles else 1
		max_steps = 10 if using_ultra_crucibles else 3

		factory = Coordinate(city_map.maxX, city_map.maxY)

		path_state_list: list[PathState] = []
		# start list with the first step already made, in both valid directions from (0, 0)
		heappush(path_state_list, PathState(block = Coordinate(1, 0), heading=Coordinate(1, 0), heat_loss=0, steps=1))
		heappush(path_state_list, PathState(block = Coordinate(0, 1), heading=Coordinate(0, 1), heat_loss=0, steps=1))

		block_heading_visited: set[(Coordinate, Coordinate)] = set()

		while path_state_list:
			ps = heappop(path_state_list)
			if ps.block not in city_block_heat: # within map boundaries?
				continue

			if ps.steps == 1:
				# loop detection only for/at turning points, otherwise we miss
				# opportunities from overlapping path options
				if (ps.block, ps.heading) in block_heading_visited:
					continue

				block_heading_visited.add((ps.block, ps.heading))

			heat_loss = ps.heat_loss + city_block_heat[ps.block]

			if ps.block == factory:
				return heat_loss

			if ps.steps < max_steps:
				# max. steps not reached yet: continue on this heading
				heappush(path_state_list, PathState(
					block = ps.block + ps.heading,
					heading = ps.heading,
					heat_loss = heat_loss,
					steps = ps.steps + 1,
			       ))

			if ps.steps < min_steps:
				# min. steps not reached yet: do not turn left or right
				continue

			# add path states for "left" and "right" from the current heading
			next_heading = Coordinate(1, 0) if ps.heading.x == 0 else Coordinate(0, 1)
			for heading in [next_heading, next_heading * -1]:
				heappush(path_state_list, PathState(
					block = ps.block + heading,
					heading = heading,
					heat_loss = heat_loss,
					steps = 1,
				))

	def part1(self) -> Any:
		return self.shortest_path(using_ultra_crucibles=False)

	def part2(self) -> Any:
		return self.shortest_path(using_ultra_crucibles=True)

	inputs = [
		[
			(102, "input17-test"),
			(870, "input17-penny"),
			(1256, "input17"),
		],
		[
			(94, "input17-test"),
			(1063, "input17-penny"),
			(1382, "input17"),
		]
	]

if __name__ == '__main__':
	day = Day(2023, 17)
	day.run(verbose=True)
