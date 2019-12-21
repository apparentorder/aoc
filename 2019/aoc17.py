#!/usr/bin/env python

import re
import sys
from os import system
from time import sleep

f = open("aoc17in")
program_string = f.read()
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

class IntcodeComputer:
	def __init__(self, program_string, initial_input):
		self.program = list(map(int, program_string.split(',')))
		self.program += [0] * 10000 # memory has to be larger than program
		self.input = initial_input
		self.output = None
		self.position = 0
		self.halted = False
		self.position_relative_base = 0
		self.opcount = 0

	def printinstruction(self, op, count):
		x = []

		for i in range(1, count + 1):
			x.append(str(self.program[self.position + i]))

		ops = " ".join(x)
		debug("position %d op %s %s" % (self.position, op, ops))

	def getpos(self, op, argnum):
		argval  = self.program[self.position + argnum]
		argmode = int(op[3 - argnum])

		if argmode == 0:
			# positional: return argument's value
			debug("... arg %d: positional: targetpos=%d" % (argnum, argval))
			return argval
		elif argmode == 1:
			# immediate: return *this* position (this argument)
			debug("... arg %d: immediate: targetpos=%d" % (argnum, self.position + argnum))
			return self.position + argnum
		elif argmode == 2:
			# relative positional: return pos. base + argument value
			relpos = self.position_relative_base + argval
			debug("... arg %d: relative to base %d: targetpos=%d"
				% (argnum, self.position_relative_base, relpos))
			return relpos
		else:
			print("panic: unknown argument mode in op=%s" % op)
			exit(1)

	def getval(self, op, argnum):
		p = self.getpos(op, argnum)
		return self.program[p]

	def run_op(self, op):
		# returns False if execution loop should not continue

		self.opcount += 1

		opcode = int(op[3:5])

		if opcode == 99:
			self.printinstruction(op, 0)
			self.halted = True
			debug("halted!")
			return False

		if opcode == 1: #add
			self.printinstruction(op, 3)
			arg1 = self.getval(op, 1)
			arg2 = self.getval(op, 2)
			dest = self.getpos(op, 3)
			debug("position %d: add %d + %d" % (self.position, arg1, arg2))
			self.program[dest] = arg1 + arg2
			self.position += 4

		elif opcode == 2: #multiply
			self.printinstruction(op, 3)
			arg1 = self.getval(op, 1)
			arg2 = self.getval(op, 2)
			dest = self.getpos(op, 3)
			debug("position %d: multiply %d * %d" % (self.position, arg1, arg2))
			self.program[dest] = arg1 * arg2
			self.position += 4

		elif opcode == 3: #store input
			self.printinstruction(op, 1)
			dest = self.getpos(op, 1)
			if len(self.input) == 0:
				# give the user a chance to provide new input
				return False
			value = self.input.pop(0)
			debug("position %d: store input %s" % (self.position, value))
			self.program[dest] = value
			self.position += 2

		elif opcode == 4: #get value
			self.printinstruction(op, 1)
			arg1 = self.getval(op, 1)
			self.output = arg1
			debug("position %d: get value %d" % (self.position, self.output))
			debug("OUTPUT: %d" % self.output)
			self.position += 2
			return False

		elif opcode == 5: # jump-if-true
			self.printinstruction(op, 2)
			arg1 = self.getval(op, 1)
			arg2 = self.getval(op, 2)
			debug("position %d: jump-if-true %d" % (self.position, arg1))
			if arg1 <> 0:
				self.position = arg2
			else:
				self.position += 3

		elif opcode == 6: # jump-if-false
			self.printinstruction(op, 2)
			arg1 = self.getval(op, 1)
			arg2 = self.getval(op, 2)
			debug("position %d: jump-if-false %d" % (self.position, arg1))
			if arg1 == 0:
				self.position = arg2
			else:
				self.position += 3

		elif opcode == 7: # less than
			self.printinstruction(op, 3)
			arg1 = self.getval(op, 1)
			arg2 = self.getval(op, 2)
			dest = self.getpos(op, 3)
			debug("position %d: %d < %d" % (self.position, arg1, arg2))
			if arg1 < arg2:
				self.program[dest] = 1
			else:
				self.program[dest] = 0

			self.position += 4

		elif opcode == 8: # equals
			self.printinstruction(op, 3)
			arg1 = self.getval(op, 1)
			arg2 = self.getval(op, 2)
			dest = self.getpos(op, 3)
			debug("position %d: %d == %d" % (self.position, arg1, arg2))
			if arg1 == arg2:
				self.program[dest] = 1
			else:
				self.program[dest] = 0

			self.position += 4

		elif opcode == 9: # adjust relative base
			self.printinstruction(op, 1)
			arg1 = self.getval(op, 1)
			debug("position %d: adjust relative base by %d" % (self.position, arg1))
			self.position_relative_base += arg1

			self.position += 2

		else:
			print("invalid opcode %d at position %d" % (self.program[self.position], self.position))
			exit(0)

		debug

		return True

	def run(self, input_add = 0):
		debug("total memory: %d ints" % len(self.program))
		#for i in range(0, len(self.program)):
		#	print("%03d = %d" % (i, self.program[i]))

		self.output = None
		self.input.append(input_add)

		if self.halted:
			print("CANNOT RUN, ALREADY HALTED")
			exit(1)

		while True:
			if self.position >= len(self.program):
				print("PROGRAM NOT HALTED BUT REACHED END OF INPUT")
				exit(1)

			op = "%05d" % int(self.program[self.position])
			can_continue = self.run_op(op)
			if not can_continue:
				break

		return self.output

