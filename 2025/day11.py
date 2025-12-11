from tools.aoc import AOCDay
from typing import Any

class Day(AOCDay):
	def part1(self) -> Any:
		self.connections = self.parse_input()
		return self.count_paths("you", "out")

	def part2(self) -> Any:
		self.connections = self.parse_input()
		svr_dac = self.count_paths("svr", "dac", skip = "fft")
		svr_fft = self.count_paths("svr", "fft", skip = "dac")

		dac_fft = self.count_paths("dac", "fft")
		fft_dac = self.count_paths("fft", "dac")

		dac_out = self.count_paths("dac", "out", skip = "fft")
		fft_out = self.count_paths("fft", "out", skip = "dac")

		return (
			svr_dac * dac_fft * fft_out +
			svr_fft * fft_dac * dac_out
		)

	path_cache = {}

	def count_paths(self, from_device: str, to_device: str, skip: str | None = None, reset = True) -> int:
		if reset:
			# avoid poisoning the cache with paths that had `skip` set
			self.path_cache = {}

		if from_device == to_device:
			return 1

		if from_device == "out":
			return 0

		if skip and from_device == skip:
			return 0

		count = 0
		for next_device in self.connections[from_device]:
			key = (next_device, to_device)

			if key in self.path_cache:
				count += self.path_cache[key]
				continue

			r = self.count_paths(
				from_device = next_device,
				to_device = to_device,
				skip = skip,
				reset = False,
			)

			self.path_cache[key] = r
			count += r

		return count

	def parse_input(self) -> dict[str, list[str]]:
		return {
			line.split()[0][:-1]: line.split()[1:]
			for line in self.getInput()
		}

	inputs = [
		[
			(5, "input11-test"),
			(634, "input11-penny"),
			(674, "input11"),
		],
		[
			(2, "input11-test-p2"),
			(377452269415704, "input11-penny"),
			(438314708837664, "input11"),
		]
	]

if __name__ == '__main__':
	day = Day(2025, 11)
	day.run(verbose=True)
