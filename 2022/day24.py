from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any
import json
import re

class Blizzard:
	def __init__(self, pos, direction):
		self.pos = pos
		self.direction = None
		match direction:
			case "<": self.direction = (-1, 0)
			case ">": self.direction = ( 1, 0)
			case "^": self.direction = ( 0,-1)
			case "v": self.direction = ( 0, 1)

	def __repr__(self):
		return f"{self.direction}@{self.pos}"

class Valley:
	# n.b.: we're shaving off the border of "#" wall blocks, so start_pos
	# and end_pos are *not* within the bounds of the valley area.

	def __init__(self, input):
		self.blizzards = []
		self.blizzard_locations = set()
		lines = len(input)
		columns = len(input[0])

		for y in range(1, lines - 1):
			row = list(input[y])
			for x in range(1, columns - 1):
				if row[x] != ".":
					self.blizzards += [Blizzard((x-1, y-1), row[x])]

		self.maxX = columns - 3
		self.maxY = lines - 3
		self.start_pos = (0,-1)
		self.end_pos = (self.maxX, self.maxY + 1)

	def move_blizzards(self):
		self.blizzard_locations.clear()
		for b in self.blizzards:
			pos = pos_add(b.pos, b.direction)

			if pos[0] < 0:         pos = (self.maxX, pos[1])
			if pos[0] > self.maxX: pos = (        0, pos[1])
			if pos[1] < 0:         pos = (pos[0], self.maxY)
			if pos[1] > self.maxY: pos = (pos[0],         0)

			b.pos = pos
			self.blizzard_locations.add(pos)

def pos_add(c1, c2):
	return (c1[0] + c2[0], c1[1] + c2[1])

def spf(valley, start_pos, end_pos):
	states = set([start_pos])
	minute = 0

	while len(states) > 0:
		minute += 1
		valley.move_blizzards()

		next_states = set()
		for state in states:
			next_pos = [
				pos_add(state, (1,0)),
				pos_add(state, (0,1)),
				pos_add(state, (0,-1)),
				pos_add(state, (-1,0)),
				state, # wait
			]

			for try_pos in next_pos:
				valid_x = (0 <= try_pos[0] <= valley.maxX)
				valid_y = (0 <= try_pos[1] <= valley.maxY)
				if not ((valid_x and valid_y) or try_pos in [start_pos, end_pos]):
					continue

				if try_pos == end_pos:
					return minute

				if not try_pos in valley.blizzard_locations:
					next_states.add(try_pos)

		states = next_states

	raise Exception("no valid paths")

class Day(AOCDay):
	inputs = [
		[
			(18, '24-test'),
			(297, '24'),
		],
		[
			(54, '24-test'),
			(856, '24'),
		]
	]

	def part1(self) -> Any:
		valley = Valley(self.getInput())
		return spf(valley, start_pos = valley.start_pos, end_pos = valley.end_pos)

	def part2(self) -> Any:
		valley = Valley(self.getInput())
		trip1 = spf(valley, start_pos = valley.start_pos, end_pos = valley.end_pos)
		trip2 = spf(valley, start_pos = valley.end_pos, end_pos = valley.start_pos)
		trip3 = spf(valley, start_pos = valley.start_pos, end_pos = valley.end_pos)
		return sum([trip1, trip2, trip3])
		""