class Screen:
	def __init__(self, width, height):
		self.grid = [[" " for _ in range(height)] for _ in range(width)]
		self.double = False

	def clear(self):
		sys.stdout.write("\033[2J") #doesn't seem to catch everything?

	def draw(self):
		global delay

		extra = ""
		if self.double:
			extra = " "

		sys.stdout.write("\033[0;0H")
		sys.stdout.write(' ' + extra)
		for x in range(len(self.grid)):
			if x % 10 == 0:
				sys.stdout.write('0' + extra)
			else:
				sys.stdout.write(' ' + extra)
		sys.stdout.write('\n')

		for y in range(len(self.grid[0])):
			if y % 10 == 0:
				sys.stdout.write('0' + extra)
			else:
				sys.stdout.write(' ' + extra)

			for x in range(len(self.grid)):
				sys.stdout.write(str(self.grid[x][y]) + extra)

			sys.stdout.write("\n")

		sleep(delay)

class Map:
	def __init__(self, width, height):
		self.mapdata = [[MapField() for _ in range(height)] for _ in range(width)]

	def set_space(self, coord):
		self.mapdata[coord.x][coord.y].is_space = True

	def set_deadend(self, coord):
		self.mapdata[coord.x][coord.y].is_deadend = True

	def set_intersection(self, coord):
		self.mapdata[coord.x][coord.y].is_intersection = True

	def unset_intersection(self, coord):
		self.mapdata[coord.x][coord.y].is_intersection = False

	def get(self, coord):
		return self.mapdata[coord.x][coord.y]

	def visited(self, coord):
		self.mapdata[coord.x][coord.y].visits += 1

class MapField:
	def __init__(self):
		self.visits = 0
		self.is_space = False
		self.is_deadend = False
		self.is_intersection = False

