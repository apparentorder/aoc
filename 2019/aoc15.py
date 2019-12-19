#!/usr/bin/env python

import sys
from os import system
from time import sleep

f = open("aoc15in")
program_string = f.read()
f.close()

debug_enabled = False
#debug_enabled = True

delay = 0.01

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
		self.program += [0] * 1000 # memory has to be larger than program
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

	def clear(self):
		sys.stdout.write("\033[2J") #doesn't seem to catch everything?

	def draw(self):
		global delay

		sys.stdout.write("\033[0;0H")
		for y in range(len(self.grid[0])):
			for x in range(len(self.grid)):
				sys.stdout.write(str(self.grid[x][y]) + '')

			sys.stdout.write("\n")

		sleep(delay)

class Map:
	def __init__(self, width, height):
		self.mapdata = [[MapField() for _ in range(height)] for _ in range(width)]

	def set_wall(self, coord):
		self.mapdata[coord.x][coord.y].is_wall = True

	def set_deadend(self, coord):
		self.mapdata[coord.x][coord.y].is_deadend = True

	def set_fork(self, coord):
		self.mapdata[coord.x][coord.y].is_fork = True

	def set_explored(self, coord):
		self.mapdata[coord.x][coord.y].is_explored = True

	def oxygen_time(self, coord, t):
		self.mapdata[coord.x][coord.y].oxygen_time = t

	def unset_fork(self, coord):
		self.mapdata[coord.x][coord.y].is_fork = False

	def get(self, coord):
		return self.mapdata[coord.x][coord.y]

	def visited(self, coord):
		self.mapdata[coord.x][coord.y].visits += 1

class MapField:
	def __init__(self):
		self.visits = 0
		self.is_wall = False
		self.is_deadend = False
		self.is_fork = False
		self.is_explored = False
		self.oxygen_time = None

