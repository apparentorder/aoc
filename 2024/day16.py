from tools.aoc import AOCDay
from tools.coordinate import Coordinate
from tools.grid import Grid
from typing import Any
import re
import sys
sys.setrecursionlimit(10000)

class Day(AOCDay):
	def solve(self, is_part2: bool):
		start = next(self.grid.find("S"))
		end = next(self.grid.find("E"))

		unvisited = set(pos for pos in self.grid.getActiveCells() if self.grid.get(pos) not in ["#"])
		distance: dict[Coordinate, int] = { pos: 2**64 for pos in unvisited }
		distance[start] = 0
		prev: dict[Coordinate, Coordinate] = {}

		while len(unvisited) > 0:
			pos = sorted(unvisited, key = lambda d: distance[d])[0]
			pos_heading = (prev[pos] - pos) if pos in prev else Coordinate(1, 0)

			if distance[pos] == 2**64 or (pos == end and not is_part2):
				break

			for neighbor in unvisited & set(self.grid.getNeighboursOf(pos, includeDiagonal = False)):
				neighbor_distance_via_pos = distance[pos] + 1
				neighbor_heading_via_pos = pos - neighbor
				if pos_heading != neighbor_heading_via_pos:
					neighbor_distance_via_pos += 1000

				if neighbor_distance_via_pos < distance[neighbor]:
					distance[neighbor] = neighbor_distance_via_pos
					prev[neighbor] = pos

			unvisited.remove(pos)

		if not is_part2:
			return distance[end]

		known_tiles: set[Coordinate] = set([start, end])
		known_tiles_unvisited: set[Coordinate] = set([end])

		while known_tiles_unvisited:
			tile = known_tiles_unvisited.pop()
			valid_neighbors = distance.keys() - known_tiles
			for neighbor in valid_neighbors & set(self.grid.getNeighboursOf(tile, includeDiagonal = False)):
				neighbor_expected_distance = distance[prev[tile]]

				tile_next = next((t for t in self.grid.getNeighboursOf(tile) if t in known_tiles and t != prev[tile]), None)
				if prev.get(tile) and tile_next:
					neighbor_heading = neighbor - tile
					tile_heading = tile - tile_next
					prev_heading = prev[tile] - tile

					if neighbor_heading == tile_heading:
						# the original path has one more turn, so the alternative path
						# continues straight through tile and therefore must have had
						# one more turn elsewhere
						neighbor_expected_distance += 1000
					elif prev_heading == tile_heading:
						# or vice versa.
						neighbor_expected_distance -= 1000

				if distance[neighbor] != neighbor_expected_distance: # not an equal-cost path
					continue

				pos = neighbor
				while pos and not pos in known_tiles:
					known_tiles.add(pos)
					known_tiles_unvisited.add(pos)
					pos = prev.get(pos)

		# for tile in known_tiles: self.grid.set(tile, "o")
		# self.grid.print()

		return len(known_tiles)

	def part1(self) -> Any:
		self.grid = Grid.from_data(self.getInput(), default = None)
		return self.solve(is_part2 = False)

	def part2(self) -> Any:
		self.grid = Grid.from_data(self.getInput(), default = None)
		return self.solve(is_part2 = True)

	inputs = [
		[
			(11048, "input16-test"),
			(109496, "input16"),
		],
		[
			(64, "input16-test"),
			(551, "input16"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 16)
	day.run(verbose=True)
