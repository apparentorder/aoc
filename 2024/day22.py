from tools.aoc import AOCDay
from collections import deque, defaultdict
from typing import Any, Iterable


class Day(AOCDay):
	def buyer_secrets(self, initial_secret: int, limit: int) -> Iterable:
		secret = initial_secret

		for _ in range(limit):
			secret = ((secret   * 64) ^ secret) % 2**24
			secret = ((secret  // 32) ^ secret) % 2**24
			secret = ((secret * 2048) ^ secret) % 2**24
			yield secret

	def scan_for_sequences(self, initial_secret: int, n: int):
		change_sequence: deque[int] = deque([2**64] * 4)
		change_sequence_seen: set[str] = set()

		price_prev = initial_secret % 10
		for secret in self.buyer_secrets(initial_secret, limit = 2000):
			price = secret % 10
			change_sequence.append(price - price_prev)
			change_sequence.popleft()
			price_prev = price

			cs = str(change_sequence)
			if not cs in change_sequence_seen:
				self.bananas_by_sequence[cs] += price
				change_sequence_seen.add(cs)

	def part1(self) -> Any:
		return sum(
			list(self.buyer_secrets(secret, limit = 2000))[-1]
			for secret in map(int, self.getInput())
		)

	def part2(self) -> Any:
		# worst case is 19^4 ~ 130k dict entries, so fuck it.
		# (actually ~40k for my input)

		self.bananas_by_sequence: dict[str, int] = defaultdict(int)
		for secret in map(int, self.getInput()):
			self.scan_for_sequences(secret, n = 2000)

		return max(self.bananas_by_sequence.values())

	inputs = [
		[
			(37327623, "input22-test"),
			(18525593556, "input22"),
		],
		[
			(23, "input22-test-p2"),
			(2089, "input22"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 22)
	day.run(verbose=True)
