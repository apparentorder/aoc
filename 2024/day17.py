from tools.aoc import AOCDay
from typing import Any

class Computer:
	def __init__(self, input_lines: list[str]):
		self.A = next(int(line.split(" ")[-1]) for line in input_lines if line.startswith("Register A"))
		self.B = next(int(line.split(" ")[-1]) for line in input_lines if line.startswith("Register B"))
		self.C = next(int(line.split(" ")[-1]) for line in input_lines if line.startswith("Register C"))
		self.program = next(list(map(int, line.split(" ")[-1].split(","))) for line in input_lines if line.startswith("Program"))
		self.output: list[int] = []

	def combo_value(self, operand: int) -> int:
		if operand == 4: return self.A
		if operand == 5: return self.B
		if operand == 6: return self.C
		return operand

	def run_with_A(self, A: int) -> list[int]:
		self.output = []
		self.A = A
		self.B = 0
		self.C = 0
		return self.run()

	def run(self) -> list[int]:
		iptr = 0

		while iptr < len(self.program):
			opcode = self.program[iptr]
			operand = self.program[iptr + 1]

			if opcode == 0: # adv
				operand = self.combo_value(operand)
				self.A = self.A // 2**operand
			elif opcode == 1: # bxl
				self.B ^= operand
			elif opcode == 2: # bst
				operand = self.combo_value(operand)
				self.B = operand % 8
			elif opcode == 3: # jnz
				if self.A != 0:
					iptr = operand
					continue
			elif opcode == 4: # bxc
				self.B ^= self.C
			elif opcode == 5: # out
				operand = self.combo_value(operand)
				self.output += [operand % 8]
			elif opcode == 6: # bdv
				operand = self.combo_value(operand)
				self.B = self.A // 2**operand
			elif opcode == 7: # cdv
				operand = self.combo_value(operand)
				self.C = self.A // 2 ** operand

			iptr += 2

		return self.output

class Day(AOCDay):
	def part1(self) -> Any:
		c = Computer(self.getInput())
		output = ",".join(map(str, c.run()))
		return output

	def part2(self) -> Any:
		c = Computer(self.getInput())

		a = 0
		for _ in range(len(c.program)):
			a *= 8
			for x in range(8**8): # something is wrong here.
				test_output = c.run_with_A(a + x)

				l = len(test_output)
				if l < 3:
					continue

				if test_output == c.program:
					return a + x

				if test_output == c.program[-l:]:
					# partial match up to here, so this `a` is good.
					# print(f"match: {c.output} v {c.program[-l:]} at {try_a}")
					a += x
					break

	"""
	reconstructed from input:
	
	- number of output parts == number of loops
	- `A` always //8, so for `n` loops, A > 8**n
	- therefore three bits per output item, then shifted left three times (or *= 8)
	- many values per output item will work for that one item, but only the "correct" value will
	  not break the other values; critical part seems to be `C  A // 2**B` here, but i haven't
	  fully understood this yet.
	
	while A > 0:
		# 2,4
		B = A % 8

		# 1,3
		B = (B XOR 3) % 8

		# 7,5
		C = A // 2**B

		# 4,2
		B = (B XOR C) % 8

		# 0,3
		A = A // 2**3

		# 1,5
		B = (B XOR 5) % 8

		# 5,5
		output regB % 8
	"""

	inputs = [
		[
			("4,6,3,5,6,3,5,2,1,0", "input17-test"),
			("1,7,6,5,1,0,5,0,7", "input17"),
		],
		[
			(117440, "input17-test-p2"),
			(236555995274861, "input17"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 17)
	day.run(verbose=True)
