#!/usr/bin/env python

import re
import sys
from os import system
from time import sleep

f = open("aoc19in")
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
	def __init__(self, program_string, initial_input = []):
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

	def set_beam_field(self, coord):
		self.mapdata[coord.x][coord.y].is_beam_field = True

	def get(self, coord):
		return self.mapdata[coord.x][coord.y]

	def visited(self, coord):
		self.mapdata[coord.x][coord.y].visits += 1

class MapField:
	def __init__(self):
		self.visits = 0
		self.is_beam_field = False

class TDrone:
	def __init__(self, ic_program, width, height):
		self.pos = Coordinates(width/2, height/2)
		self.screen = Screen(width, height)
		self.map = Map(width, height)
		self.ic_program = ic_program
		self.width = width
		self.height = height
		self.beam_field_count = 0

		#self.screen.clear()
		#self.draw()

	def draw(self):
		for y in range(len(self.screen.grid[0])):
			for x in range(len(self.screen.grid)):
				c = '.'
				if self.map.mapdata[x][y].is_beam_field:
					c = '#'

				self.screen.grid[x][y] = c

		self.screen.draw()

	def try_pull(self, coord):
		ic = IntcodeComputer(self.ic_program, [coord.x, coord.y])
		#ic.input += [coord.x, coord.y]
		result = ic.run()
		if result == 1:
			#print("beam at %s" % (coord))
			self.beam_field_count += 1
			self.map.set_beam_field(coord)

		return result

drone = TDrone(program_string, 1500, 1500)

# (0,0) is always active, let's set it
drone.try_pull(Coordinates(0, 0))

prev_row_beam_start = -1
for y in range(1050, drone.height):
	if y % 50 == 0:
		print("%d ..." % (y))

	this_row_beam_start = None
	for x in range(0, drone.width):
		if x <= prev_row_beam_start:
			#print("skip %s,%s" % (x, y))
			continue
		b = drone.try_pull(Coordinates(x, y))
		if b == 1 and this_row_beam_start is None:
			this_row_beam_start = x
			prev_row_beam_start = x
		if b == 0 and not this_row_beam_start is None:
			# done for this row
			#print("stop at %s,%s" % (x, y))
			break

	if this_row_beam_start is not None:
		# check for santa's bad year zeppelin
		check_x = this_row_beam_start + 99
		check_y = y - 99
		check = Coordinates(check_x, check_y)
		upper_right = drone.map.get(check)
		#print("checking %s" % (check))
		if upper_right.is_beam_field:
			upperleft = Coordinates(this_row_beam_start, check_y)
			print("winner at scanned row y=%d upperright=%s upperleft=%s" %
				(y, check, upperleft))
			print("upperleft.x * 10000 + upperleft.y = %d" %
				(upperleft.x * 10000 + upperleft.y))
			exit(0)

	if y == 1200:
		break

drone.draw()

print("beam in %d fields" % drone.beam_field_count)

