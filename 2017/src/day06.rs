use crate::aoc;
use std::collections::HashMap;

fn solve(input: String, is_part2: bool) -> String {
	let mut banks: Vec<usize> = vec![];
	let mut states_seen: HashMap<Vec<usize>, usize> = HashMap::new();
	let mut iterations = 0;

	// parse input into banks
	for block in input.split_whitespace() {
		banks.push(block.parse().unwrap());
	}

	//println!("starting state: {:?}", banks);

	// find infinite loop state
	loop {
		let mut largest_count = 0;
		let mut source_bank_index = 0;
		iterations += 1;

		// find largest (source) bank
		for i in 0..banks.len() {
			if banks[i] > largest_count {
				largest_count = banks[i];
				source_bank_index = i;
			}
		}

		// empty source bank
		banks[source_bank_index] = 0;

		// distribute blocks over all banks
		for offset in 1..=largest_count {
			let target_bank_index = (source_bank_index + offset) % banks.len();
			banks[target_bank_index] += 1;
		}

		if let Some(prev_index) = states_seen.get(&banks) {
			if is_part2 {
				// return iteration *cycle* count (since pattern's prev. occurrence)
				return (iterations - prev_index).to_string();
			} else {
				// return iteration count (since start)
				return iterations.to_string();
			}
		}

		states_seen.insert(banks.to_vec(), iterations);
	}
}

pub fn part1(input: String) -> String {
	return solve(input, false);
}

pub fn part2(input: String) -> String {
	return solve(input, true);
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 06,
	input: "4 1 15 12 0 9 9 5 5 8 7 3 14 5 12 3",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("5", "0 2 7 0"),
	],
	tests_part2: &[
		("4", "0 2 7 0"),
	],
};

