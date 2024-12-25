from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate, DistanceAlgorithm
from typing import Any

class Day(AOCDay):
	def count_cheats(self, cheat_steps_allowed: int, threshold: int) -> int:
		path = list(reversed(self.track.getPath(self.start, self.end, includeDiagonal=False, walls=["#"])))
		steps_at_pos = {pos: i for i, pos in enumerate(path)}

		count = 0
		cheats_by_steps_saved: dict[int, int] = dict()

		# runs almost 20 seconds, hm.
		for path_i, start_pos in enumerate(path):
			for end_pos in path[path_i:]:
				distance = end_pos.getDistanceTo(start_pos, algorithm=DistanceAlgorithm.MANHATTAN)
				if distance > cheat_steps_allowed:
					continue

				cheat_for = steps_at_pos[end_pos] - steps_at_pos[start_pos] - distance
				if cheat_for >= threshold:
					count += 1
					cheats_by_steps_saved[cheat_for] = cheats_by_steps_saved.get(cheat_for, 0) + 1
					# print(f"cheat for {cheat_for} 1={start_pos} 2={end_pos}")

		# for k in sorted(cheats_by_steps_saved):
		# 	print(f"count={cheats_by_steps_saved[k]} with steps={k}")

		return count

	def parse(self):
		self.track = Grid.from_data(self.getInput())
		self.start = next(self.track.find("S"))
		self.end = next(self.track.find("E"))

	def part1(self) -> Any:
		self.parse()
		return self.count_cheats(cheat_steps_allowed = 2, threshold = 8 if self.is_test() else 100)

	def part2(self) -> Any:
		self.parse()
		return self.count_cheats(cheat_steps_allowed = 20, threshold = 50 if self.is_test() else 100)

	inputs = [
		[
			(14, "input20-test"),
			(1367, "input20"),
		],
		[
			(285, "input20-test"),
			(1006850, "input20"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 20)
	day.run(verbose=True)
