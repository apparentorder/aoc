from tools.aoc import AOCDay
from typing import Any
import json
import re

class Monkey:
	def __init__(self, s):
		e = s.split(": ")
		self.id = e[0]

		e = e[1].split(" ")
		self.op1 = None
		self.op = None
		self.op2 = None
		self.number = None

		if e[0].isnumeric():
			self.number = int(e[0])
		else:
			self.op1, self.op, self.op2 = e[0], e[1], e[2]

	def known_number(self):
		if self.number is not None:
			return self.number

class RiddleMonkeys:
	def __init__(self, input):
		self.monkeys = {}

		for line in input:
			monkey = Monkey(line)
			self.monkeys[monkey.id] = monkey

	def solve(self, target, skip_human = False):
		#print(f"solve: {target}, sh={skip_human}")
		if target == "humn" and skip_human:
			return None

		monkey = self.monkeys[target]
		n = monkey.known_number()
		if n is not None:
			return n

		n1 = self.solve(monkey.op1, skip_human=skip_human)
		n2 = self.solve(monkey.op2, skip_human=skip_human)

		#print(f"solve() for op1={monkey.op1} = {n1}")
		#print(f"solve() for op2={monkey.op2} = {n2}")

		if n1 is None or n2 is None:
			return None

		if monkey.op == '+':
			return n1 + n2
		elif monkey.op == '-':
			return n1 - n2
		elif monkey.op == '*':
			return n1 * n2
		elif monkey.op == '/':
			return n1 // n2

	def solve_equal(self, target):
		unknown = self.monkeys[target]

		n1 = self.solve(unknown.op1, skip_human = True)
		n2 = self.solve(unknown.op2, skip_human = True)

		print(f"solve_eq n1 {n1}, n2 {n2}")

		known = n1 if n1 is not None else n2
		monkey_unknown = unknown.op1 if n1 is None else unknown.op2

		print(f"known result {known}, unknown side is {monkey_unknown}")

		return self.solve_expect(monkey_unknown, known)

	def solve_expect(self, unknown_id, expected_result):
		print(f"solve_expect for id {unknown_id}")

		if unknown_id == "humn":
			return expected_result

		monkey_unknown = self.monkeys[unknown_id]

		n = monkey_unknown.known_number()
		if n is not None:
			return n

		n1 = self.solve(monkey_unknown.op1, skip_human = True)
		n2 = self.solve(monkey_unknown.op2, skip_human = True)

		print(f"expect {expected_result}, n1 {n1}, n2 {n2}")
		known = n1 if n1 is not None else n2
		unknown = monkey_unknown.op1 if n1 is None else monkey_unknown.op2

		is_human_op1 = n1 is None

		expect = None
		if monkey_unknown.op == '-':
			if is_human_op1:
				print( expected_result + n2)
				expect = expected_result + n2
			else:
				print( (expected_result - n1) * -1)
				expect = (expected_result - n1) * -1
		if monkey_unknown.op == '+':
			expect = expected_result - known
		if monkey_unknown.op == '*':
			expect = expected_result // known
		if monkey_unknown.op == '/':
			if is_human_op1:
				print( expected_result * n2)
				expect = expected_result * n2
			else:
				print(n1//expected_result)
				expect = (n1//expected_result)

		return self.solve_expect(unknown, expect)

class Day(AOCDay):
	inputs = [
		[
			(152, '21-test')
			,(21_120_928_600_114, '21')
		],
		[
			(301, '21-test')
			,(3_453_748_220_116, '21')
		]
	]

	def part1(self) -> Any:
		monkeys = RiddleMonkeys(self.getInput())
		return monkeys.solve('root')

	def part2(self) -> Any:
		monkeys = RiddleMonkeys(self.getInput())
		return monkeys.solve_equal("root")

