#!/usr/bin/env python

program_string_ex1 = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'
program_string_ex2 = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'
program_string_ex3 = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'
program_string_feedback_ex1 = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
program_string_feedback_ex2 = '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'

program_string_actual = '3,8,1001,8,10,8,105,1,0,0,21,46,67,76,97,118,199,280,361,442,99999,3,9,1002,9,3,9,101,4,9,9,102,3,9,9,1001,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,101,5,9,9,1002,9,2,9,101,2,9,9,4,9,99,3,9,101,4,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,1001,9,4,9,1002,9,5,9,4,9,99,3,9,102,3,9,9,1001,9,2,9,1002,9,3,9,1001,9,3,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99'

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
		self.input = initial_input
		self.output = None
		self.iptr = 0
		self.halted = False

	def printinstruction(self, op, count):
		x = []

		for i in range(1, count + 1):
			x.append(str(self.program[self.iptr + i]))

		ops = " ".join(x)
		debug("iptr %d op %s %s" % (self.iptr, op, ops))
		
	def getargs(self, op, count):
		args = []

		for argnum in range(1, count + 1):
			value = self.program[self.iptr + argnum]
			if op[3 - argnum] == "0":
				# positional parameter
				debug("... arg %d: positional: pos %d -> value %d"
					% (argnum, value, self.program[value]))
				value = self.program[value]
			else:
				debug("... arg %d: immediate: value %d" % (argnum, value))

			args.append(value)

		return args

	def run(self):
		debug("total memory: %d ints" % len(self.program))
		#for i in range(0, len(program)):
		#	print("%03d = %d" % (i, program[i]))

		while True:
			op = "%05d" % int(self.program[self.iptr])
			opcode = int(op[3:5])

			if opcode == 99:
				self.printinstruction(op, 0)
				self.halted = True
				debug("halted!")
				break

			if opcode == 1: #add
				self.printinstruction(op, 3)
				args = self.getargs(op, 2)
				debug("iptr %d: add %d + %d" % (self.iptr, args[0], args[1]))
				self.program[self.program[self.iptr + 3]] = args[0] + args[1]
				self.iptr += 4

			elif opcode == 2: #multiply
				self.printinstruction(op, 3)
				args = self.getargs(op, 2)
				debug("iptr %d: multiply %d * %d" % (self.iptr, args[0], args[1]))
				self.program[self.program[self.iptr + 3]] = args[0] * args[1]
				self.iptr += 4

			elif opcode == 3: #store input
				self.printinstruction(op, 1)
				args = self.getargs(op, 0)
				value = self.input.pop(0)
				debug("iptr %d: store input %s" % (self.iptr, value))
				self.program[self.program[self.iptr + 1]] = value
				self.iptr += 2

			elif opcode == 4: #get value
				self.printinstruction(op, 1)
				args = self.getargs(op, 1)
				self.output = args[0]
				debug("iptr %d: get value %d" % (self.iptr, self.output))
				debug("OUTPUT: %d" % self.output)
				self.iptr += 2
				break

			elif opcode == 5: # jump-if-true
				self.printinstruction(op, 2)
				args = self.getargs(op, 2)
				debug("iptr %d: jump-if-true %d" % (self.iptr, args[0]))
				if args[0] <> 0:
					self.iptr = args[1]
				else:
					self.iptr += 3

			elif opcode == 6: # jump-if-false
				self.printinstruction(op, 2)
				args = self.getargs(op, 2)
				debug("iptr %d: jump-if-false %d" % (self.iptr, args[0]))
				if args[0] == 0:
					self.iptr = args[1]
				else:
					self.iptr += 3

			elif opcode == 7: # less than
				self.printinstruction(op, 3)
				args = self.getargs(op, 2)
				debug("iptr %d: %d < %d" % (self.iptr, args[0], args[1]))
				if args[0] < args[1]:
					self.program[self.program[self.iptr + 3]] = 1
				else:
					self.program[self.program[self.iptr + 3]] = 0

				self.iptr += 4

			elif opcode == 8: # equals
				self.printinstruction(op, 3)
				args = self.getargs(op, 2)
				debug("iptr %d: %d == %d" % (self.iptr, args[0], args[1]))
				if args[0] == args[1]:
					self.program[self.program[self.iptr + 3]] = 1
				else:
					self.program[self.program[self.iptr + 3]] = 0

				self.iptr += 4

			else:
				print("invalid opcode %d at iptr %d" % (self.program[self.iptr], self.iptr))
				exit(0)

			debug

		return

		if self.iptr >= len(self.program):
			print("PROGRAM NOT HALTED BUT REACHED END OF INPUT")
			exit(1)

# part2

amp = [None] * 5
maxsignal = 0
maxsignalphase = []
for phase in PhaseSettingSequence(5, 9):
	# initialize program state for each amp
	# amp A (initial second input: 0)
	for i in range(0, 5):
		amp[i] = IntcodeComputer(program_string, list([phase[i]]))

	amp[0].input.append(0)

	# now run them
	while not amp[4].halted:
		for i in range(0, 5):
			debug(">>> amp[%d] input %s" % (i, amp[i].input))
			amp[i].run()
			# set input of next amp
			amp[(i + 1) % 5].input.append(amp[i].output)
			debug("<<< amp[%d] output %d" % (i, amp[i].output))

	print("phase %s => signal %d" % (phase, amp[4].output))

	if amp[4].output > maxsignal:
		maxsignal = amp[4].output
		maxsignalphase = phase

print("max signal %d at phase %s" % (maxsignal, maxsignalphase))

