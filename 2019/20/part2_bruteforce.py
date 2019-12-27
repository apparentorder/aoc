#!/usr/bin/env python

import sys
import copy
import math
import pprint
from os import system
from time import sleep

f = open(sys.argv[1])
#f = open("aoc18in")
inputstring = f.read()
f.close()

debug_enabled = False

delay = 0

def debug(s):
	if debug_enabled:
		print(s)

class Coordinates:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

	def update(self, x, y):
		self.__init__(x, y)

	def copy(self):
		return Coordinates(self.x, self.y)

	def __str__(self):
		return "(%d,%d)" % (self.x, self.y)

	def iszero(self):
		return (self.x == 0 and self.y == 0)

	def __eq__(self, other):
		return (self.x == other.x) and (self.y == other.y)

	def __ne__(self, other):
		return not ((self.x == other.x) and (self.y == other.y))

class Map:
	def __init__(self, width, height):
		self.mapdata = [[MapField() for _ in range(height)] for _ in range(width)]
		self.width = width
		self.height = height

	def set_wall(self, coord):
		self.mapdata[coord.x][coord.y].is_wall = True

	def set_deadend(self, coord):
		self.mapdata[coord.x][coord.y].is_deadend = True

	def set_portal_letter(self, coord, value):
		self.mapdata[coord.x][coord.y].portal_letter = value

	def set_portal_entrance(self, coord, value):
		self.mapdata[coord.x][coord.y].portal_entrance = value

	def get(self, coord):
		return self.mapdata[coord.x][coord.y]

	def visited(self, coord):
		self.mapdata[coord.x][coord.y].visits += 1

	def all_coordinates(self):
		for x in range(self.width):
			for y in range(self.height):
				yield Coordinates(x, y)

	def surroundings(self, coord):
		# returns [0=up 1=down 2=left 3=right] field
		ret = []
		ret.append(Coordinates(coord.x, coord.y - 1))
		ret.append(Coordinates(coord.x, coord.y + 1))
		ret.append(Coordinates(coord.x - 1, coord.y))
		ret.append(Coordinates(coord.x + 1, coord.y))

		for i in range(len(ret) - 1, -1, -1):
			if ret[i].x < 0 or ret[i].y < 0:
				ret[i] = None
			elif ret[i].x >= self.width or ret[i].y >= self.height:
				ret[i] = None

		return ret

	def mark_deadends(self):
		# remove all deadends (i.e. fields that have exactly one opening
		# and have nothing useful on them)
		# we do this in sweeps, as marking a deadend might cause the
		# next deadend field to appear (think: deadend tunnel)
		while True:
			defound = 0
			for c in self.all_coordinates():
				f = self.get(c)
				if f.is_wall or f.is_deadend:
					continue

				if f.portal_letter is not None:
					continue

				opt = 0
				for s in self.surroundings(c):
					if s is None:
						continue
					f = self.get(s)
					if f.is_wall or f.is_deadend:
						continue

					opt += 1
				if opt == 1:
					# this is a deadend
					self.set_deadend(c)
					defound += 1
					#print("deadend: %s" % (c))

			if defound == 0:
				break
			print("marked %d deadends" % (defound))

class MapField:
	def __init__(self):
		self.visits = 0
		self.is_wall = False
		self.is_deadend = False
		self.portal_letter = None
		self.portal_entrance = None