class Vacuum:
	def __init__(self, ic, width, height):
		self.pos = Coordinates(width/2, height/2)
		self.direction = None #ascii art char [^v<>]
		self.dircodes = ['^', 'v', '<', '>']
		self.pos_prev = Coordinates(width/2, height/2)
		self.pos_start = Coordinates(width/2, height/2)
		self.screen = Screen(width, height)
		self.map = Map(width, height)
		self.ic = ic
		self.width = width
		self.height = height
		self.backtracking = False
		self.steps = 0
		self.scaffolding_count = 0

		self.map.visited(self.pos)
		#self.screen.clear()
		#self.draw()

	def draw(self):
		for y in range(len(self.screen.grid[0])):
			for x in range(len(self.screen.grid)):
				c = '#'
				if self.map.mapdata[x][y].is_space:
					c = '.'
				elif self.map.mapdata[x][y].is_intersection:
					c = 'O'
				elif self.map.mapdata[x][y].is_deadend:
					c = '='
				#elif self.map.mapdata[x][y].visits > 0:
				#	c = '.'

				self.screen.grid[x][y] = c

		self.screen.grid[self.pos.x][self.pos.y] = self.direction

		self.screen.draw()

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

	def retrieve_map(self):
		pos = Coordinates(0, 0)
		while True:
			char = ic.run()

			if ic.halted:
				break

			if char is None:
				raise Exception("no output, but still running?!")

			char = chr(char)

			if char == '#':
				# movable space
				pass

			if char == '.':
				vacuum.map.set_space(pos)

			if char in ['^', 'v', '<', '>']:
				vacuum.pos = pos.copy()
				vacuum.direction = char

			if char == 'X':
				raise Exception("Vacuum has drifted into space :(")

			if char == "\n":
				pos.update(0, pos.y + 1)
			else:
				pos.update(pos.x + 1, pos.y)


		for x in range(self.width):
			for y in range(self.height):
				if not self.map.mapdata[x][y].is_space:
					self.scaffolding_count += 1

	def mark_intersections(self):
		alignment = 0
		for x in range(1, self.width - 1):
			for y in range(1, self.height - 1):
				pos = Coordinates(x, y)
				if self.map.get(pos).is_space:
					continue

				space = 0
				for neighbor in self.surroundings(pos):
					if self.map.get(neighbor).is_space:
						space += 1
						break

				if space > 0:
					continue

				# all non-space here, so scaffold intersection
				self.map.set_intersection(pos)
				alignment += pos.x * pos.y

		return alignment

		# returns [0=up 1=down 2=left 3=right] field

	def _dir_reverse(self, direction):
		if direction == 0:
			return 1
		elif direction == 1:
			return 0
		elif direction == 2:
			return 3
		else:
			return 2

	def _dir_right(self, direction):
		if direction == 0:
			return 3
		elif direction == 1:
			return 2
		elif direction == 2:
			return 0
		else:
			return 1

	def _dir_left(self, direction):
		return self._dir_reverse(self._dir_right(direction))

	def moveforward(self, direction):
		if direction == 0:
			self.pos.update(self.pos.x, self.pos.y - 1)
		elif direction == 1:
			self.pos.update(self.pos.x, self.pos.y + 1)
		elif direction == 2:
			self.pos.update(self.pos.x - 1, self.pos.y)
		else:
			self.pos.update(self.pos.x + 1, self.pos.y)

		self.map.visited(self.pos)

	def find_path_easy(self, draw = False):
		path = []
		steps_same_direction = 0

		while True:
			direction = self.dircodes.index(self.direction)
			direction_reverse = self._dir_reverse(direction)

			#print("pos=%s dir=%s path=%s" % (self.pos, direction, path))
			if draw:
				self.draw()

			options = self.surroundings(self.pos)
			options[direction_reverse] = None # no going backwards!

			if options[direction] is not None:
				if not self.map.get(options[direction]).is_space:
					#print("dir=%s direction=%d pos=%s candidatepos=%s" %
					#	(self.direction, direction, self.pos, options[direction]))
					# continue on path
					steps_same_direction += 1
					self.moveforward(direction)
					continue

			# so turn either right or left; emit number of steps taken so far,
			# then try right
			if steps_same_direction > 0:
				path += [str(steps_same_direction)]
				steps_same_direction = 0

			right = self._dir_right(direction)
			if options[right] is not None and not self.map.get(options[right]).is_space:
				self.direction = self.dircodes[right]
				path += ["R"]
				continue

			left = self._dir_left(direction)
			if options[left] is not None and not self.map.get(options[left]).is_space:
				self.direction = self.dircodes[left]
				path += ["L"]
				continue

			# if we're here, then we're out of options, ergo finished
			return path

	def find_all_paths(self, path_so_far = [], steps_same_direction_so_far = 0, force_next_direction = None, depth = 0, intersections_seen = [], scaffolds_seen = []):
		path = list(path_so_far)
		steps_same_direction = steps_same_direction_so_far

		#print("fapr, depth = %d, path = %s" % (depth, path))

		if depth > 50:
			# probably looping like an idiot.
			#print("aborting depth=%d pathlen=%d" % (depth, len(path)))
			return

		# assumption: we get called when the robot first moves, or when we have
		# *arrived* at an intersection, ergo we don't need to check for that.
		# we continue moving until we hit an intersection (or the very end).
		while True:
			if len(path) > 80:
				#print("aborting depth=%d pathlen=%d" % (depth, len(path)))
				return

			direction = self.dircodes.index(self.direction)
			direction_reverse = self._dir_reverse(direction)

			options = self.surroundings(self.pos)
			options[direction_reverse] = None # no going backwards!

			#self.draw()

			if force_next_direction is None:
				f = self.map.get(self.pos)
				if f.is_intersection:
					if intersections_seen.count(self.pos) < 2:
						break
			else:
				if force_next_direction == direction:
					force_next_direction = None
				else:
					# make sure that the force-direction is the only one
					# that seems to be available
					for i in range(len(self.dircodes)):
						if i != force_next_direction:
							options[i] = None

			if options[direction] is not None:
				if not self.map.get(options[direction]).is_space:
					# continue on path
					steps_same_direction += 1
					scaffolds_seen += [str(self.pos)]
					self.moveforward(direction)
					continue

			# so turn either right or left; emit number of steps taken so far,
			# then try right
			if steps_same_direction > 0:
				path += [str(steps_same_direction)]
				steps_same_direction = 0

			right = self._dir_right(direction)
			if options[right] is not None and not self.map.get(options[right]).is_space:
				self.direction = self.dircodes[right]
				path += ["R"]
				continue

			left = self._dir_left(direction)
			if options[left] is not None and not self.map.get(options[left]).is_space:
				self.direction = self.dircodes[left]
				path += ["L"]
				continue

			# if we're here, then we're out of options, ergo finished
			if len(set(scaffolds_seen)) == self.scaffolding_count - 1:
				#print("have path! depth=%d pathlen=%d scaffolds=%d path=%s" % (depth, len(path), len(set(scaffolds_seen)), "".join(path)))
				yield path

			return

		#print("have intersection!")
		#self.map.visited(self.pos)

		# if we're here, we've moved to an intersection. try all the paths!
		# (this takes about 2 hours on a moderate machine.)
		# move forward by 1 on each direction, then call ourself
		for try_direction in [direction, self._dir_right(direction), self._dir_left(direction)]:
			# save state
			xpos = self.pos.copy()
			xdir = self.direction

			# recurse
			for x in self.find_all_paths(path,
				steps_same_direction,
				try_direction,
				depth = depth + 1,
				intersections_seen = list(intersections_seen + [self.pos.copy()]),
				scaffolds_seen = list(scaffolds_seen)):
				yield x

			# restore state
			self.pos = xpos.copy()
			self.direction = xdir