class Droid:
	def __init__(self, ic, width, height):
		self.pos = Coordinates(width/2, height/2)
		self.pos_prev = Coordinates(width/2, height/2)
		self.pos_start = Coordinates(width/2, height/2)
		self.oxygen = None
		self.screen = Screen(width, height)
		self.map = Map(width, height)
		self.width = width
		self.height = height
		self.intcodecomputer = ic
		self.backtracking = False
		self.steps = 0

		self.map.visited(self.pos)
		self.screen.clear()
		self.draw()

	def draw(self):
		for y in range(len(self.screen.grid[0])):
			for x in range(len(self.screen.grid)):
				c = ' '
				if self.map.mapdata[x][y].is_wall:
					c = '#'
				elif self.map.mapdata[x][y].oxygen_time is not None:
					# note that oxy takes precedence over almost everything
					c = 'o'
				elif self.map.mapdata[x][y].is_deadend:
					c = '='
				elif self.map.mapdata[x][y].is_fork:
					c = '?'
				elif self.map.mapdata[x][y].visits > 0:
					c = '.'
				self.screen.grid[x][y] = c

		self.screen.grid[self.pos_start.x][self.pos_start.y] = 'X'
		self.screen.grid[self.pos.x][self.pos.y] = 'D'

		if self.oxygen is not None:
			self.screen.grid[self.oxygen.x][self.oxygen.y] = 'O'

		self.screen.draw()

	def _pos_to_direction(self, pos_from, pos_to):
		if pos_from.x == pos_to.x:
			if pos_to.y == pos_from.y - 1:
				# from south to north
				return 1
			if pos_to.y == pos_from.y + 1:
				# from north to south
				return 2
			raise ValueError("invalid from/to position %s/%s" % (pos_from, pos_to))
		elif pos_from.y == pos_to.y:
			if pos_to.x == pos_from.x - 1:
				# from east to west
				return 3
			if pos_to.x == pos_from.x + 1:
				# from west to east
				return 4
			raise ValueError("invalid from/to position %s/%s" % (pos_from, pos_to))
		else:
			raise ValueError("invalid from/to, both axis differ")

	def move(self, newpos):
		if self.pos == newpos:
			return None

		dir = self._pos_to_direction(self.pos, newpos)
		output = self.intcodecomputer.run(dir)

		if output == 0:
			self.map.set_wall(newpos)
			return 0

		if output == 2:
			self.oxygen = newpos.copy()

		# if we're here, output must be [1, 2],
		# so in both cases we have moved

		self.pos_prev = self.pos.copy()
		self.pos = newpos.copy()

		# mark NEW position as visited
		self.map.visited(self.pos)

		# mark OLD position as deadend if we're backtracking
		if self.backtracking:
			self.map.set_deadend(self.pos_prev)

		self.draw()

		return output

	def surroundings(self, coord):
		ret = []
		ret.append(Coordinates(coord.x, coord.y - 1))
		ret.append(Coordinates(coord.x, coord.y + 1))
		ret.append(Coordinates(coord.x - 1, coord.y))
		ret.append(Coordinates(coord.x + 1, coord.y))

		return ret

	def explore_field(self):
		# make sure to try each option first, to
		# populate our map data and to know where
		# we have alternative ways and where we're
		# walled anyway

		if self.map.get(self.pos).is_explored:
			return

		unvisited = 0

		for coord in self.surroundings(self.pos):
			field = self.map.get(coord)
			if field.is_wall:
				continue
			if field.visits == 0 and unvisited == 0:
				# having ONE unvisited field is fine,
				# as we need to go there anyway
				unvisited += 1
			if field.visits == 0 and unvisited > 0:
				# need to explore that!
				self.move(coord)
				if self.pos == coord:
					# move back
					self.move(self.pos_prev)

		self.map.set_explored(self.pos)

	def _nextpos_least_visited(self):
		least_visits = 999
		least_visits_direction = None
		for coord in self.surroundings(self.pos):
			field = self.map.get(coord)
			if field.is_wall:
				continue

			if field.is_deadend:
				continue

			if field.visits < least_visits:
				least_visits = field.visits
				least_visits_pos = coord

		return least_visits_pos

	def nextpos(self):
		# assumption: when we get called, this
		# field is fully explored

		candidates = self.surroundings(self.pos)
		options = 4
		for coord in candidates:
			f = self.map.get(coord)
			if f.is_wall or f.is_deadend:
				options -= 1

		if options >= 3:
			self.map.set_fork(self.pos)

		if options == 2:
			self.map.unset_fork(self.pos)

		if options >= 2:
			if self.backtracking:
				self.backtracking = False

		if options == 1:
			if self.steps > 0 and not self.backtracking:
				self.backtracking = True

		if options == 0:
			return None

		if self.backtracking:
			self.steps -= 1
		else:
			self.steps += 1

		return self._nextpos_least_visited()

ic = IntcodeComputer(program_string, [])
droid = Droid(ic, 50, 50)

# moves:
# 1 north
# 2 south
# 3 west
# 4 east

delay = 0.05
while True:
	droid.explore_field()
	nextpos = droid.nextpos()
	if nextpos is None:
		print("out of options. end!")
		break

	print("nextpos: %s" % (nextpos))
	print("steps: %d" % (droid.steps))
	print("backtracking: %s" % (droid.backtracking))
	if droid.move(nextpos) == 2:
		print("*** OXY FOUND AT %s AFTER %d STEPS ***" % (droid.oxygen, droid.steps))

print("")
print("")
print("")
print("")
print("// --- // now expanding oxygen")

# got map, now simulate air expansion (part 2)
# our i loop serves as a minutes timer
droid.map.oxygen_time(droid.oxygen, 0)

delay = 0.1

i = 0
ptr = Coordinates(0, 0)
while True:
	# 1) scan map for oxygen with time == (i - 1)
	#    (don't catch oxygen that just was created
	#    in *this* iteration)
	# 2) check surroundings, oxygenize every field that
	#    is not a wall (droids we don't care about)

	i += 1

	new_oxy = 0
	for x in range(droid.width):
		for y in range(droid.height):
			ptr.update(x, y)
			f = droid.map.get(ptr)

			if f.oxygen_time == i - 1:
				for surr in droid.surroundings(ptr):
					fsurr = droid.map.get(surr)
					if not fsurr.is_wall and fsurr.oxygen_time is None:
						droid.map.oxygen_time(surr, i)
						new_oxy += 1

	if new_oxy == 0:
		# n.b. we'll have had one extra minute to figure out that
		# no further expansion is happening
		print("no further oxygen expansion after %d minutes" % (i - 1))
		break

	droid.draw()