class Maze:
	def __init__(self, inputstring):
		self.width = inputstring.find("\n")
		self.height = inputstring.count("\n")
		self.map = Map(self.width, self.height)
		self.routes = {}
		self.route_cache = {}
		self.pos_start = None
		self.pos_end = None
		self.portal_entrances = {}

		self.retrieve_map(inputstring)
		self.map.mark_deadends()
		self.mark_portals()
		self.mark_pos_start_end()

	def mark_pos_start_end(self):
		# scan map to find entries to/from AA and ZZ

		for c in self.map.all_coordinates():
			f = self.map.get(c)

			if f.portal_entrance == "AA":
				self.pos_start = c.copy()

			if f.portal_entrance == "ZZ":
				self.pos_end = c.copy()

		print("start %s end %s" % (self.pos_start, self.pos_end))

	def mark_portal_entrance(self, central_letter_pos, surroundings, walkable_surrounding_index):
		central_letter = self.map.get(central_letter_pos).portal_letter

		is_inner = False

		entrance_pos = surroundings[walkable_surrounding_index]

		if walkable_surrounding_index == 0:
			# entrance is up from here:
			# <entrance>
			# <centralletter>
			# <otherletter>
			other_letter = self.map.get(surroundings[1]).portal_letter
			portal_name = central_letter + other_letter
			is_inner = (central_letter_pos.y < self.height/2)

		elif walkable_surrounding_index == 1:
			# entrance is down from here:
			# <otherletter>
			# <centralletter>
			# <entrance>
			other_letter = self.map.get(surroundings[0]).portal_letter
			portal_name = other_letter + central_letter
			is_inner = (central_letter_pos.y > self.height/2)

		elif walkable_surrounding_index == 2:
			# entrance is left from here: <entrance><centralletter><otherletter>
			other_letter = self.map.get(surroundings[3]).portal_letter
			portal_name = central_letter + other_letter
			is_inner = (central_letter_pos.x < self.width/2)

		elif walkable_surrounding_index == 3:
			# entrance is right from here: <otherletter><centralletter><entrance>
			other_letter = self.map.get(surroundings[2]).portal_letter
			portal_name = other_letter + central_letter
			is_inner = (central_letter_pos.x > self.width/2)

		if portal_name not in self.portal_entrances:
			self.portal_entrances[portal_name] = {}

		if is_inner:
			self.portal_entrances[portal_name]["inner"] = entrance_pos.copy()
		else:
			self.portal_entrances[portal_name]["outer"] = entrance_pos.copy()

		self.map.set_portal_entrance(entrance_pos, portal_name)

	def mark_portals(self):
		# find all portals:
		# - scan map for portal letters
		# - scan their surroundings
		# - if we have one that
		#   a) has another letter nearby AND
		#   b) has a walkable field nearby
		# then
		# - we know the portal's full name
		# - we mark the walkable field as entrance
		#   to this portal

		for c in self.map.all_coordinates():
			f = self.map.get(c)

			if f.portal_letter is None:
				continue

			portal_name = None

			# this is a portal letter, great! scan
			# the surroundings.

			surr = self.map.surroundings(c)
			for i in range(len(surr)):
				if surr[i] is None:
					continue

				fp = self.map.get(surr[i])
				if fp.portal_letter is None and not fp.is_wall:
					self.mark_portal_entrance(c, surr, i)

	def retrieve_map(self, inputstring):
		pos = Coordinates(0, 0)
		for char in inputstring:
			if char == '#':
				self.map.set_wall(pos)

			if char == ' ':
				# treat open space as wall
				self.map.set_wall(pos)

			if ord(char) in range(65, 91):
				self.map.set_portal_letter(pos, char)

			if char == "\n":
				pos.update(0, pos.y + 1)
			else:
				pos.update(pos.x + 1, pos.y)

	def portal_other_side(self, portal_name, this_side):
		pe = self.portal_entrances[portal_name]

		if pe["inner"] == this_side:
			return pe["outer"], "outer"
		else:
			return pe["inner"], "inner"

	def find_path2(self, start, dest, depth = 0, pos_seen_in = {}, maze_level = 0):
		steps = 0
		indent = "   " * depth
		portals_used = []
		pos = start.copy()
		pos_seen = copy.deepcopy(pos_seen_in)

		#print(indent + "find_path2 depth=%d startpos=%s dest=%s pos_seen=%s" % (depth, start, dest, pos_seen))

		if depth > 600 or maze_level > 30:
			# seems to be a dead end
			print("aborting at depth %d maze_level %d" % (depth, maze_level))
			return None, None

		while True:
			if pos == dest and maze_level == 0:
				print("WE HAVE A WINNER! (depth %d)" % (depth))
				return steps, portals_used

			#print(indent + "... now at %s" % (state["pos"]))

			if maze_level not in pos_seen:
				pos_seen[maze_level] = []

			pos_seen[maze_level] += [str(pos)]

			portal = self.map.get(pos).portal_entrance
			if portal is not None and portal not in ['AA', 'ZZ']:
				label = "outer"
				if pos == self.portal_entrances[portal]["inner"]:
					label = "inner"

				if maze_level > 0 or label == "inner":
					pos, _ = self.portal_other_side(portal, this_side = pos)
					pos_seen[maze_level] += [str(pos)]
					steps += 1
					portals_used += ["%s(%s)@%d" % (portal, label, maze_level)]
					if label == "inner":
						maze_level += 1
					else:
						maze_level -= 1

					if maze_level not in pos_seen:
						pos_seen[maze_level] = []

			surr = self.map.surroundings(pos)
			options = []
			for s in surr:
				if s is None:
					continue

				field = self.map.get(s)

				if field.is_wall:
					#print(indent + "candidate %s: wall" % (s))
					continue

				if field.is_deadend:
					#print(indent + "candidate %s: deadend" % (s))
					continue

				if str(s) in pos_seen[maze_level]:
					# we've already been at that point
					#print(indent + "candidate %s: seen" % (s))
					continue

				# if we got here, this field is a valid option
				options += [s]
				#print(indent + "good candidate: %s" % (s))

			if len(options) == 0:
				#print(indent + "no options.")
				return None, None

			if len(options) == 1:
				# move to new field
				pos = options[0].copy()
				steps += 1
				#print(indent + "move immediately to %s" % (pos))

			if len(options) >= 2:
				# note: we could have MULTIPLE paths to get to our
				# destination (not in the examples, but in the puzzle input,
				# since there is multiple fields of space around the @ entrance)
				mins = 9999999
				minpu = None
				minpos = None
				for opt in options:
					new_pos = opt.copy()

					#print(indent + "start fp2 for %s -> %s" % (new_pos, dest))
					fp_steps, fp_portals_used = self.find_path2(start = new_pos,
						dest = dest,
						depth = depth + 1,
						maze_level = maze_level,
						pos_seen_in = pos_seen)

					#print(indent + "... fp2 %s-%s returned %s steps" % (new_pos, dest, fp_steps))

					if fp_steps is not None:
						if fp_steps < mins:
							mins = fp_steps
							minpu = fp_portals_used
							minpos = new_pos

				if minpu is not None:
					# n.b.: we have to count one (1) additional step
					# to account for starting fp2() at 'opt' instead
					# of our current position
					pos = minpos
					steps += mins + 1
					portals_used += minpu
					return steps, portals_used

				return None, None

	def find_shortest_wrapper(self):
		return self.find_path2(start = self.pos_start, dest = self.pos_end)

maze = Maze(inputstring)

print("map with width=%d height=%d" % (maze.width, maze.height))

#pprint.pprint(maze.portal_entrances)
#maze.calc_routes()
#pprint.pprint(maze.routes)

s, r = maze.find_shortest_wrapper()
print(s, r)

