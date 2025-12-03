from tools.aoc import AOCDay
from typing import Any, Generator

class Day(AOCDay):
	def joltage(self, bank: list[int], digits: int) -> int:
		# strategy: start with the last $digits digits in the bank,
		# then try to replace each digit with the largest remaining digit

		jolt = bank[(len(bank) - digits):]
		bank_remaining = bank[:-digits]

		for i_digit in range(digits):
			i_max = bank_remaining.index(max(bank_remaining))
			if bank_remaining[i_max] < jolt[i_digit]:
				# no more digits to be moved
				break

			bank_remaining += [jolt[i_digit]]
			jolt[i_digit] = bank_remaining[i_max]
			bank_remaining = bank_remaining[i_max+1:]

		return sum(n * 10**i for i, n in enumerate(reversed(jolt)))

	def part1(self) -> Any:
		return sum(self.joltage(list(map(int, bank)), digits = 2) for bank in self.getInput())

	def part2(self) -> Any:
		return sum(self.joltage(list(map(int, bank)), digits = 12) for bank in self.getInput())

	inputs = [
		[
			(357, "input3-test"),
			(17109, "input3-penny"),
			(17311, "input3"),
		],
		[
			(3121910778619, "input3-test"),
			(169347417057382, "input3-penny"),
			(171419245422055, "input3"),
		]
	]

if __name__ == '__main__':
	day = Day(2025, 3)
	day.run(verbose=True)
