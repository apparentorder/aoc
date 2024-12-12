from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any

class Day(AOCDay):
	cache: dict[int, dict[int, int]] = {} # cache[stone_number] = entry[blink_count] = stone_count

	def count_stones(self, stone_number: int, blink_count: int):
		cache_entry_stone_number = self.cache.setdefault(stone_number, {})
		if cache_entry_blink_count := cache_entry_stone_number.get(blink_count):
			return cache_entry_blink_count

		if blink_count == 0:
			return 1

		stone_count = 0
		s = str(stone_number)

		if stone_number == 0:
			stone_count += self.count_stones(1, blink_count - 1)
		elif len(s) % 2 == 0:
			# split in two stones
			stone_count += self.count_stones(int(s[:len(s)//2]), blink_count - 1)
			stone_count += self.count_stones(int(s[len(s)//2:]), blink_count - 1)
		else:
			stone_count += self.count_stones(stone_number*2024, blink_count - 1)

		cache_entry_stone_number[blink_count] = stone_count
		return stone_count

	def part1(self) -> Any:
		input = map(int, self.getInput().split())
		return sum(self.count_stones(n, blink_count = 25) for n in input)

	def part2(self) -> Any:
		input = map(int, self.getInput().split())
		return sum(self.count_stones(n, blink_count = 75) for n in input)

	inputs = [
		[
			(55312, "input11-test"),
			(183435, "input11"),
		],
		[
			(218279375708592, "input11"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 11)
	day.run(verbose=True)
