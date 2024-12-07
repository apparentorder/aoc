from tools.aoc import AOCDay
from tools.coordinate import Coordinate, DistanceAlgorithm
from tools.grid import Grid
from typing import Any, Dict

class Guard:
	heading_list = [
		Coordinate(0, -1),  # up
		Coordinate(1, 0),  # right
		Coordinate(0, 1),  # down
		Coordinate(-1, 0),  # left
	]

	def __init__(self, grid: Grid, start_pos: Coordinate):
		self.grid = grid
		self.start_pos = start_pos
		self.path_cache = {}
		self.loop_obstruction_pos = None
		self.reset()

	def set_loop_obstruction(self, pos):
		self.loop_obstruction_pos = pos
		self.grid.set(pos, "#")

	def reset(self):
		self.pos = self.start_pos
		self.heading = self.heading_list[0]

		if self.loop_obstruction_pos:
			self.grid.set(self.loop_obstruction_pos, ".")

	def turn(self):
		self.heading = self.heading_list[(self.heading_list.index(self.heading) + 1) % 4]

	def walk_line(self) -> str | None:
		while True:
			next_pos = self.pos + self.heading
			next_field = self.grid.get(next_pos)

			if next_field is None or next_field == "#":
				return next_field

			self.pos = next_pos

	def add_path_cache(self, from_pos: Coordinate, to_pos: Coordinate, next_heading: Coordinate | None):
		if self.loop_obstruction_pos:
			if from_pos.x == self.loop_obstruction_pos.x: return
			if from_pos.y == self.loop_obstruction_pos.y: return
			if to_pos.x == self.loop_obstruction_pos.x: return
			if to_pos.y == self.loop_obstruction_pos.y: return

		self.path_cache[from_pos] = (to_pos, next_heading)

	def get_path_cache(self, from_pos: Coordinate):
		if self.loop_obstruction_pos:
			if from_pos.x == self.loop_obstruction_pos.x: return None
			if from_pos.y == self.loop_obstruction_pos.y: return None

		entry = self.path_cache.get(from_pos)

		if self.loop_obstruction_pos and entry:
			if entry[0].x == self.loop_obstruction_pos.x: return None
			if entry[0].y == self.loop_obstruction_pos.y: return None

		return entry

	def patrol(self) -> list[Coordinate] | None:
		# n.b.: stop points cannot be at the edge of the map.

		route_points = [self.pos]
		next_field = "."
		while next_field:
			if cache_entry := self.get_path_cache(self.pos):
				self.pos = cache_entry[0]
				self.heading = cache_entry[1]
				next_field = "." if cache_entry[1] else None
			else:
				next_field = self.walk_line()
				while next_field == "#":
					# note: we might need two turns.
					self.turn()
					next_field = self.grid.get(self.pos + self.heading)

				cache_heading = self.heading if next_field else None
				self.add_path_cache(route_points[-1], self.pos, cache_heading)

			if self.pos in route_points[1:]:
				return None

			route_points += [self.pos]

		return route_points

	def get_patrol_route(self) -> [Coordinate]:
		route_points = self.patrol()

		# from the list of route stop points, build a full list of coordinates.
		route_pos_list = [route_points[0]]
		for i, rp in enumerate(route_points[:-1]):
			route_pos_list += rp.getLineTo(route_points[i+1])[1:]

		# print(route_pos_list)
		return route_pos_list

class Day(AOCDay):
	def part1(self) -> Any:
		grid = Grid.from_data(self.getInput(), default = None)
		start_pos = [pos for pos in grid.getActiveCells() if grid.get(pos) == "^"][0]
		guard = Guard(grid, start_pos)
		return len(set(guard.get_patrol_route()))

	def part2(self) -> Any:
		grid = Grid.from_data(self.getInput(), default = None)
		start_pos = [pos for pos in grid.getActiveCells() if grid.get(pos) == "^"][0]
		guard = Guard(grid, start_pos)
		valid_loop_pos = set()

		for pos in guard.get_patrol_route()[1:]:
			guard.reset()
			guard.set_loop_obstruction(pos)
			if guard.patrol() is None:
				valid_loop_pos.add(pos)

		return len(set(valid_loop_pos))

	inputs = [
		[
			(41, "input6-test"),
			(4374, "input6"),
		],
		[
			(6, "input6-test"),
			(1705, "input6"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 6)
	day.run(verbose=True)
