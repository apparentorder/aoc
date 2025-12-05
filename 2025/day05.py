from tools.aoc import AOCDay
from typing import Any, Tuple

class Day(AOCDay):
	def parse_input(self) -> list[Any]:
		return self.getInput()

	def parse(self) -> Tuple[list[range], list[int]]:
		input_ranges, input_ingredients = self.getMultiLineInputAsArray()
		ingredient_list = list(map(int, input_ingredients))
		range_list = [
			range(int(start), int(end) + 1)
			for start, end in (x.split('-') for x in input_ranges)
		]

		return range_list, ingredient_list

	def part1(self) -> Any:
		range_list, ingredient_list = self.parse()
		return sum(
			1 for ingredient in ingredient_list
			if any(ingredient in r for r in range_list)
		)

	def part2(self) -> Any:
		range_list, _ = self.parse()
		range_list.sort(key = lambda r: r.start)

		fresh = 0
		while len(range_list) > 0:
			current_range = range_list.pop(0)

			done = False
			while not done:
				for i in range(len(range_list)):
					if range_list[i].start > current_range.stop:
						done = True
						break

					current_range = range(current_range.start, max(current_range.stop, range_list[i].stop))
					range_list.pop(i)
					break # repeat
				else:
					done = True

			fresh += len(current_range)

		return fresh

	inputs = [
		[
			(3, "input5-test"),
			(782, "input5-penny"),
			(611, "input5"),
		],
		[
			(14, "input5-test"),
			(353863745078671, "input5-penny"),
			(345995423801866, "input5"),
		]
	]

if __name__ == '__main__':
	day = Day(2025, 5)
	day.run(verbose=True)
