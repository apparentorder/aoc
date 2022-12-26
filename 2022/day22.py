from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any
import json
import re
import time

WALL_CHAR = "⊘"

def parse(input, path_string_override = None):
	grid = Grid(" ")
	start_pos = None

	for y, line in enumerate(input):
		if line == "":
			break

		for x, c in enumerate(list(line)):
			pos = Coordinate(x,y)
			if c == "#":
				grid.set(pos, WALL_CHAR)
			elif c != " ":
				grid.set(pos, c)
				start_pos = start_pos or pos

	path = split_path(path_string_override or input[-1])

	# find smallest row, use that as grid size
	grid_size = grid.maxX
	for y in range(grid.maxY):
		limits = get_limits(grid, y=y)
		grid_size = min(grid_size, limits[-1] - limits[0] + 1)

	return grid, grid_size, path, start_pos

def split_path(path_string):
	s = ""
	path = []

	for c in list(path_string):
		if c.isnumeric():
			s += c
		else:
			if s != "":
				path += [s]
				s = ""
			path += [c]

	if s != "":
		path += [s]

	return path

class Direction:
	def __init__(self, i):
		self.i = i

	def __int__(self):
		return self.i

	def __str__(self):
		match self.i:
			case 0: return ">"
			case 1: return "v"
			case 2: return "<"
			case 3: return "^"
			case _: raise Exception("unreach")

	def coord(self):
		match self.i:
			case 0: return Coordinate(1,0)
			case 1: return Coordinate(0,1)
			case 2: return Coordinate(-1,0)
			case 3: return Coordinate(0,-1)
			case _: raise Exception("unreach")

	def rotate_right(self, count = 1):
		self.i = (self.i + count) % 4

	def rotate(self, c):
		self.rotate_right(3 if c == "L" else 1)

	def char_colored(self):
		return f"[33m{str(self)}[0m"

def get_limits(grid, x=None, y=None):
	if x is not None:
		y_values = sorted([c.y for c in grid.getActiveCells() if c.x == x])
		return y_values[0], y_values[-1]
	else:
		x_values = sorted([c.x for c in grid.getActiveCells() if c.y == y])
		return x_values[0], x_values[-1]

def follow_path_cube(grid, path, start_pos, start_facing, cube_mode_cube, debug = False):
	pos = start_pos
	facing = start_facing

	assert(cube_mode_cube is None or not debug) # debug cannot be used in non-cube_mode

	for move in path:
		if debug:
			grid.set(pos, facing.char_colored())

		if move in ["R", "L"]:
			facing.rotate(move)
			if debug:
				grid.set(pos, facing.char_colored())
			continue

		for _ in range(int(move)):
			# try direct movement
			next_pos = pos + facing.coord()
			next_facing = facing
			next_value = grid.get(next_pos)

			if next_value == " ":
				# cannot go further in this direction.
				# if cube_mode, call the cube's get_next_position() to see if
				# we can continue somewhere else.
				if cube_mode_cube is None:
					return None

				next_pos, next_facing = cube_mode_cube.get_next_position(pos, facing)
				next_value = grid.get(next_pos)

			if next_value == WALL_CHAR and cube_mode_cube is not None:
				# n.b.: in non-cube_mode, we only care if a position exists (is set)
				break

			pos = next_pos
			facing = next_facing

			if debug:
				grid.set(pos, facing.char_colored())
				print("[0;0H")
				grid.set(pos, "[31;1;4mX[0m")
				print(grid)
				grid.set(pos, facing.char_colored())
				#time.sleep(0.001)

		#print(f"pos after {move} now {pos} facing {facing}")

	#cube.grid.print()

	return pos, facing

