#!/usr/bin/env python

import sys

program_string_actual = '3,8,1005,8,310,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,29,1,2,11,10,1,1101,2,10,2,1008,18,10,2,106,3,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,67,2,105,15,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,93,2,1001,16,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,119,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,141,2,7,17,10,1,1103,16,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,170,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,193,1,7,15,10,2,105,13,10,1006,0,92,1006,0,99,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,101,0,8,228,1,3,11,10,1006,0,14,1006,0,71,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,101,0,8,261,2,2,2,10,1006,0,4,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,289,101,1,9,9,1007,9,1049,10,1005,10,15,99,109,632,104,0,104,1,21101,0,387240009756,1,21101,327,0,0,1105,1,431,21101,0,387239486208,1,21102,1,338,0,1106,0,431,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,3224472579,1,1,21101,0,385,0,1106,0,431,21101,0,206253952003,1,21102,396,1,0,1105,1,431,3,10,104,0,104,0,3,10,104,0,104,0,21102,709052072296,1,1,21102,419,1,0,1105,1,431,21102,1,709051962212,1,21102,430,1,0,1106,0,431,99,109,2,21202,-1,1,1,21102,1,40,2,21102,462,1,3,21102,452,1,0,1105,1,495,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,457,458,473,4,0,1001,457,1,457,108,4,457,10,1006,10,489,1101,0,0,457,109,-2,2105,1,0,0,109,4,2102,1,-1,494,1207,-3,0,10,1006,10,512,21101,0,0,-3,22101,0,-3,1,21202,-2,1,2,21102,1,1,3,21101,531,0,0,1105,1,536,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,559,2207,-4,-2,10,1006,10,559,21202,-4,1,-4,1105,1,627,22102,1,-4,1,21201,-3,-1,2,21202,-2,2,3,21102,1,578,0,1105,1,536,21202,1,1,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,597,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,619,21201,-1,0,1,21102,1,619,0,106,0,494,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0'

program_string = program_string_actual

debug_enabled = False

def debug(s):
	if debug_enabled:
		print(s)

class PhaseSettingSequence:
	# note: this is written for py2.7. yielding from
	# recursion is easier in py3.3+:
	# yield from self.findperm(list(have), list(want))

	def __init__(self, minnum, maxnum):
		self.minnum = minnum
		self.maxnum = maxnum

	def findperm(self, have, want):
		if len(want) == 0:
			yield have

		for digit in want:
			new_have = list(have + [digit])
			new_want = list(want)
			new_want.remove(digit)
			for x in self.findperm(new_have, new_want):
				yield x

	def __iter__(self):
		have = []
		want = range(self.minnum, self.maxnum + 1)
		for x in self.findperm(list(have), list(want)):
			yield x

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

		while True:
			op = "%05d" % int(self.program[self.position])
			can_continue = self.run_op(op)
			if not can_continue:
				break

		return

		if self.position >= len(self.program):
			print("PROGRAM NOT HALTED BUT REACHED END OF INPUT")
			exit(1)

class PaintRobot:
	# direction: 0=up 1=right 2=down 3=left
	def __init__(self, posx, posy, direction = 0):
		self.x = posx
		self.y = posy
		self.direction = direction

	def turn(self, new_direction):
		# turn 0=left 1=right, then move
		adjust = new_direction
		if new_direction == 0:
			adjust = 3

		self.direction = (self.direction + adjust) % 4

# no specifics give, so maybe we'll give the robot a "spacy" 100x100 grid
# -1 = not painted (black; initial)
#  0 = black (initial)
#  1 = white
hull = [[-1 for i in range(100)] for i in range(100)]
painted_tiles = {}

bot = PaintRobot(50, 50)

# part 2: start on a white panel
hull[50][50] = 1

ic = IntcodeComputer(program_string, [])
while not ic.halted:
	# "camera" input: 0 = black panel // 1 = white panel
	input = 0
	if hull[bot.x][bot.y] == 1:
		input = 1

	ic.input.append(input)
	ic.run()
	color = ic.output

	print("pos (%d,%d): paint %d" % (bot.x, bot.y, color))

	hull[bot.x][bot.y] = color
	painted_tiles["(%d,%d)" % (bot.x, bot.y)] = 1

	if ic.halted:
		print("halt between two outputs")
		break

	ic.run()
	newdir = ic.output

	print("pos (%d,%d): turn&move %d" % (bot.x, bot.y, newdir))

	bot.turn(newdir)
	if bot.direction == 0:
		bot.y -= 1
	elif bot.direction == 1:
		bot.x += 1
	elif bot.direction == 2:
		bot.y += 1
	elif bot.direction == 3:
		bot.x -= 1

print("painted tiles count: %d" % len(painted_tiles.keys()))

for y in range(len(hull)):
	for x in range(len(hull[0])):
		c = "."
		if hull[x][y] == 1:
			c = "#"

		sys.stdout.write(c)

	sys.stdout.write("\n")

