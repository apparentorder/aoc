from tools.aoc import AOCDay
from tools.coordinate import Coordinate
from typing import Any

class Day(AOCDay):
	def get_word(self, from_coord: Coordinate, direction: Coordinate, word_length: int) -> str:
		pos = from_coord
		word_found = ""

		for _ in range(word_length):
			if pos.x not in self.range_x or pos.y not in self.range_y:
				return None

			word_found += self.input[pos.y][pos.x]
			pos += direction

		return word_found

	def scan_xmas(self, start_of_word: Coordinate):
		results = []
		results += [self.get_word(start_of_word, Coordinate(0,1), word_length = 4)]
		results += [self.get_word(start_of_word, Coordinate(0, -1), word_length = 4)]
		results += [self.get_word(start_of_word, Coordinate(1, 0), word_length = 4)]
		results += [self.get_word(start_of_word, Coordinate(-1, 0), word_length = 4)]
		results += [self.get_word(start_of_word, Coordinate(1, 1), word_length = 4)]
		results += [self.get_word(start_of_word, Coordinate(1, -1), word_length = 4)]
		results += [self.get_word(start_of_word, Coordinate(-1, 1), word_length = 4)]
		results += [self.get_word(start_of_word, Coordinate(-1, -1), word_length = 4)]

		return results.count("XMAS")

	def scan_x_mas(self, center_of_word: Coordinate):
		results = []
		results += [self.get_word(center_of_word + Coordinate(-1, -1), Coordinate(1, 1), word_length = 3)]
		results += [self.get_word(center_of_word + Coordinate(-1, 1), Coordinate(1, -1), word_length = 3)]

		if results.count("MAS") + results.count("SAM") == 2:
			return 1

		return 0

	def scan(self, scan_char: str, scan_function):
		match_count = 0

		for x in range(len(self.input[0])):
			for y in range(len(self.input)):
				if self.input[y][x] == scan_char:
					match_count += scan_function(Coordinate(x, y))

		return match_count

	inputs = [
		[
			(18, "input4-test"),
			(2591, "input4"),
		],
		[
			(9, "input4-test"),
			(1880, "input4"),
		]
	]

	def part1(self) -> Any:
		self.input = self.getInput()
		self.range_x = range(len(self.input[0]))
		self.range_y = range(len(self.input))

		return self.scan("X", self.scan_xmas)

	def part2(self) -> Any:
		self.input = self.getInput()
		self.range_x = range(len(self.input[0]))
		self.range_y = range(len(self.input))

		return self.scan("A", self.scan_x_mas)

if __name__ == '__main__':
	day = Day(2024, 4)
	day.run(verbose=True)