def tokenize(path_str, maxlen):
	minlen = min(maxlen, len(path_str) / 2 + 1)
	out = [path_str]
	while minlen >= 2:
		out_try = out
		for path_try in out_try:
			if path_try.startswith('token_'):
				continue

			for startpos in range(len(path_try)):
				if len(path_try) < startpos + minlen:
					continue
				match_try = path_try[startpos:startpos+minlen]
				if (len(match_try) < minlen):
					continue
				matchcount = 0
				for path_try_match in out_try:
					if path_try_match.startswith('token_'):
						continue
					if len(path_try_match) < minlen:
						continue
					matches = path_try_match.split(match_try)
					#print("%s in %s => %d matches" % (match_try, path_try_match, len(matches)))
					if len(matches) >= 2:
						matchcount += 1
					if (matchcount >= 1 and len(matches) >= 2):
						matchcount += 1
						#print("MATCH!")
						index = out.index(path_try_match)
						out.pop(index)
						i = 0
						for m in matches:
							if m != '':
								out.insert(index + i, m)
								i += 1
							out.insert(index + i, "token_%s" % (match_try))
							i += 1
						out.pop(index + i - 1)

		minlen -= 1

	return out

def tokenize3(str, maxlen, tokens = None, depth = 0):
	if tokens is None:
		tokens = {
			'A': None,
			'B': None,
			'C': None,
		}

	indent = "   " * depth

	parts = re.findall('[^ABC]+', str)

	for p in parts:
		if len(p) < 2:
			# can't tokenize any further
			#print(indent + "len(p) < 2, for p=%s" % (p))
			return

	# figure out which slot to use next
	slot = None
	for x in ['A', 'B', 'C']:
		if tokens[x] is None:
			slot = x
			break

	if slot is None:
		# no free slots, go home.
		#print(indent + "all slots used up.")
		return

	for chunklen in range(maxlen, 2-1, -1):
		str_this = str
		if len(parts[0]) < chunklen:
			# remaining part is shorter than
			# what we're looking for -> can't resolve this
			#print(indent + "len(parts0) < chunklen, for p=%s chunklen=%d" % (parts[0], chunklen))
			continue

		chunk = parts[0][0:chunklen]
		tokens[slot] = chunk
		#print(indent + "t2 depth=%d chunklen=%d chunk=%s str=%s tokens=%s" % (depth, chunklen, chunk, str_this, tokens))

		str_this = str_this.replace(chunk, slot)

		if len(re.findall('[^ABC]+', str_this)) == 0 and len(str_this) <= maxlen:
			#print("depth=%d str=%s tokens=%s" % (depth, str_this, tokens))
			yield str_this, tokens
			continue

		for x in tokenize3(str_this, maxlen, tokens = dict(tokens), depth = depth + 1):
			yield x

