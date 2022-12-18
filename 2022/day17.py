import time
import os
from tools.coordinate import Coordinate
from tools.grid import Grid
from tools.aoc import AOCDay
from typing import Any
import re

class TetrisGrid(Grid):
	def get_height(grid):
		# the Grid class doesn't update (reduce) boundaries after clearing fields,
		# so we need to count the grid height ourselves
		return max(abs(c.y) for c in grid.getActiveCells())

	def __str__(self):
		s = ""
		for y in self.rangeY():
			for x in self.rangeX():
				s += self.get(Coordinate(x, y))
				s += " "

			s += "\n"

		return s

class Shape(TetrisGrid):
	def __get_coords(self):
		return [Coordinate(c.x + self.offset_x, c.y + self.offset_y) for c in self.getActiveCells()]

	def __init__(self, grid, shape_id):
		self.parent_grid = grid
		self.parent_grid_max_x = grid.getBoundaries()[2]
		super().__init__(" ")

		for point in Shape.shapes[shape_id]:
			c = Coordinate(point[0], point[1])
			self.set(c)

	def start(self):
		shape_height = self.getBoundaries()[3] + 1
		self.offset_x = 2
		self.offset_y = -(self.parent_grid.get_height() + 3 + shape_height)

	def move(self, movement):
		self.offset_x += movement.x
		self.offset_y += movement.y

		shape_fits = self.test_fit()

		if not shape_fits:
			self.offset_x -= movement.x
			self.offset_y -= movement.y

		return shape_fits

	def test_fit(self):
		for c in self.__get_coords():
			if not (c.y < 0 and 0<=c.x<=self.parent_grid_max_x and not self.parent_grid.isSet(c)):
				return False

		return True

	def persist_to_grid(self):
		shape_fits = self.test_fit()

		if shape_fits:
			for c in self.__get_coords():
				self.parent_grid.set(c, "#")

		return shape_fits

	def __str__(self):
		# n.b.: this doesn't check for fit, so it might overwrite something
		coords = self.__get_coords()
		for c in coords:
			self.parent_grid.set(c, "@")
		s = str(self.parent_grid)
		for c in coords:
			self.parent_grid.set(c, " ")

		return s

	shapes = [
			[
				# horizontal bar
				(0,0), (1,0), (2,0), (3,0),
			], [
				# plus sign
				(1,0),
				(0,1), (1,1), (2,1),
				(1,2),
			], [
				# crazy L
				(2,0),
				(2,1),
				(0,2), (1,2), (2,2),
			], [
				# vertical bar
				(0,0), (0,1), (0,2), (0,3),
			], [
				# square
				(0,0), (1,0),
				(0,1), (1,1),
			]
	]

def tetris(jets, rock_count, animated = False):
	grid = TetrisGrid(" ")

	# floor
	for x in range(7):
		grid.set(Coordinate(x, 0), "=")

	move_right = Coordinate(1, 0)
	move_left = Coordinate(-1, 0)
	move_down = Coordinate(0, +1)

	shapes = [Shape(grid, i) for i in range(len(Shape.shapes))]

	jet_count = 0
	states = {}

	if animated:
		# clear screen
		print(chr(0o33) + "[2J")
		screen_lines = os.get_terminal_size()[1]

	i_rock = 0
	while i_rock < rock_count:
		i_shape = i_rock % len(shapes)
		shape = shapes[i_shape]
		shape.start()
		#print(shape)

		while True:
			i_jet = jet_count % len(jets)
			movement = move_right if jets[i_jet] == ">" else move_left
			shape.move(movement)
			jet_count += 1

			#print(f"movement: {jets[jet_count]}")

			#print(f"movement: down")
			if not shape.move(move_down):
				shape.persist_to_grid()

				state = {
					"i_jet": i_jet,
					"i_shape": i_shape,
					"i_rock": i_rock,
				}
				result = check_repeat(grid, rock_count=rock_count, states=states, state=state)

				if result:
					if animated:
						print(chr(0o33) + f"[{screen_lines - 3};0H")
						print("ANIMATION STOPPED, pattern repeats now")

					return result

				break

			if animated:
				output = str(shape)
				output_lines = list(output).count("\n") + 1

				draw_y = screen_lines - output_lines - 3
				#print(f"draw_y {draw_y}")
				if draw_y <= 0:
					print(chr(0o33) + f"[{screen_lines - 3};0H")
					print("ANIMATION STOPPED, terminal size exceeded")
					animated = False
				else:
					print(chr(0o33) + f"[{draw_y};0H")
					print(shape)
					time.sleep(0.2)

			#print(shape)

		i_rock += 1

	return grid.get_height()

def check_repeat(grid, rock_count, states, state):
	# height_pattern: for every column, note the highest point's
	# difference from the top
	state["height"] = grid.get_height()
	hp = [0 for _ in range(7)]
	for c in grid.getActiveCells():
		hp[c.x] = max(hp[c.x], abs(c.y)) - state["height"]
	state["height_pattern"] = hp

	state_key = str((state["i_jet"], state["i_shape"], state["height_pattern"]))

	if not state_key in states:
		states[state_key] = state
		return None

	# we found a previous state with this configuration, so from here on the
	# results repeat. calculate the height after all rocks.

	#print(f"repeating state at i_jet {state['i_jet']}, i_shape {state['i_shape']}")
	first_state = states[state_key]

	# calc the number of rocks and height gained in each repetition
	height_diff = state["height"] - first_state["height"]
	i_rock_diff = state["i_rock"] - first_state["i_rock"]
	#print(f"i_rock {first_state['i_rock']} -> {state['i_rock']} (+{i_rock_diff})")
	#print(f"height {first_state['height']} -> {state['height']} (+{height_diff})")

	# calc state after the last repetition
	skip_rocks = (rock_count - first_state["i_rock"] + 1) // i_rock_diff
	state["i_rock"] = first_state["i_rock"] + i_rock_diff * skip_rocks
	state["height"] = first_state["height"] + height_diff * skip_rocks
	rocks_remaining = rock_count - state["i_rock"] - 1

	#print(f"fast-forwarded to {state['i_rock']} (remaining: {rocks_remaining})")

	# for the remaining rocks (that are not a full repetition), lookup the height difference
	# in the corresponding previous state
	final_state = [s for s in states.values() if s["i_rock"] == first_state["i_rock"] + rocks_remaining][0]
	final_height = state["height"] + final_state["height"] - first_state["height"]
	#print(f"final state {final_state} final height {final_height}")
	return final_height

class Day(AOCDay):
	inputs = [
		[
			(3068, '17-test')
			,(3067, '17')
		],
		[
			(1_514_285_714_288, '17-test')
			,(1_514_369_501_484, '17')
		]
	]

	def part1(self) -> Any:
		jets = list(self.getInput())

		animate_test = False
		animate_real = False
		animate = True if (animate_test and len(jets) < 1000) or (animate_real and len(jets) >= 1000) else False

		return tetris(jets, 2022, animate)

	def part2(self) -> Any:
		jets = list(self.getInput())
		return tetris(jets, 1_000_000_000_000)

