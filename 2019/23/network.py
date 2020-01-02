#!/usr/bin/env python

import re
import sys
from time import sleep

f = open("input")
program_string = f.read()
f.close()

debug_enabled = False

delay = 0

def debug(s):
	if debug_enabled:
		print(s)

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
		self.use_stdio = False

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

	def convert_from_ascii(self, inputstring):
		for c in inputstring:
			yield ord(c)

	def convert_to_ascii(self, intnum):
		if intnum > 255:
			# assume this was meant to be "a single giant integer
			# outside the normal ASCII range", as it says on day 21.
			return str(intnum) + "\n"
		else:
			return chr(intnum)

	def input_from_stdin(self):
		line = None
		while True:
			line = sys.stdin.readline()

			# weed out comments and empty lines
			if line.count("#") > 0:
				line = line.split('#')[0]

			line = line.strip()

			if len(line) > 0:
				line += "\n"
				break

		return (self.convert_from_ascii(line))

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
				if self.use_stdio:
					self.input += self.input_from_stdin()
				else:
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
			if self.use_stdio:
				sys.stdout.write(self.convert_to_ascii(self.output))
			else:
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

	def run(self, input_add = None):
		debug("total memory: %d ints" % len(self.program))
		#for i in range(0, len(self.program)):
		#	print("%03d = %d" % (i, self.program[i]))

		self.output = None
		if input_add is not None:
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

value_queue_empty = -1
computers_total = 50
computer = [None] * computers_total
nat_x = None
nat_y = None
nat_y_seen = {}
idle_count = 0

for i in range(computers_total):
	computer[i] = IntcodeComputer(program_string, initial_input = [i])

while True:
	for i in range(computers_total):
		#print("executing node %d" % (i))
		packet_dest = computer[i].run()

		if packet_dest is None:
			# returned because of no input, so synthesize some
			# input to indicate "empty queue" (we queue the input
			# but don't run the computer again)
			computer[i].input += [value_queue_empty]
			idle_count += 1

			if idle_count > computers_total*2:
				if nat_y in nat_y_seen:
					print(">>> finished: would repeat " +
						"transmission of " +
						"nat_y=%d to " % (nat_y) +
						"computer 0")
					exit(0)

				# network is idle, emit packet from NAT to
				# computer[0]
				computer[0].input += [nat_x, nat_y]
				nat_y_seen[nat_y] = True
				idle_count = 0

			continue

		# we have an output from this computer,
		# continue running until it emits the next
		# two values as well.
		packet_x = computer[i].run()
		packet_y = computer[i].run()

		# ... and place the packet on the destination's
		# input queue
		#print(">>> packet from %d to %d (x=%d, y=%d)" %
		#	(i, packet_dest, packet_x, packet_y))

		if packet_dest == 255:
			#print(">>> packet to address 255 (NAT)")

			if nat_y is None:
				print(">>> FIRST packet to address NAT (255): " +
					"x=%d y=%d" % (packet_x, packet_y))

			nat_x = packet_x
			nat_y = packet_y
		else:
			computer[packet_dest].input += [packet_x, packet_y]

		# ... also reset the idle counter, as we've seen some
		# activity now.
		idle_count = 0

