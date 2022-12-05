from tools.aoc import AOCDay
from typing import Any

def parse(input):
	end_of_map = input.index("")
	input_map = input[:end_of_map]
	input_instructions = input[end_of_map + 1:]

	stacks = {}
	for i, c in enumerate(input_map.pop()):
		if c.isnumeric():
			stack_id = int(c)
			stacks[stack_id] = {
				"column": i,
				"crates": []
			}

	for line in input_map:
		for stack_id in stacks:
			crate = line[stacks[stack_id]["column"]]
			if crate.isupper():
				stacks[stack_id]["crates"] += [crate]

	instructions = []
	for line in input_instructions:
		elem = line.split()
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
			crate = stacks[move["from_stack"]]["crates"].pop(0)
			stacks[move["to_stack"]]["crates"].insert(target_pos, crate)
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
		return "".join(stacks[stack_id]["crates"][0] for stack_id in sorted(stacks))

	def part2(self) -> Any:
		stacks, instructions = parse(self.getInput())
		moves(stacks, instructions, True)
		return "".join(stacks[stack_id]["crates"][0] for stack_id in sorted(stacks))

