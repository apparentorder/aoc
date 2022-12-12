import copy
from tools.aoc import AOCDay
from tools.ocr_ascii import AsciiOcr
from typing import Any

def parse(input):
	return [list(line) for line in input]

def get_pos(height_map, height): # returns [pos]
	r = []

	for y, row in enumerate(height_map):
		for x, c in enumerate(row):
			if c == height:
				r += [(x,y)]

	return r

def find_least_steps(height_map, start, end):
	active_paths = start
	least_steps = [[None for x in height_map[0]] for y in height_map]

	for spx, spy in start:
		least_steps[spy][spx] = 0

	while len(active_paths) > 0:
		next_active_paths = []

		for pos_x, pos_y in active_paths:
			if (pos_x, pos_y) == end:
				continue

			pos_height = height_map[pos_y][pos_x]
			pos_steps = least_steps[pos_y][pos_x]

			#print(f"at ({pos_x},{pos_y})@{pos_height} after steps={pos_steps}")
			if pos_steps > 1000:
				raise Exception("too tired")

			candidate_pos = [
				(pos_x    , pos_y + 1),
				(pos_x + 1, pos_y    ),
				(pos_x    , pos_y - 1),
				(pos_x - 1, pos_y    ),
			]

			for cand_x, cand_y in candidate_pos:
				if not 0 <= cand_x < len(height_map[0]):
					continue

				if not 0 <= cand_y < len(height_map):
					continue

				cand_height = height_map[cand_y][cand_x]
				cand_steps = least_steps[cand_y][cand_x]

				if not ord(pos_height) + 1 >= ord(cand_height):
					continue

				if cand_steps != None and cand_steps <= pos_steps + 1:
					continue

				#print(f"adding candidate ({cand_x},{cand_y}) steps {pos_steps} -> {cand_steps} height {pos_height} -> {cand_height}")

				least_steps[cand_y][cand_x] = pos_steps + 1
				next_active_paths += [(cand_x, cand_y)]

		active_paths = next_active_paths

	return least_steps[end[1]][end[0]]

class Day(AOCDay):
	inputs = [
		[
			(31, '12-test')
			,(468, '12')
		],
		[
			(29, '12-test')
			,(459, '12')
		]
	]

	def part1(self) -> Any:
		height_map = parse(self.getInput())
		start = get_pos(height_map, 'S')
		end = get_pos(height_map, 'E')[0]

		height_map[start[0][1]][start[0][0]] = 'a'
		height_map[end[1]][end[0]] = 'z'

		return find_least_steps(height_map, start, end)

	def part2(self) -> Any:
		height_map = parse(self.getInput())
		start  = get_pos(height_map, 'S')
		start += get_pos(height_map, 'a')
		end = get_pos(height_map, 'E')[0]

		height_map[start[0][1]][start[0][0]] = 'a'
		height_map[end[1]][end[0]] = 'z'

		return find_least_steps(height_map, start, end)

