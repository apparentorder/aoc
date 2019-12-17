#!/usr/bin/env python

import sys
from os import system
from time import sleep

f = open("aoc13in")
program_string = f.read()
f.close()

debug_enabled = False

def debug(s):
	if debug_enabled:
		print(s)

class Screen:
	def __init__(self, width, height):
		self.grid = [[Pixel() for _ in range(height)] for _ in range(width)]

	def clear(self):
		sys.stdout.write("\033[2J") #doesn't seem to catch everything?

	def draw(self, score, blocks, delay):
		sys.stdout.write("\033[0;0H")
		for y in range(len(self.grid[0])):
			for x in range(len(self.grid)):
				sys.stdout.write(str(self.grid[x][y]) + ' ')

			sys.stdout.write("\n")

		sys.stdout.write("// SCORE: %d // BLOCKS: %d" % (score, blocks))
		sys.stdout.write("\033[K")

		sleep(delay)

class PongGame:
	def __init__(self, gamespeed = 1.0):
		self.score = 0
		self.blocks = 0
		self.game_active = False
		self.paddle = Coordinates()
		self.ball = Coordinates()
		self.screen = Screen(width = 50, height = 24)
		self.speed = gamespeed

	def updatescreen(self):
		self.screen.draw(self.score, self.blocks, self.speed)

	def update(self, x, y, arg):
		if x == -1 and y == 0:
			self.score = arg
			return

		previous_tile_id = self.screen.grid[x][y].tile_id
		self.screen.grid[x][y].tile_id = arg

		if arg != 2 and previous_tile_id == 2:
			# removed a block!
			self.blocks -= 1

		if arg == 2: #block
			self.blocks += 1
		elif arg == 3: #paddle
			self.paddle.update(x, y)
			self.updatescreen()
		elif arg == 4: #ball
			self.ball.update(x, y)
			self.updatescreen()

class Coordinates:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

	def update(self, x, y):
		self.__init__(x, y)

	def __str__(self):
		return "(%d,%d)" % (self.x, self.y)

	def iszero(self):
		return (self.x == 0 and self.y == 0)

	def __eq__(self, other):
		return (self.x == other.x) and (self.y == other.y)

class Pixel:
	tile = {}
	tile[0] = " " #empty
	tile[1] = "#" #wall
	tile[2] = "*" #block
	tile[3] = "=" #horiz. paddle
	tile[4] = "@" #ball

	def __init__(self, tile_id = 0):
		self.tile_id = tile_id

	def __str__(self):
		return Pixel.tile[self.tile_id]

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

	def run(self):
		debug("total memory: %d ints" % len(self.program))
		#for i in range(0, len(self.program)):
		#	print("%03d = %d" % (i, self.program[i]))

		self.output = None

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

ic = IntcodeComputer(program_string, [])
game = PongGame(0.005)

# for part 2
ic.program[0] = 2

# note: the halt instruction will happen when
# we run the ic to get the first output value
# (i.e. "while not halted" will not work properly)
while True:
	x = ic.run()

	if ic.halted:
		break

	if x != None:
		# computer gave us output, expect two more
		# (update score, draw screen, ...)
		y = ic.run()
		tile_id = ic.run()
		game.update(x, y, tile_id)
	else:
		# no output, so we're here because input ran dry.
		# let's see where we need to move the paddle.
		joystick = 0

		if game.ball.x > game.paddle.x:
			joystick = 1 #right
		elif game.ball.x < game.paddle.x:
			joystick = -1 #left

		ic.input.append(joystick)

print("done, halted=%s score=%d" % (ic.halted, game.score))

