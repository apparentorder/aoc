from tools.coordinate import Coordinate
from tools.aoc import AOCDay
from math import prod
from typing import Any

class Day(AOCDay):
	def solve(self, part1_limit: int | None) -> int:
		unconnected_list = [
			(box_a, box_b)
			for ia, box_a in enumerate(self.box_list)
			for box_b in self.box_list[ia + 1:]
		]

		unconnected_list.sort(key = lambda pair: pair[0].getDistanceTo(pair[1]))
		unconnected_list = unconnected_list[:part1_limit]

		len_by_circuit_id = { id: 1 for id in range(len(self.box_list)) }
		circuit_id_by_box = { box: id for id, box in enumerate(self.box_list) }

		while len(unconnected_list) > 0:
			(box_a, box_b) = unconnected_list.pop(0)

			from_circuit_id = circuit_id_by_box[box_a]
			to_circuit_id = circuit_id_by_box[box_b]

			if from_circuit_id == to_circuit_id:
				continue

			len_by_circuit_id[to_circuit_id] += len_by_circuit_id[from_circuit_id]
			del len_by_circuit_id[from_circuit_id]

			for box, id in circuit_id_by_box.items():
				if id == from_circuit_id:
					circuit_id_by_box[box] = to_circuit_id

			if not part1_limit and len_by_circuit_id[to_circuit_id] == len(self.box_list):
				return box_a.x * box_b.x

		return prod(sorted(len_by_circuit_id.values())[-3:])

	def parse_input(self) -> list[Any]:
		return [
			Coordinate(*tuple(map(int, line.split(","))))
			for line in self.getInput()
		]

	def part1(self) -> Any:
		self.box_list = self.parse_input()
		return self.solve(part1_limit = 1000 if len(self.box_list) > 100 else 10)

	def part2(self) -> Any:
		self.box_list = self.parse_input()
		return self.solve(part1_limit = None)

	inputs = [
		[
			(40, "input8-test"),
			(140008, "input8-penny"),
			(112230, "input8"),
		],
		[
			(25272, "input8-test"),
			(9253260633, "input8-penny"),
			(2573952864, "input8"),
		]
	]

if __name__ == '__main__':
	day = Day(2025, 8)
	day.run(verbose=True)
