from tools.aoc import AOCDay
from tools.coordinate import Coordinate
from tools.grid import Grid
from typing import Any

class Keypad:
	layout_data = []

	def __init__(self):
		self.layout = Grid.from_data(self.layout_data)
		self.button_pos = {self.layout.get(pos): pos for pos in self.layout.getActiveCells()}
		self.controlling_keypad = self
		self.cache: dict[tuple[str, int], int] = {}

	def shortest_for_button_sequence(self, code: list[str], level: int) -> int:
		if level < 0:
			return len(code) # just press the damn buttons.

		cache_key = (str(code), level)
		if r := self.cache.get(cache_key):
			return r

		total_len = 0
		button_prev = "A" # any robot arm button sequence starts at "A"
		for button in code:
			possible_paths = self.best_path_list(self.button_pos[button_prev], self.button_pos[button])

			min_path_len = 2**64
			for path in possible_paths:
				# the next-level robot arm that needs to enter this sequence
				# will always end with a button push "A"
				moves = self.path_to_movements(path) + ["A"]
				path_len = self.controlling_keypad.shortest_for_button_sequence(moves, level = level - 1)
				min_path_len = min(min_path_len, path_len)

			total_len += min_path_len
			button_prev = button

		self.cache[cache_key] = total_len
		return total_len

	def best_path_list(self, from_pos: Coordinate, to_pos: Coordinate) -> list[list[Coordinate]]:
		path_list = [[from_pos]]
		path_list_complete = []

		min_path_len = 2**64
		while path_list:
			path = path_list.pop()

			if path[-1] == to_pos:
				path_list_complete += [path]
				min_path_len = min(min_path_len, len(path))
				continue

			if len(path) > min_path_len:
				continue

			for neighbor in self.layout.getNeighboursOf(path[-1], includeDiagonal=False):
				if self.layout.get(neighbor) is not None and neighbor not in path:
					path_list += [path + [neighbor]]

		return [p for p in path_list_complete if len(p) == min_path_len]

	@staticmethod
	def path_to_movements(path: list[Coordinate]):
		movements = {
			Coordinate(0, -1): "^",
			Coordinate(-1, 0): "<",
			Coordinate(0, 1): "v",
			Coordinate(1, 0): ">",
		}

		return [movements[path[i] - path[i-1]] for i in range(1, len(path))]

class NumericKeypad(Keypad):
	layout_data = [
		["7", "8", "9"],
		["4", "5", "6"],
		["1", "2", "3"],
		[None, "0", "A"],
	]

	def __init__(self):
		super().__init__()
		self.controlling_keypad = DirectionalKeypad()

class DirectionalKeypad(Keypad):
	layout_data = [
		[None, "^", "A"],
		["<", "v", ">"],
	]

class Day(AOCDay):
	def part1(self) -> Any:
		nk = NumericKeypad()
		return sum(
			int(code.replace("A", "")) * nk.shortest_for_button_sequence(code, level = 2)
			for code in self.getInput()
		)

	def part2(self) -> Any:
		nk = NumericKeypad()
		return sum(
			int(code.replace("A", "")) * nk.shortest_for_button_sequence(code, level = 25)
			for code in self.getInput()
		)

	inputs = [
		[
			(126384, "input21-test"),
			(152942, "input21"),
		],
		[
			(154115708116294, "input21-test"),
			(189235298434780, "input21"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 21)
	day.run(verbose=True)
