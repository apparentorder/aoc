from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any, Iterable

class Day(AOCDay):
	def parse(self):
		self.byte_list: list[Coordinate] = []

		for line in self.getInput():
			line.replace("(", "")
			line.replace(")", "")
			x, y = map(int, line.split(","))
			self.byte_list += [Coordinate(x, y)]

	def setup_grid(self):
		self.map = Grid()
		for x in range(self.exit.x + 1):
			for y in range(self.exit.y + 1):
				self.map.set(Coordinate(x, y), ".")

	def part1(self) -> Any:
		self.parse()
		self.start = Coordinate(0, 0)
		if len(self.byte_list) < 100:
			self.exit = Coordinate(6, 6)
			self.byte_count = 12
		else:
			self.exit = Coordinate(70, 70)
			self.byte_count = 1024

		self.setup_grid()

		for byte_pos in self.byte_list[:self.byte_count]:
			self.map.set(byte_pos, "#")

		return len(self.map.getPath(self.start, self.exit, includeDiagonal = False, walls = ["#"])) - 1

	def part2(self):
		_ = self.part1() # setup and mark the first `byte_count` entries

		last_path = self.map.getPath(self.start, self.exit, includeDiagonal=False, walls=["#"])
		for byte_pos in self.byte_list[self.byte_count:]:
			self.map.set(byte_pos, "#")

			if byte_pos in last_path:
				last_path = self.map.getPath(self.start, self.exit, includeDiagonal=False, walls=["#"])

				if last_path is None:
					return f"{byte_pos.x},{byte_pos.y}"

	inputs = [
		[
			(22, "input18-test"),
			(374, "input18"),
		],
		[
			("6,1", "input18-test"),
			("30,12", "input18"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 18)
	day.run(verbose=True)