def mutate_path(path, min_replace = None):
	# try variations, e.g. replacing '12' with '6 6' and so on.
	replacements = {
		4: [2, 2],
		6: [2, 4],
		6: [4, 2],
		8: [2, 6],
		8: [4, 4],
		8: [6, 2],
		10: [2, 8],
		10: [4, 6],
		10: [6, 4],
		10: [8, 2],
		12: [2, 10],
		12: [4, 8],
		12: [6, 6],
		12: [8, 4],
		12: [10, 2],
	}

	if min_replace is None:
		min_replace = min(sorted(replacements))

	#print("mp with min_replace=%d" % (min_replace))
	for replace in sorted(replacements):
		path_try = path
		for i in range(len(path_try) - 1, -1, -1):
			if path_try[i] == str(replace) and replace > min_replace:
				path_try.pop(i)
				for r in replacements[replace]:
					path_try.insert(i, str(r))
				for m in mutate_path(path_try, replace):
					yield m

		yield path_try

def str_to_vacuum(string):
	# return e.g. 'ABCCA' or 'R8L4R12' as list of
	# ASCII codes, separated by comma,
	# ended with 10 (newline)
	# (tokens are either single letters or
	# (possibly multi-digit) numbers)

	out = []
	string = re.sub('([A-Z]|[0-9]+)', ',\\1', string)
	string = re.sub('^,', '', string)

	for s in string:
		out += [ord(s)]

	out += [ord("\n")]

	print("str2vac string=%s out=%s" % (string, out))
	return out

ic = IntcodeComputer(program_string, [])
vacuum = Vacuum(ic, 77, 41)
vacuum.retrieve_map()
print("scaffolds = %d" % (vacuum.scaffolding_count))
alignment = vacuum.mark_intersections()
vacuum.screen.double = True
#vacuum.draw()
print("alignment value %s" % (alignment))

path = vacuum.find_path_easy()
path = "".join(path)
for (mainprogram, functions) in tokenize3(path, 11):
	print("trying program=%s with functions=%s" % (mainprogram, functions))

	input = []
	input += str_to_vacuum(mainprogram)
	input += str_to_vacuum(functions['A'])
	input += str_to_vacuum(functions['B'])
	input += str_to_vacuum(functions['C'])
	input += [ord('n'), ord("\n")]

	print(input)

	# reboot the IC, wake the robot
	ic = IntcodeComputer(program_string, input)
	ic.program[0] = 2

	# loop to digest & ignore initial screen output
	output = None
	while True:
		x = ic.run()

		if x is not None:
			output = x

		if ic.halted:
			break

	print("=> dust: %d" % (output))

