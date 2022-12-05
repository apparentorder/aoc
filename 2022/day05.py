from tools.aoc import AOCDay
from typing import Any

def parse(input):
	stacks = [[] for _ in range(10)]

	for i in range(len(input)):
		line = input[0]
		input = input[1:]

		if '1' in line:
			break

		num_crates = (len(line) - 2) // 4 + 1

		for crate_pos in range(num_crates):
			crate = line[1 + crate_pos*4]
			if crate.isupper():
				stacks[crate_pos] += [crate]

	input = input[1:] # drop empty line

	instructions = []
	for line in input:
		elem = line.split(" ")
		instructions += [{
			"from_stack": int(elem[3]),
			"to_stack": int(elem[5]),
			"count": int(elem[1])
		}]
	
	#print("stacks %s\ninstructions %s" % (stacks, instructions))
	return stacks, instructions

def moves(stacks, instructions, multiple: bool):
	for move in instructions:
		#print(move)
		for i in range(move["count"]):
			target_pos = i if multiple else 0
			crate = stacks[move["from_stack"] - 1].pop(0)
			stacks[move["to_stack"] - 1].insert(target_pos, crate)
		#print(stacks)
		#print()

class Day(AOCDay):
	inputs = [
		[
			('CMZ', '05-test')
			,('VJSFHWGFT', '05')
		],
		[
			('MCD', '05-test')
			,('LCTQFBVZV', '05')
		]
	]

	def part1(self) -> Any:
		stacks, instructions = parse(self.getInput())
		moves(stacks, instructions, False)
		message = "".join([stack[0] for stack in stacks if len(stack) > 0])
		return message

	def part2(self) -> Any:
		stacks, instructions = parse(self.getInput())
		moves(stacks, instructions, True)
		message = "".join([stack[0] for stack in stacks if len(stack) > 0])
		return message

