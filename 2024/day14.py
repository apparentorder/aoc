from tools.aoc import AOCDay
from tools.coordinate import Coordinate
from tools.grid import Grid
from typing import Any
import re

class Robot:
	def __init__(self, input_line, maxX: int, maxY: int):
		re_match = re.match(r'p=([0-9-]+),([0-9-]+) v=([0-9-]+),([0-9-]+)', input_line)

		self.pos = (int(re_match.group(1)), int(re_match.group(2)))
		self.velocity = (int(re_match.group(3)), int(re_match.group(4)))
		self.maxX = maxX
		self.midX = maxX // 2
		self.maxY = maxY
		self.midY = maxY // 2

	def move(self, count: int):
		x = (self.pos[0] + count * self.velocity[0]) % (self.maxX + 1)
		y = (self.pos[1] + count * self.velocity[1]) % (self.maxY + 1)
		self.pos = (x, y)

	def get_quadrant_index(self) -> int | None:
		if self.pos[0] < self.midX and self.pos[1] < self.midY: # top left
			return 0
		elif self.pos[0] > self.midX and self.pos[1] < self.midY: # top right
			return 1
		elif self.pos[0] < self.midX and self.pos[1] > self.midY: # bottom left
			return 2
		elif self.pos[0] > self.midX and self.pos[1] > self.midY: # bottom right
			return 3
		else:
			return None # on the middle line (or elsewhere)

class Day(AOCDay):
	def part1(self) -> Any:
		input_lines = self.getInput()

		maxX, maxY = 100, 102
		if len(input_lines) < 20:
			maxX, maxY = 10, 6

		robot_list = [Robot(line, maxX = maxX, maxY = maxY) for line in input_lines]

		quadrant_count = [0, 0, 0, 0]
		for robot in robot_list:
			robot.move(count = 100)
			if (qi := robot.get_quadrant_index()) is not None:
				quadrant_count[qi] += 1

		safety_factor = 1
		for qc in quadrant_count:
			safety_factor *= qc

		return safety_factor

	def part2(self) -> Any:
		input_lines = self.getInput()

		maxX, maxY = 100, 102
		if len(input_lines) < 20:
			maxX, maxY = 10, 6

		robot_list = [Robot(line, maxX = maxX, maxY = maxY) for line in input_lines]

		for i in range(1, 2**64):
			for robot in robot_list:
				robot.move(1)

			for robot in robot_list:
				# looking for a diagonal line "attached" to any of the robots.
				# runs for a minute or so. could optimize by hardcoding target positions and removing robots that can
				# never touch the target position, and possibly lcm'ing the needed steps, or something like that.
				coords = set((robot.pos[0] + offset, robot.pos[1] + offset) for offset in range(20))
				tree_bot_count = sum(1 for robot in robot_list if (robot.pos[0], robot.pos[1]) in coords)

				if tree_bot_count < 15:
					continue

				if False: # optional: show the tree!
					grid = Grid()
					for x in range(maxX + 1):
						for y in range(maxY + 1):
							grid.set(Coordinate(x, y), ".")

					for xmas_robot in robot_list:
						grid.set(Coordinate(xmas_robot.pos[0], xmas_robot.pos[1]), "X")

					grid.print()

				return i

	inputs = [
		[
			(12, "input14-test"),
			(230172768, "input14"),
		],
		[
			(8087, "input14"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 14)
	day.run(verbose=True)
