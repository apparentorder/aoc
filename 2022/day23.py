from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any
import json
import re

def parse(input):
	grid = Grid(".")

	for y, line in enumerate(input):
		for x, c in enumerate(list(line)):
			if c != ".":
				grid.set(Coordinate(x,y), c)

	return grid

moves = {
	"N":  Coordinate(0, -1),
	"NE":  Coordinate(1, -1),
	"NW":  Coordinate(-1, -1),

	"S":  Coordinate(0, 1),
	"SE":  Coordinate(1, 1),
	"SW":  Coordinate(-1, 1),

	"W":  Coordinate(-1, 0),
	"NW":  Coordinate(-1, -1),
	"SW":  Coordinate(-1, 1),

	"E":  Coordinate(1, 0),
	"NE":  Coordinate(1, -1),
	"SE":  Coordinate(1, 1),
}

proposal_groups = {
	"N": [moves["N"], moves["NE"], moves["NW"]],
	"S": [moves["S"], moves["SE"], moves["SW"]],
	"W": [moves["W"], moves["NW"], moves["SW"]],
	"E": [moves["E"], moves["NE"], moves["SE"]],
}

def spread(grid, times_limit = None):
	proposal_directions = ["N", "S", "W", "E"]

	#print(f"initial")
	#grid.print()
	#print()

	round = 1
	while True and ((times_limit is None) or (round <= times_limit)):
		proposed_positions = {}

		# first half: make proposals
		for elf_pos in grid.getActiveCells():
			# mark proposal positions
			found_any = False
			free_proposal_direction = None

			for pi in range(len(proposal_directions)):
				proposal_direction = proposal_directions[(pi + round - 1) % 4]
				for other_pos in proposal_groups[proposal_direction]:
					if grid.isSet(elf_pos + other_pos):
						found_any = True
						break
				else:
					free_proposal_direction = free_proposal_direction or proposal_direction # keep first match

				if found_any and free_proposal_direction:
					break

			if not found_any:
				continue

			if free_proposal_direction:
				target_pos = elf_pos + moves[free_proposal_direction]
				proposed_positions[elf_pos] = target_pos

		# second half: perform  proposed moves, if possible
		moved = False
		for proposing_elf_pos, target_pos in proposed_positions.items():
			if list(proposed_positions.values()).count(target_pos) == 1:
				moved = True
				grid.set(proposing_elf_pos, ".")
				grid.set(target_pos, "#")

		#print(f"== End of Round {round}")
		#grid.print()
		#print()

		if not moved:
			return round

		round += 1

	bounds = grid.getBoundaries()
	positions = (abs(bounds[0]) + abs(bounds[2]) + 1) * (abs(bounds[1]) + abs(bounds[3]) + 1)
	return positions - grid.getOnCount()

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

