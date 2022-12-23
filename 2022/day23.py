from tools.aoc import AOCDay
from typing import Any
import json
import re

def parse(input):
	grid = set()

	for y, line in enumerate(input):
		for x, c in enumerate(list(line)):
			if c != ".":
				grid.add((x,y))

	return grid

moves = {
	"N":  (0, -1),
	"NE":  (1, -1),
	"NW":  (-1, -1),

	"S":  (0, 1),
	"SE":  (1, 1),
	"SW":  (-1, 1),

	"W":  (-1, 0),
	"NW":  (-1, -1),
	"SW":  (-1, 1),

	"E":  (1, 0),
	"NE":  (1, -1),
	"SE":  (1, 1),
}

proposal_groups = {
	"N": [moves["N"], moves["NE"], moves["NW"]],
	"S": [moves["S"], moves["SE"], moves["SW"]],
	"W": [moves["W"], moves["NW"], moves["SW"]],
	"E": [moves["E"], moves["NE"], moves["SE"]],
}

def pos_add(p1, p2):
	return (p1[0] + p2[0], p1[1] + p2[1])

def spread(grid, times_limit = None):
	proposal_directions = ["N", "S", "W", "E"]

	#print(f"initial")
	#grid.print()
	#print()

	round = 0
	while True and ((times_limit is None) or (round <= times_limit)):
		proposed_positions = {}

		round += 1

		# first half: make proposals
		for elf_pos in grid:
			# mark proposal positions
			found_any = False
			free_proposal_direction = None

			for pi in range(len(proposal_directions)):
				proposal_direction = proposal_directions[(pi + round - 1) % 4]
				for other_pos in proposal_groups[proposal_direction]:
					if pos_add(elf_pos, other_pos) in grid:
						found_any = True
						break
				else:
					free_proposal_direction = free_proposal_direction or proposal_direction # keep first match

				if found_any and free_proposal_direction:
					break

			if not found_any:
				continue

			if free_proposal_direction:
				target_pos = pos_add(elf_pos, moves[free_proposal_direction])
				proposed_positions[elf_pos] = target_pos

		# second half: perform  proposed moves, if possible
		moved = False
		for proposing_elf_pos, target_pos in proposed_positions.items():
			if list(proposed_positions.values()).count(target_pos) == 1:
				moved = True
				grid.remove(proposing_elf_pos)
				grid.add(target_pos)

		#print(f"== End of Round {round}")
		#grid.print()
		#print()

		if not moved:
			return round

	minx = maxx = miny = maxy = 0
	for pos in grid:
		minx = min(pos[0], minx)
		maxx = max(pos[0], maxx)
		miny = min(pos[1], miny)
		maxy = max(pos[1], maxy)

	positions = (abs(minx) + abs(maxx) + 1) * (abs(miny) + abs(maxy) + 1)
	return positions - len(grid)

class Day(AOCDay):
	inputs = [
		[
			(110, '23-test')
			,(4070, '23')
		],
		[
			(20, '23-test')
			,(881, '23')
		]
	]

	def part1(self) -> Any:
		grid = parse(self.getInput())
		return spread(grid, 10)

	def part2(self) -> Any:
		grid = parse(self.getInput())
		return spread(grid, None)

