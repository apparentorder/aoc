use crate::aoc;

struct Generator {
	value: u64,
	factor: u64,
	find_multiples_of: Option<u64>,
}

impl Iterator for Generator {
	type Item = u64;

	fn next(&mut self) -> Option<Self::Item> {
		loop {
			self.value = (self.value * self.factor) % 2147483647;
			let judge_value = self.value & 0xffff;

			if let Some(fmo) = self.find_multiples_of {
				if judge_value % fmo == 0 {
					return Some(judge_value)
				}
				// else: keep looping
			} else {
				return Some(judge_value)
			}
		}
	}
}

fn count_equal_results(mut a: Generator, mut b: Generator, pairs: u64) -> u64 {
	let mut r = 0;

	for _ in 0..pairs {
		let value_a = a.next().unwrap();
		let value_b = b.next().unwrap();

		if value_a == value_b {
			r += 1;
		}
	}

	return r
}

pub fn part1(input: String) -> String {
	let mut i = input.split_whitespace();
	let start_a: u64 = i.next().unwrap().parse().unwrap();
	let start_b: u64 = i.next().unwrap().parse().unwrap();

	let a = Generator { value: start_a, factor: 16807, find_multiples_of: None };
	let b = Generator { value: start_b, factor: 48271, find_multiples_of: None };

	return count_equal_results(a, b, 40_000_000).to_string()
}

pub fn part2(input: String) -> String {
	let mut i = input.split_whitespace();
	let start_a: u64 = i.next().unwrap().parse().unwrap();
	let start_b: u64 = i.next().unwrap().parse().unwrap();

	let a = Generator { value: start_a, factor: 16807, find_multiples_of: Some(4) };
	let b = Generator { value: start_b, factor: 48271, find_multiples_of: Some(8) };

	return count_equal_results(a, b, 5_000_000).to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 15,
	input: "618 814",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("588", "65 8921"),
	],
	tests_part2: &[
		("309", "65 8921"),
	],
};

