use crate::aoc;
use std::collections::HashMap;

pub fn part1(input: String) -> String {
	let bits = input.split('\n').nth(0).unwrap().len();
	let values = input.split('\n').count();

	//let counts: HashMap<i32, i32> = HashMap::new();
	let mut count1 = vec![0; bits];

	for line in input.split('\n') {
		let i = i32::from_str_radix(line, 2).unwrap();

		for b in 0..bits {
			if i & (1<<b) != 0 {
				count1[b] += 1;
			}
		}
	}

	let mut gamma = 0;
	for b in 0..bits {
		if count1[b] >= values/2 {
			gamma += 1<<b;
		}
	}

	let epsilon = !gamma & ((1<<bits) - 1);

	return (gamma * epsilon).to_string()
}

fn rating(values: &Vec<i32>, bits: usize, find_most_common: bool) -> i32 {
	let mut candidates = values.clone();
	let mut check_position = bits;

	while candidates.len() != 1 {
		let mut count1 = 0;

		check_position -= 1;

		for c in &candidates {
			if c & (1<<check_position) != 0 {
				count1 += 1;
			}
		}

		let count0 = candidates.len() - count1;

		let keep_value;
		if find_most_common {
			keep_value = if count1 > count0 || count0 == count1 { 1 } else { 0 };
		} else /* least common value */ {
			keep_value = if count1 > count0 || count0 == count1 { 0 } else { 1 };
		}

		println!("pos={} len={} count1={} keep {}", check_position, candidates.len(), count1, keep_value);

		for i in (0..candidates.len()).rev() {
			let b = if candidates[i] & (1<<check_position) != 0 { 1 } else { 0 };
			if b != keep_value {
				candidates.remove(i);
			}
		}

		println!("{:?}", candidates);
		println!();
	}

	return candidates[0]
}

pub fn part2(input: String) -> String {
	let bits = input.split('\n').nth(0).unwrap().len();
	let values = input.split('\n').count();

	let mut count1 = vec![0; bits];

	let ints: Vec<i32> = input.split('\n').map(|line| i32::from_str_radix(line, 2).unwrap()).collect();

	let oxy = rating(&ints, bits, true);
	let co2 = rating(&ints, bits, false);

	return (oxy * co2).to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 3,
	input: "file:03-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("198", "file:03-input-test"),
	],
	tests_part2: &[
		("230", "file:03-input-test"),
	],
};

