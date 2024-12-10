from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any

class Day(AOCDay):
	# runs for ~15s on moderate hardware, some of opportunity to optimize,
	# e.g. weed out neighbors that are not "height + 1" instead of checking all neighbors over and over

	def parse(self):
		self.trailheads: list[int] = []
		self.peaks: list[int] = []
		self.grid = Grid(default = None)

		for y, row in enumerate(self.getInput(())):
			for x, height_s in enumerate(row):
				if height_s == ".":
					continue

				height = int(height_s)
				pos = Coordinate(x, y)
				self.grid.set(pos, height)

				if height == 0:
					self.trailheads += [pos]
				elif height == 9:
					self.peaks += [pos]

	def trailhead_score(self, trailhead_pos: Coordinate, count_all_paths: bool = False) -> int:
		score = 0

		for dest_pos in self.peaks:
			vhc = self.valid_hike_count(trailhead_pos, dest_pos)
			score += vhc if self.is_part2 else int(bool(vhc)) # for part 1, only count valid start/dest, not total path count

		return score

	def valid_hike_count(self, start_pos, dest_pos, path_so_far: list[Coordinate] = []) -> int | None:
		if start_pos == dest_pos:
			# print(f"trail end, path: {path_so_far}")
			return 1

		height = int(self.grid.get(start_pos))
		result = 0
		for neigh_pos in self.grid.getNeighboursOf(start_pos, includeDefault = False, includeDiagonal = False):
			neigh_height = self.grid.get(neigh_pos)
			if neigh_height != height + 1:
				continue

			vhc = self.valid_hike_count(neigh_pos, dest_pos, path_so_far + [neigh_pos])
			result += vhc

			if vhc > 0 and not self.is_part2:
				break

		return result

	def part1(self) -> Any:
		self.parse()
		self.is_part2 = False
		return sum(self.trailhead_score(trailhead_pos) for trailhead_pos in self.trailheads)

	def part2(self) -> Any:
		self.parse()
		self.is_part2 = True
		return sum(self.trailhead_score(trailhead_pos) for trailhead_pos in self.trailheads)

	inputs = [
		[
			(2, "input10-test1"),
			(4, "input10-test2"),
			(3, "input10-test3"),
			(36, "input10-test4"),
			(744, "input10"),
		],
		[
			(81, "input10-test4"),
			(1651, "input10"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 10)
	day.run(verbose=True)
