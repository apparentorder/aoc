#!/usr/bin/env python

program_string = '1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,13,19,1,10,19,23,2,9,23,27,1,6,27,31,1,10,31,35,1,35,10,39,1,9,39,43,1,6,43,47,1,10,47,51,1,6,51,55,2,13,55,59,1,6,59,63,1,10,63,67,2,67,9,71,1,71,5,75,1,13,75,79,2,79,13,83,1,83,9,87,2,10,87,91,2,91,6,95,2,13,95,99,1,10,99,103,2,9,103,107,1,107,5,111,2,9,111,115,1,5,115,119,1,9,119,123,2,123,6,127,1,5,127,131,1,10,131,135,1,135,6,139,1,139,5,143,1,143,9,147,1,5,147,151,1,151,13,155,1,5,155,159,1,2,159,163,1,163,6,0,99,2,0,14,0'

program_orig = list(map(int, program_string.split(',')))

def run_program(noun, verb):
	#print("run_program(%d, %d)" % (noun, verb))
	program = list(program_orig)

	# set input
	program[1] = noun
	program[2] = verb

	pos = 0
	halt = False
	while pos < len(program):
		if program[pos] == 99:
			halt = True
			break

		arg1 = program[pos + 1]
		arg2 = program[pos + 2]
		dest = program[pos + 3]

		if program[pos] == 1:
			program[dest] = program[arg1] + program[arg2]
		elif program[pos] == 2:
			program[dest] = program[arg1] * program[arg2]
		else:
			print("invalid opcode %d at pos %d" % (program[pos], pos))
			exit(0)

		pos += 4

	if False:
		if halt:
			print("halted!")
		else:
			print("PROGRAM NOT HALTED BUT REACHED END OF INPUT")

	return program[0]

for noun in range(0, 100):
	for verb in range(0, 100):
		x = run_program(noun, verb)

		print("noun=%d verb=%d => %d" % (noun, verb, x))

		if x == 19690720:
			print("noun, verb = %d, %d" % (noun, verb))
			print("100 * noun + verb = %d" % (100 * noun + verb))
			break

	# hack to lazily allow the inner-loop break to also break the outer loop
	else:
		continue

	break

