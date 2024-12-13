from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any

class Day(AOCDay):
	coord_up = Coordinate(0, -1)
	coord_down = Coordinate(0, 1)
	coord_left = Coordinate(-1, 0)
	coord_right = Coordinate(1, 0)

	def solve(self, bulk_discount = False):
		pos_checked: set[Coordinate] = set()
		price_total = 0

		for pos in self.farm.getActiveCells():
			if pos in pos_checked:
				continue

			check_queue = {pos}
			plant_type = self.farm.get(pos)
			region_pos: set[Coordinate] = set()
			perimeter = 0

			while check_queue:
				pos = check_queue.pop()
				pos_checked.add(pos)

				neigh_all = pos.getNeighbours(includeDiagonal = False)
				neigh_same_plant = set(np for np in neigh_all if self.farm.get(np) == plant_type)

				check_queue |= (neigh_same_plant - region_pos)
				region_pos.add(pos)
				region_pos |= neigh_same_plant
				perimeter += 4 - len(neigh_same_plant)

			# print(f"type {plant_type} area {len(region_pos)} perimeter {perimeter} -- {region_pos}")

			if not bulk_discount:
				price_total += len(region_pos) * perimeter
				continue

			# part 2

			sides = 0

			for pos in region_pos:
				# top side, walking right
				if self.is_side_end(pos, plant_type, walk_heading = self.coord_right, perimeter_heading = self.coord_up):
					sides += 1

				# bottom side, walking right
				if self.is_side_end(pos, plant_type, walk_heading = self.coord_right, perimeter_heading = self.coord_down):
					sides += 1

				# left side, walking down
				if self.is_side_end(pos, plant_type, walk_heading = self.coord_down, perimeter_heading = self.coord_left):
					sides += 1

				# right side, walking down
				if self.is_side_end(pos, plant_type, walk_heading = self.coord_down, perimeter_heading = self.coord_right):
					sides += 1

				continue

			# print(f"type {plant_type} area {len(region_pos)} sides {sides}")
			price_total += len(region_pos) * sides

		return price_total

	def is_side_end(self, pos: Coordinate, plant_type: str, walk_heading: Coordinate, perimeter_heading: Coordinate) -> bool:
		pos_side_continuation = pos + walk_heading

		if self.farm.get(pos + perimeter_heading) == plant_type:
			return False

		if self.farm.get(pos_side_continuation) != plant_type:
			return True

		return self.farm.get(pos_side_continuation + perimeter_heading) == plant_type

	def part1(self) -> Any:
		self.farm = Grid.from_data(self.getInput(), default = None)
		return self.solve()

	def part2(self) -> Any:
		self.farm = Grid.from_data(self.getInput(), default = None)
		return self.solve(bulk_discount = True)

	inputs = [
		[
			(1930, "input12-test"),
			(1446042, "input12"),
		],
		[
			(1206, "input12-test"),
			(902742, "input12"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 12)
	day.run(verbose=True)
