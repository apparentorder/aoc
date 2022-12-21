from tools.aoc import AOCDay
from typing import Any
import json
import re

class Monkey:
	def __init__(self, s):
		e = s.split(": ")
		self.id = e[0]

		e = e[1].split(" ")
		self.lhs = None
		self.op = None
		self.rhs = None
		self.number = None

		if e[0].isnumeric():
			self.number = int(e[0])
		else:
			self.lhs, self.op, self.rhs = e[0], e[1], e[2]

	def solve(self, lhs, rhs):
		if self.op == '+':
			return lhs + rhs
		elif self.op == '-':
			return lhs - rhs
		elif self.op == '*':
			return lhs * rhs
		elif self.op == '/':
			return lhs // rhs

	def solve_expected(self, lhs, rhs, expected_result):
		known_result = lhs if lhs is not None else rhs
		is_human_lhs = lhs is None

		next_expected_result = None
		if self.op == '-':
			if is_human_lhs:
				next_expected_result = expected_result + rhs
			else:
				next_expected_result = (expected_result - lhs) * -1
		if self.op == '+':
			next_expected_result = expected_result - known_result
		if self.op == '*':
			next_expected_result = expected_result // known_result
		if self.op == '/':
			if is_human_lhs:
				next_expected_result = expected_result * rhs
			else:
				next_expected_result = (lhs//expected_result)

		return next_expected_result

class RiddleMonkeys:
	def __init__(self, input):
		self.monkeys = {}

		for line in input:
			monkey = Monkey(line)
			self.monkeys[monkey.id] = monkey

	def solve(self, target, expected_result = None, skip_human = False):
		if expected_result is not None:
			skip_human = True

		if target == "humn" and skip_human:
			return expected_result # possibly None

		monkey = self.monkeys[target]

		if monkey.number is not None:
			return monkey.number

		lhs = self.solve(monkey.lhs, skip_human = skip_human)
		rhs = self.solve(monkey.rhs, skip_human = skip_human)

		if expected_result is None:
			if lhs is None or rhs is None:
				return None

			return monkey.solve(lhs, rhs)
		else:
			#print(f"exp {expected_result} for {target}, lhs {monkey.lhs} rhs {monkey.rhs}")
			unknown_monkey_id = monkey.lhs if lhs is None else monkey.rhs
			next_expected_result = monkey.solve_expected(lhs, rhs, expected_result)

			#print(f"exp {expected_result} for {target}: next_er {next_expected_result} for {unknown_monkey_id}")
			return self.solve(unknown_monkey_id, expected_result = next_expected_result)

class Day(AOCDay):
	inputs = [
		[
			(152, '21-test')
			,(41857219607906, '21-penny')
			,(21_120_928_600_114, '21')
		],
		[
			(301, '21-test')
			,(3916936880448, '21-penny')
			,(3_453_748_220_116, '21')
		]
	]

	def part1(self) -> Any:
		monkeys = RiddleMonkeys(self.getInput())
		return monkeys.solve('root')

	def part2(self) -> Any:
		monkeys = RiddleMonkeys(self.getInput())

		root = monkeys.monkeys["root"]
		lhs = monkeys.solve(root.lhs, skip_human = True)
		rhs = monkeys.solve(root.rhs, skip_human = True)

		known_result = rhs if lhs is None else lhs
		unknown_monkey_id = root.lhs if lhs is None else root.rhs

		#print(f"monkey root tests equality; kr={known_result} unknown={unknown_monkey_id}")
		return monkeys.solve(unknown_monkey_id, expected_result = known_result)

