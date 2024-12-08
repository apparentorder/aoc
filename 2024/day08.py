from tools.aoc import AOCDay
from tools.coordinate import Coordinate
from tools.grid import Grid
from typing import Any

class Day(AOCDay):
	def get_antinode_pos(self, is_part2 = False):
		antennas_by_frequency: dict[str, set[Coordinate]] = {}
		antinodes_by_frequency: dict[str, set[Coordinate]] = {}

		for pos in self.grid.getActiveCells():
			c = self.grid.get(pos)
			if c.isalnum():
				a = antennas_by_frequency.setdefault(c, set())
				a.add(pos)

		for frequency, antenna_a_pos_set in antennas_by_frequency.items():
			antinodes_by_frequency.setdefault(frequency, set())

			for antenna_a_pos in antenna_a_pos_set:
				for antenna_b_pos in antennas_by_frequency[frequency]:
					if antenna_b_pos == antenna_a_pos:
						continue

					diff = antenna_b_pos - antenna_a_pos

					if is_part2:
						antinode_pos = antenna_a_pos + diff
						while self.grid.isWithinBoundaries(antinode_pos):
							antinodes_by_frequency[frequency].add(antinode_pos)
							antinode_pos += diff
					else:
						antinode_pos = antenna_a_pos + diff * 2
						if self.grid.isWithinBoundaries(antinode_pos):
							antinodes_by_frequency[frequency].add(antinode_pos)

		return set(anpos for anset in antinodes_by_frequency.values() for anpos in anset)

	def part1(self) -> Any:
		self.grid = Grid.from_data(self.getInput(), default = None)
		return len(self.get_antinode_pos())

	def part2(self) -> Any:
		self.grid = Grid.from_data(self.getInput(), default = None)
		return len(self.get_antinode_pos(is_part2 = True))

	inputs = [
		[
			(2, "input8-test-two"),
			(14, "input8-test"),
			(244, "input8"),
		],
		[
			(34, "input8-test"),
			(912, "input8"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 8)
	day.run(verbose=True)
