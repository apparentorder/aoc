from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any

class Day(AOCDay):
	all_box_chars = {"[", "]", "O"}

	def walk(self):
		robot = next(self.map.find("@"))
		boxes_are_wide = bool(next(self.map.find("["), None))

		for move in self.moves:
			next_pos = robot + move
			todo = {next_pos}
			affected_boxes: set[Coordinate] = set()
			can_move = True

			while todo:
				box_pos = todo.pop()
				box_char = self.map.get(box_pos)

				if box_char == "#":
					can_move = False
					affected_boxes.clear()
					break

				if box_char not in self.all_box_chars:
					# done successfully (but check remaining todo)
					continue

				if box_char == "]":
					box_pos -= Coordinate(1, 0)
					box_char = "["

				if box_pos in affected_boxes:
					continue

				affected_boxes.add(box_pos)

				todo.add(box_pos + move)
				if boxes_are_wide and move.x > 0:
					todo.add(box_pos + Coordinate(move.x * 2, 0))
				elif boxes_are_wide and move.x == 0:
					todo.add(box_pos + move + Coordinate(1, 0))

			for box_pos in affected_boxes:
				self.map.set(box_pos, ".")
				if boxes_are_wide:
					self.map.set(box_pos + Coordinate(1, 0), ".")

			for box_pos in affected_boxes:
				if boxes_are_wide:
					self.map.set(box_pos + move, "[")
					self.map.set(box_pos + move + Coordinate(1, 0), "]")
				else:
					self.map.set(box_pos + move, "O")

			if can_move:
				self.map.set(robot, ".")
				robot += move
				self.map.set(robot, "@")

			# self.map.print()
			# print()

	def parse(self):
		input_map, input_moves = self.getMultiLineInputAsArray()
		self.map = Grid.from_data(input_map, default = None)

		move_map = {
			"^": Coordinate(0, -1),
			">": Coordinate(1, 0),
			"v": Coordinate(0, 1),
			"<": Coordinate(-1, 0),
		}

		self.moves = [move_map[c] for c in "".join(input_moves) if c in move_map]

	def expand_map(self):
		new_map = Grid(default = None)

		for pos in self.map.getActiveCells():
			c = self.map.get(pos)
			new_pos = Coordinate(pos.x * 2, pos.y)

			if c == "#":
				new_map.set(new_pos, "#")
				new_map.set(new_pos + Coordinate(1, 0), "#")
			elif c == "O":
				new_map.set(new_pos, "[")
				new_map.set(new_pos + Coordinate(1, 0), "]")
			elif c == ".":
				new_map.set(new_pos, ".")
				new_map.set(new_pos + Coordinate(1, 0), ".")
			elif c == "@":
				new_map.set(new_pos, "@")
				new_map.set(new_pos + Coordinate(1, 0), ".")

		self.map = new_map

	def get_gps(self):
		return sum(
			100 * pos.y + pos.x
			for pos in self.map.getActiveCells()
			if self.map.get(pos) in ["O", "["]
		)

	def part1(self) -> Any:
		self.parse()
		self.walk()
		return self.get_gps()

	def part2(self) -> Any:
		self.parse()
		self.expand_map()
		self.walk()
		return self.get_gps()

	inputs = [
		[
			(2028, "input15-test-small"),
			(10092, "input15-test"),
			(1349898, "input15"),
		],
		[
			(618, "input15-test-p2"),
			(9021, "input15-test"),
			(1376686, "input15"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 15)
	day.run(verbose=True)
