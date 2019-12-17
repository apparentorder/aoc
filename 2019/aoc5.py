#!/usr/bin/env python

program_string = '3,225,1,225,6,6,1100,1,238,225,104,0,1102,35,92,225,1101,25,55,225,1102,47,36,225,1102,17,35,225,1,165,18,224,1001,224,-106,224,4,224,102,8,223,223,1001,224,3,224,1,223,224,223,1101,68,23,224,101,-91,224,224,4,224,102,8,223,223,101,1,224,224,1,223,224,223,2,217,13,224,1001,224,-1890,224,4,224,102,8,223,223,1001,224,6,224,1,224,223,223,1102,69,77,224,1001,224,-5313,224,4,224,1002,223,8,223,101,2,224,224,1,224,223,223,102,50,22,224,101,-1800,224,224,4,224,1002,223,8,223,1001,224,5,224,1,224,223,223,1102,89,32,225,1001,26,60,224,1001,224,-95,224,4,224,102,8,223,223,101,2,224,224,1,223,224,223,1102,51,79,225,1102,65,30,225,1002,170,86,224,101,-2580,224,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,101,39,139,224,1001,224,-128,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,54,93,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,677,224,1002,223,2,223,1005,224,329,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,344,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,359,1001,223,1,223,7,677,226,224,1002,223,2,223,1005,224,374,1001,223,1,223,1107,677,226,224,1002,223,2,223,1005,224,389,1001,223,1,223,107,226,677,224,102,2,223,223,1005,224,404,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,419,101,1,223,223,107,226,226,224,102,2,223,223,1005,224,434,1001,223,1,223,108,677,226,224,1002,223,2,223,1006,224,449,101,1,223,223,108,226,226,224,102,2,223,223,1006,224,464,1001,223,1,223,1007,226,226,224,1002,223,2,223,1005,224,479,101,1,223,223,8,677,226,224,1002,223,2,223,1006,224,494,101,1,223,223,1007,226,677,224,102,2,223,223,1006,224,509,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,524,101,1,223,223,107,677,677,224,102,2,223,223,1005,224,539,101,1,223,223,1008,677,226,224,1002,223,2,223,1005,224,554,1001,223,1,223,1008,226,226,224,1002,223,2,223,1006,224,569,1001,223,1,223,1108,226,226,224,102,2,223,223,1005,224,584,101,1,223,223,1107,226,677,224,1002,223,2,223,1005,224,599,1001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,614,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,629,1001,223,1,223,8,226,226,224,1002,223,2,223,1005,224,644,1001,223,1,223,1107,677,677,224,1002,223,2,223,1005,224,659,1001,223,1,223,1007,677,677,224,1002,223,2,223,1005,224,674,101,1,223,223,4,223,99,226'

#program_string = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'
#program_string = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'
#program_string = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'

def printinstruction(op, program, pos, count):
	x = []

	for i in range(1, count + 1):
		x.append(str(program[pos + i]))

	ops = " ".join(x)
	print("pos %d op %s %s" % (pos, op, ops))
	
def getargs(op, program, pos, count):
	args = []

	for argnum in range(1, count + 1):
		value = program[pos + argnum]
		if op[3 - argnum] == "0":
			# positional parameter
			print("... arg %d: positional: pos %d -> value %d" % (argnum, value, program[value]))
			value = program[value]
		else:
			print("... arg %d: immediate: value %d" % (argnum, value))

		args.append(value)

	return args

def run_program(program, input):
	pos = 0
	halt = False

	# input/output buffer
	io = input

	print("total memory: %d ints" % len(program))
	for i in range(0, len(program)):
		print("%03d = %d" % (i, program[i]))

	print()

	while pos < len(program):
		op = "%05d" % int(program[pos])
		opcode = int(op[3:5])

		if opcode == 99:
			printinstruction(op, program, pos, 0)
			halt = True
			break

		if opcode == 1: #add
			printinstruction(op, program, pos, 3)
			args = getargs(op, program, pos, 2)
			print("pos %d: add %d + %d" % (pos, args[0], args[1]))
			program[program[pos + 3]] = args[0] + args[1]
			pos += 4

		elif opcode == 2: #multiply
			printinstruction(op, program, pos, 3)
			args = getargs(op, program, pos, 2)
			print("pos %d: multiply %d * %d" % (pos, args[0], args[1]))
			program[program[pos + 3]] = args[0] * args[1]
			pos += 4

		elif opcode == 3: #store input
			printinstruction(op, program, pos, 1)
			args = getargs(op, program, pos, 0)
			print("pos %d: store input %d" % (pos, io))
			program[program[pos + 1]] = io
			pos += 2

		elif opcode == 4: #get value
			printinstruction(op, program, pos, 1)
			args = getargs(op, program, pos, 1)
			io = args[0]
			print("pos %d: get value %d" % (pos, io))
			print("OUTPUT: %d" % io)
			pos += 2

		elif opcode == 5: # jump-if-true
			printinstruction(op, program, pos, 2)
			args = getargs(op, program, pos, 2)
			print("pos %d: jump-if-true %d" % (pos, args[0]))
			if args[0] <> 0:
				pos = args[1]
			else:
				pos += 3

		elif opcode == 6: # jump-if-false
			printinstruction(op, program, pos, 2)
			args = getargs(op, program, pos, 2)
			print("pos %d: jump-if-false %d" % (pos, args[0]))
			if args[0] == 0:
				pos = args[1]
			else:
				pos += 3

		elif opcode == 7: # less than
			printinstruction(op, program, pos, 3)
			args = getargs(op, program, pos, 2)
			print("pos %d: %d < %d" % (pos, args[0], args[1]))
			if args[0] < args[1]:
				program[program[pos + 3]] = 1
			else:
				program[program[pos + 3]] = 0

			pos += 4

		elif opcode == 8: # equals
			printinstruction(op, program, pos, 3)
			args = getargs(op, program, pos, 2)
			print("pos %d: %d == %d" % (pos, args[0], args[1]))
			if args[0] == args[1]:
				program[program[pos + 3]] = 1
			else:
				program[program[pos + 3]] = 0

			pos += 4

		else:
			print("invalid opcode %d at pos %d" % (program[pos], pos))
			exit(0)

		print

	if halt:
		print("halted!")
	else:
		print("PROGRAM NOT HALTED BUT REACHED END OF INPUT")

	return io

program = list(map(int, program_string.split(',')))

#run_program(program, 1) #part1
run_program(program, 5) #part2

