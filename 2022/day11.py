from tools.aoc import AOCDay
from tools.ocr_ascii import AsciiOcr
from typing import Any

class Monkey:
	def __init__(self, lines):
		self.items_inspected = 0

		if not lines[0].startswith("Monkey "):
			raise Exception("bad input: %s" % (lines))

		for line in lines:
			e = line.split()

			match e[0]:
				case "Monkey":
					self.id = int(e[1].rstrip(":"))
				case "Starting":
					self.items = list(map(int, [i.rstrip(",") for i in e[2:]]))
				case "Operation:":
					self.operation = "multiply" if e[4] == "*" else "add"
					self.operand = None if e[5] == "old" else int(e[5])
				case "Test:":
					self.test_divisor = int(e[3])
				case "If":
					if e[1] == "true:":
						self.target_if_true = int(e[5])
					else:
						self.target_if_false = int(e[5])
				case _:
					raise Exception("bad input: %s" % (line))

	def inspect_item(self, worry_divisor, worry_modulo): # returns item, target
		worry = self.items.pop(0)
		self.items_inspected += 1

		operand = self.operand or worry
		worry = (worry * operand) if self.operation == "multiply" else (worry + operand)
		worry //= worry_divisor
		worry %= worry_modulo

		if worry % self.test_divisor == 0:
			return worry, self.target_if_true
		else:
			return worry, self.target_if_false

	def catch(self, item):
		self.items += [item]

	def __str__(self):
		return ", ".join([f"{k}={v}" for k,v in sorted(vars(self).items())])

class MonkeyBusiness:
	def __init__(self, lines, worry_divisor):
		self.monkeys = []
		self.worry_divisor = worry_divisor

		while len(lines) > 0:
			if lines[0] == "":
				lines = lines[1:]

			self.monkeys.append(Monkey(lines[:6]))
			lines = lines[6:]

		# find LCM
		divs = sorted(m.test_divisor for m in self.monkeys)
		self.worry_modulo = divs.pop()

		while len(divs) > 0:
			step = self.worry_modulo
			n = divs.pop()

			while self.worry_modulo % n != 0:
				self.worry_modulo += step

		#print(f"lcm {self.worry_modulo}")

	def keep_away(self, rounds):
		for round in range(1, rounds + 1):
			for i in range(len(self.monkeys)):
				while len(self.monkeys[i].items) > 0:
					item, target = self.monkeys[i].inspect_item(self.worry_divisor, self.worry_modulo)
					self.monkeys[target].catch(item)

			if False and rounds < 100:
				print(f"round {round}:")
				print(self)
				print()

	def result(self):
		ii = sorted([m.items_inspected for m in self.monkeys], reverse = True)
		return ii[0] * ii[1]

	def __str__(self):
		s = [f"monkey {i} {m}" for i, m in enumerate(self.monkeys)]
		return "\n".join(s)

class Day(AOCDay):
	inputs = [
		[
			(10605, '11-test')
			,(56595, '11')
		],
		[
			(2_713_310_158, '11-test')
			,(15_693_274_740, '11')
		]
	]

	def part1(self) -> Any:
		monkeybiz = MonkeyBusiness(self.getInput(), 3)
		monkeybiz.keep_away(20)
		#print(f"final state:\n{monkeybiz}\n")
		return monkeybiz.result()

	def part2(self) -> Any:
		monkeybiz = MonkeyBusiness(self.getInput(), 1)
		monkeybiz.keep_away(10_000)
		#print(f"final state:\n{monkeybiz}\n")
		return monkeybiz.result()