class CubeMap:
	def __init__(self, grid, grid_size, wrap_only):
		self.grid = grid
		self.size = grid_size
		self.wrap_only = wrap_only

		# scan the Grid and create an additional Grid where each position
		# represents a
		self.cube = Grid(" ")
		for y in range(grid.maxY//self.size + 1):
			for x in range(grid.maxX//self.size + 1):
				if grid.isSet(Coordinate(x*self.size, y*self.size)):
					self.cube.set(Coordinate(x, y), WALL_CHAR)

		self.__generate_paths()

		# Of note:
		#   The starting position (top-left square) always represents the
		#   layout of the 2D map. All squares in the input map share the
		#   starting square's orientation! We need to figure out which square
		#   should be in which orientation to properly connect the cube squares.
		# ASSUMPTIONS: (some of which would be relevant only if we were to fully
		# scan and generate the cube)
		# - Cube will be unfolded in a 4x3 or 3x4 layout
		# - There will be a column of three squares downwards from the starting
		#   position. We'll regard those as being the top, front and bottom sides
		#   of the cube.
		# - This means that the top-left area of the input *must* be unused (as,
		#   otherwise, it would be the starting position)
		# - The left and right squares will be on the left and right side of the
		#   middle row, i.e. they are on the same Y-coordinate as one of the middle
		#   row fields.
		# - The remaining square is the back side of the cube.

	def __generate_paths(self):
		# based on possible layouts, i.e. possible paths that can be taken from
		# any one side of a cube to any other side of a cube, we define the steps
		# necessary to get to the other side. by doing so, we know which side it
		# is (relative to the originating side) and thus can rotate and flip
		# accordingly.
		#
		# note that any path is considered relative to it's current `facing` direction,
		# so it works for any "absolute" `facing` as seen on the 2D map.
		#
		# this list likely is incomplete and/or contains redundant entries that
		# should be covered by having another path be `reversible`.

		paths = [
			{
				# diagonally adjacent, connected via "side" square
				"path": split_path("1L1"),
				"rotate_right_path": 1,
				"rotate_right_position": 1,
				"reversible": True,
				"hflip": False,
				"vflip": False,
				"tags": "",
			},
			{
				# ...
				"path": split_path("2L1"),
				"rotate_right_path": 1,
				"rotate_right_position": 2,
				"reversible": False,
				"hflip": False,
				"vflip": False,
				"tags": "",
			},
			{
				# ...
				"path": split_path("1L2"),
				"rotate_right_path": 2, # backwards
				"rotate_right_position": 2,
				"reversible": False,
				"hflip": False,
				"vflip": False,
				"tags": "",
			},
			{
				# ...
				"path": split_path("2R1"),
				"rotate_right_path": 3, # left
				"rotate_right_position": 2,
				"reversible": False,
				"hflip": False,
				"vflip": False,
				"tags": "",
			},
			{
				# ...
				"path": split_path("2R1L1"),
				"rotate_right_path": 2, # back
				"rotate_right_position": 1,
				"reversible": True,
				"hflip": False,
				"vflip": False,
				"tags": "",
			},
			{
				# ...
				"path": split_path("1R1L2"),
				"rotate_right_path": 1,
				"rotate_right_position": 3,
				"reversible": False,
				"hflip": False,
				"vflip": False,
				"tags": "",
			},
			{
				# ...
				"path": split_path("1L2R1L1"),
				"rotate_right_path": 3, # left
				"rotate_right_position": 0,
				"reversible": False,
				"hflip": False,
				"vflip": False,
				"tags": "",
			},
			{
				# ...
				"path": split_path("1R1L2R1"),
				"rotate_right_path": 2, # back
				"rotate_right_position": 0,
				"reversible": False,
				"hflip": False,
				"vflip": False,
				"tags": "",
			},
		]

		# generate additional paths for `reversible` entries
		for i in range(len(paths)):
			p = paths[i]

			if not p["reversible"]:
				continue

			# flipped path
			flipped = p.copy()
			flipped["rotate_right_path"] = (p["rotate_right_path"] + 2) % 4
			flipped["rotate_right_position"] = (p["rotate_right_position"] + 2) % 4
			flipped["path"] = list(p["path"])

			flipped["tags"] += "flipped"
			paths += [flipped]

			# reversed path
			reversed = p.copy()
			reversed["rotate_right_path"] = (p["rotate_right_path"] + 2) % 4
			reversed["rotate_right_position"] = (p["rotate_right_position"] + 2) % 4
			reversed["path"] = []
			for move in p["path"]:
				if move == "L":
					reversed["path"] += ["R"]
				elif move == "R":
					reversed["path"] += ["L"]
				else:
					reversed["path"] += [move]
			reversed["path"].reverse()
			reversed["tags"] += "reversed"
			paths += [reversed]

			# reversed flipped path
			reversed_flipped = reversed.copy()
			reversed_flipped["rotate_right_path"] = (reversed["rotate_right_path"] + 2) % 4 # don't rotate for rev. flip (rotate back to normal)
			reversed_flipped["rotate_right_position"] = reversed["rotate_right_position"]
			reversed_flipped["path"] = list(reversed["path"])
			reversed["tags"] += "flipped"
			paths += [reversed_flipped]

		#print()
		#print(paths)

		# longest paths need to be tried first, so sort accordingly
		paths.sort(reverse = True, key = lambda p: len(p["path"]))

		self.cube_paths = paths

	def get_square_for_pos(self, grid_pos):
		return Coordinate(grid_pos.x // self.size, grid_pos.y // self.size)

	def get_next_position(self, pos, facing):
		if self.wrap_only: # part1
			limits_x = get_limits(self.grid, y = pos.y)
			limits_y = get_limits(self.grid, x = pos.x)
			match str(facing):
				case ">": return Coordinate(limits_x[0], pos.y), facing
				case "<": return Coordinate(limits_x[1], pos.y), facing
				case "v": return Coordinate(pos.x, limits_y[0]), facing
				case "^": return Coordinate(pos.x, limits_y[1]), facing

		square_pos = self.get_square_for_pos(pos)
		relative_x = pos.x % self.size
		relative_y = pos.y % self.size

		for try_path in self.cube_paths:
			try_facing = Direction((int(facing) + try_path["rotate_right_path"]) % 4)
			r = follow_path_cube(
				grid = self.cube,
				path = try_path["path"],
				cube_mode_cube = None,
				start_pos = square_pos,
				start_facing = try_facing,
			)

			if r is None:
				continue

			dest_square_pos = r[0]

			next_facing = Direction(facing.i)
			next_facing.rotate_right(try_path["rotate_right_position"])

			posx, posy = relative_x, relative_y
			# note that the starting position in the new square will be 0, this is accounted for
			for _ in range(try_path["rotate_right_position"]):
				oldx = posx
				posx = self.size - 1 - posy
				posy = oldx

			if next_facing.i in [1,3]: # up,down
				posy = self.size - 1 - posy

			if next_facing.i in [0,2]: # right,left
				posx = self.size - 1 - posx

			if try_path["hflip"]:
				posx = self.size - 1 - posx

			if try_path["vflip"]:
				posy = self.size - 1 - posy

			next_pos = Coordinate(dest_square_pos.x * self.size + posx, dest_square_pos.y * self.size + posy)

			#print(f"transition from square {square_pos} -> {dest_square_pos}, pos {pos} -> {next_pos}, facing {facing} -> {next_facing} using path {try_path['path']} [{try_path['tags']}]")

			return next_pos, next_facing

		self.grid.print()
		raise Exception(f"no connection from cube square {square_pos} facing {facing}")

class Day(AOCDay):
	inputs = [
		[
			(6032, '22-test'),
			(1428, '22-penny'),
			(191010, '22'),
		],
		[
			(5031, '22-test'),
			(142380, '22-penny'),
			(55364, '22'),
		]
	]

	def part1(self) -> Any:
		grid, grid_size, path, start_pos = parse(self.getInput())
		cube = CubeMap(grid, grid_size, wrap_only = True)
		pos, facing = follow_path_cube(
			grid = grid,
			path = path,
			cube_mode_cube = cube,
			start_pos = start_pos,
			start_facing = Direction(0),
			debug = False
		)
		return (pos.y+1)*1000 + (pos.x+1)*4 + int(facing)

	def part2(self) -> Any:
		grid, grid_size, path, start_pos = parse(self.getInput())
		cube = CubeMap(grid, grid_size, wrap_only = False)
		pos, facing = follow_path_cube(
			grid = grid,
			path = path,
			cube_mode_cube = cube,
			start_pos = start_pos,
			start_facing = Direction(0),
			debug = False
		)
		return (pos.y+1)*1000 + (pos.x+1)*4 + int(facing)

