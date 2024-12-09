from tools.aoc import AOCDay
from typing import Any

class Day(AOCDay):
	def parse(self):
		self.file_system: list[(int | None, int)] = []

		for i, block_count in enumerate(map(int, list(self.getInput()))):
			if i % 2 == 0:
				self.file_system += [(i//2, block_count)]
			else:
				self.file_system += [(None, block_count)]

	def p1(self):
		# could optimize by tracking last *used* index, instead of always searching from end of list
		block_pos = 0
		checksum = 0
		for fs_i in range(len(self.file_system)):
			(file_id, block_count) = self.file_system[fs_i]

			if file_id is not None:
				checksum += sum((block_pos + i) * file_id for i in range(block_count))
				block_pos += block_count
				continue

			free_space = block_count
			source_i = len(self.file_system)
			while free_space > 0 and source_i > fs_i:
				source_i -= 1
				(source_file_id, source_block_count) = self.file_system[source_i]

				if source_file_id is None or source_block_count == 0:
					continue

				move_block_count = min(free_space, source_block_count)
				self.file_system[source_i] = (source_file_id, source_block_count - move_block_count)

				checksum += sum((block_pos + i) * source_file_id for i in range(move_block_count))
				block_pos += move_block_count
				free_space -= move_block_count

		return checksum

	def p2(self):
		# could optimize by computing checksum in main loop; also see p1 note.
		try_move_i = len(self.file_system)
		while try_move_i > 1:
			try_move_i -= 1

			if self.file_system[try_move_i][0] is None:
				continue

			(source_file_id, source_block_count) = self.file_system[try_move_i]

			for target_i in range(try_move_i):
				(target_file_id, target_block_count) = self.file_system[target_i]

				if target_file_id is not None or target_block_count < source_block_count:
					continue

				# we can move this file
				self.file_system[target_i] = self.file_system[try_move_i]
				self.file_system[try_move_i] = (None, source_block_count)
				# looks like we don't need to consolidate multiple entries of free space

				gap_blocks = target_block_count - source_block_count
				if gap_blocks == 0:
					break

				# remaining gap needs a new slot
				# try_move_i is bumped, as a new element took its place.
				try_move_i += 1
				self.file_system.insert(target_i + 1, (None, gap_blocks))
				break

		checksum = 0
		block_pos = 0
		for (file_id, block_count) in self.file_system:
			if file_id is None:
				block_pos += block_count
				continue

			for _ in range(block_count):
				checksum += block_pos * file_id
				block_pos += 1

		return checksum

	def part1(self) -> Any:
		self.parse()
		return self.p1()

	def part2(self) -> Any:
		self.parse()
		return self.p2()

	inputs = [
		[
			(1928, "input9-test"),
			(6154342787400, "input9"),
		],
		[
			(2858, "input9-test"),
			(6183632723350, "input9"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 9)
	day.run(verbose=True)
