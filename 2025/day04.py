from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any, Generator

class Day(AOCDay):
	def get_removable_rolls(self) -> list[Coordinate]:
		def is_removable_roll(roll_pos: Coordinate):
			return 4 > sum(
				1 for neigh_pos in roll_pos.getNeighbours(includeDiagonal = True)
				if self.grid.get(neigh_pos) == "@"
			)

		return [
			roll_pos for roll_pos in self.grid.find("@")
			if is_removable_roll(roll_pos)
		]

	def part1(self) -> Any:
		self.grid = Grid.from_data(self.getInput())
		return len(self.get_removable_rolls())

	def part2(self) -> Any:
		self.grid = Grid.from_data(self.getInput())
		count_removed = 0

		while True:
			removable_rolls_list = self.get_removable_rolls()
			if len(removable_rolls_list) == 0:
				break

			for removable_pos in removable_rolls_list:
				self.grid.set(removable_pos, "x")

			count_removed += len(removable_rolls_list)

		return count_removed

	inputs = [
		[
			(13, "input4-test"),
			(1376, "input4-penny"),
			(1435, "input4"),
		],
		[
			(43, "input4-test"),
			(8587, "input4-penny"),
			(8623, "input4"),
		]
	]

if __name__ == '__main__':
	day = Day(2025, 4)
	day.run(verbose=True)
