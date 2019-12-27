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

	def set_wall(self, coord):
		self.mapdata[coord.x][coord.y].is_wall = True

	def set_deadend(self, coord):
		self.mapdata[coord.x][coord.y].is_deadend = True

	def get(self, coord):
		return self.mapdata[coord.x][coord.y]

	def visited(self, coord):
		self.mapdata[coord.x][coord.y].visits += 1

class MapField:
	def __init__(self):
		self.visits = 0
		self.is_wall = False
		self.is_deadend = False

class Tunnel:
	def __init__(self, inputstring):
		self.width = inputstring.find("\n")
		self.height = inputstring.count("\n")
		self.map = Map(self.width, self.height)
		self.keys = {}
		self.doors = {}
		self.routes = {}
		self.route_cache = {}
		self.combinations = {}
		self.pos_start = {}

		self.retrieve_map(inputstring)

	def retrieve_map(self, inputstring):
		pos = Coordinates(0, 0)
		for char in inputstring:
			if char == '#':
				self.map.set_wall(pos)

			if char == '@':
				i = 0
				while str(i) in self.pos_start:
					i += 1
				self.pos_start[str(i)] = pos.copy()
				#print("got sp %d %s" % (i, self.pos_start[i]))

			if ord(char) in range(97, 123):
				self.keys[char] = pos.copy()

			if ord(char) in range(65, 91):
				self.doors[char] = pos.copy()

			if char == "\n":
				pos.update(0, pos.y + 1)
			else:
				pos.update(pos.x + 1, pos.y)

		# remove all deadends (i.e. fields that have exactly one opening
		# and have nothing useful on them)
		# we do this in sweeps, as marking a deadend might cause the
		# next deadend field to appear (think: deadend tunnel)
		defound = 0
		while True:
			defound = 0
			for x in range(self.width):
				for y in range(self.height):
					c = Coordinates(x, y)
					f = self.map.get(c)
					if f.is_wall or f.is_deadend:
						continue

					if c in map(lambda id: self.doors[id], self.doors.keys()):
						continue

					if c in map(lambda id: self.keys[id], self.keys.keys()):
						continue

					is_startpos = False
					for robot in self.pos_start:
						if self.pos_start[robot] == c:
							is_startpos = True
							break
					if is_startpos:
						continue

					opt = 0
					for s in self.surroundings(c):
						if s is None:
							continue
						f = self.map.get(s)
						if f.is_wall or f.is_deadend:
							continue

						opt += 1
					if opt == 1:
						# this is a deadend
						self.map.set_deadend(c)
						defound += 1
						#print("deadend: %s" % (c))

			if defound == 0:
				break
			print("marked %d deadends" % (defound))

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

	def find_path2(self, start, dest, depth = 0, blocking = [], pos_seen_in = []):
		steps = 0
		indent = "   " * depth
		blocking = list(blocking)
		pos = start.copy()
		pos_seen = list(pos_seen_in)

		#print(indent + "find_path2 depth=%d startpos=%s dest=%s pos_seen=%s" % (depth, start, dest, pos_seen))

		while True:
			if pos == dest:
				return steps, blocking

			# we could be starting fp2() on a key or door. in that
			# case we need to consider the recursion depth: if
			# this is the *first* call (depth 0), then we will
			# be on the key that we are starting from, but
			# we don't count this as blocking us. but for deeper
			# levels, we need to record other keys as blocking.
			if depth > 0 or pos != start:
				# check if this is a key or door
				for k in self.keys:
					if self.keys[k] == pos:
						blocking += [k]

				for k in self.doors:
					if self.doors[k] == pos:
						blocking += [k]

			#print(indent + "... now at %s" % (state["pos"]))
			pos_seen += [str(pos)]
			surr = self.surroundings(pos)
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

				if str(s) in pos_seen:
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
				minb = None
				minpos = None
				for opt in options:
					new_pos = opt.copy()

					#print(indent + "start fp2 for %s -> %s" % (new_pos, dest))
					fp_steps, fp_blocking = self.find_path2(start = new_pos,
						dest = dest,
						depth = depth + 1,
						pos_seen_in = list(pos_seen))

					#print(indent + "... fp2 %s-%s returned %s steps" % (new_pos, dest, fp_steps))

					if fp_steps is not None:
						if fp_steps < mins:
							mins = fp_steps
							minb = fp_blocking
							minpos = new_pos

				if minb is not None:
					# n.b.: we have to count one (1) additional step
					# to account for starting fp2() at 'opt' instead
					# of our current position
					pos = minpos
					steps += mins + 1
					blocking += minb
					return steps, blocking

				return None, None

	def robot_for_key(self, key):
		for robot in self.pos_start:
			if self.routes[robot][key]["steps"] is not None:
				return robot

	def calc_routes(self):
		for robot in self.pos_start:
			self.routes[robot] = {}

		# first map all starting positions <-> all keys
		for source_key in self.keys:
			if source_key not in self.routes:
				self.routes[source_key] = {}

			for robot in self.pos_start:
				# first map all connection from our position (entrance / starting point)
				# (we don't need to add the reverse path here)
				source = self.keys[source_key].copy()
				steps, blocking = self.find_path2(self.pos_start[robot], source)

				#print("%s%s <=> %s%s: %s steps, blocking=%s" % (robot, state["pos"], source_key, source, steps, blocking))
				self.routes[robot][source_key] = { "steps": steps, "blocking": blocking, "robot": robot}

				#print(pprint.pprint(self.routes))

		# then map all keys to all keys
		for source_key in self.keys:
			print("calculating all routes from source=%s ..." % (source_key))

			# then do the same for all other keys
			for dest_key in self.keys:
				if source_key in self.routes and dest_key in self.routes[source_key]:
					# route already known
					#print("%s%s already known: %s" % (source_key, dest_key, self.routes[source_key][dest_key]))
					continue

				source = self.keys[source_key].copy()
				dest = self.keys[dest_key].copy()

				if source == dest:
					continue

				steps, blocking = self.find_path2(source, dest)

				# part2: it's possible that there is no connection between two places. in that case, fp2()
				# returns None. let's keep that, for our records.
				if steps is None:
					blocking_reverse = None
					robot = None
				else:
					blocking_reverse = list(reversed(blocking))
					robot = self.robot_for_key(dest_key)

				#print("%s%s <=> %s%s: %s steps, blocking=%s" % (source_key, source, dest_key, dest, steps, blocking))

				if dest_key not in self.routes:
					# to make sure we can store the reverse path
					self.routes[dest_key] = {}

				self.routes[source_key][dest_key] = { "steps": steps, "robot": robot, "blocking": blocking }
				self.routes[dest_key][source_key] = { "steps": steps, "robot": robot, "blocking": blocking_reverse }

	def find_available_keys(self, currpos, keys_so_far):
		out = []

		for robot in self.pos_start:
			# return all keys that are
			# 1) not blocked
			# 2) reachable for this robot
			# 3) not already collected

			from_key = currpos[robot]
			for dest_key in self.routes[from_key]:
				if dest_key in keys_so_far:
					continue

				if self.routes[from_key][dest_key]["steps"] is None:
					continue

				blockers = [b for b in self.routes[from_key][dest_key]["blocking"]
					if b.lower() not in keys_so_far]

				if len(blockers) == 0:
					#print("avail key: from=%s dest=%s robot=%s" %
					#	(from_key, dest_key, robot))
					out += [dest_key]

		return out

	def find_shortest_wrapper(self):
		currpos = {}
		for robot in self.pos_start:
			currpos[robot] = robot

		return self.find_shortest(currpos = copy.deepcopy(currpos))

	def find_shortest(self, currpos, keys_so_far = "", depth = 0):
		indent = "   " * depth

		potential_dest_keys = self.find_available_keys(currpos, keys_so_far = keys_so_far)

		if len(keys_so_far) == len(self.keys):
			#print(indent + "final: %s" % (keys_so_far))
			return 0, ""

		allpos = [currpos[r] for r in currpos]
		cache_id = "%s_%s" % ("".join(sorted(keys_so_far)), "".join(sorted(allpos)))

		if cache_id in self.route_cache:
			#print(indent + "cache hit: %s %s" %
			#	(self.route_cache[cache_id]["steps"], self.route_cache[cache_id]["route"]))
			return self.route_cache[cache_id]["steps"], self.route_cache[cache_id]["route"]

		mins = 999999999
		minr = None
		for dest_key in potential_dest_keys:
			newpos = copy.deepcopy(currpos)
			robot = self.robot_for_key(dest_key)
			newpos[robot] = dest_key

			#print(indent + "fs(%d) dest_key=%s, robot=%s newposrobot=%s ksf=%s" %
			#	(depth, dest_key, robot, newpos[robot], keys_so_far))

			s, r = self.find_shortest(currpos = newpos,
				keys_so_far = keys_so_far + dest_key,
				depth = depth + 1)

			steps = self.routes[currpos[robot]][dest_key]["steps"]
			steps += s
			route = dest_key + r
 
			#print(indent + "candidate: allcurrpos=%s dest=%s steps=%s + s=%s" %
			#	(allpos, dest_key, self.routes[currpos[robot]][dest_key]["steps"], s))

			if steps < mins:
				mins = steps
				minr = route

		self.route_cache[cache_id] = {}
		self.route_cache[cache_id]["steps"] = mins
		self.route_cache[cache_id]["route"] = minr
		#print(indent + "CACHE MISS: %s %s" % (mins, minr))

		return mins, minr

tunnel = Tunnel(inputstring)

print("map with width=%d height=%d" % (tunnel.width, tunnel.height))

tunnel.calc_routes()
#pprint.pprint(tunnel.routes)

s, r = tunnel.find_shortest_wrapper()
print(s, r)

