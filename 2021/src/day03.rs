use crate::aoc;

fn rating(values: &Vec<i32>, bits: i32, find_most_common: bool) -> i32 {
	let mut candidates = values.clone();

	for check_bit in (0..bits).rev() {
		let mut keep_value = most_common_bit(&candidates, check_bit).unwrap_or(1);
		if !find_most_common {
			keep_value = !keep_value & 1;
		}

		//println!("pos={} len={} count1={} keep {}", check_bit, candidates.len(), count1, keep_value);
		candidates.retain(|&v| v & (1<<check_bit) == keep_value<<check_bit);
		//println!("{:?}", candidates);
		//println!();

		if candidates.len() == 1 {
			break
		}
	}

	assert!(candidates.len() == 1);
	return candidates[0]
}

fn most_common_bit(values: &Vec<i32>, bit: i32) -> Option<i32> {
	// returns None when tied

	let count1 = values.iter().filter(|&v| v & (1<<bit) != 0).count();
	let count0 = values.len() - count1;

	return if count1 == count0 {
		None
	} else if count1 > count0 {
		Some(1)
	} else {
		Some(0)
	}
}

fn parse(input: String) -> Vec<i32> {
	return input.split('\n').map(|line| i32::from_str_radix(line, 2).unwrap()).collect();
}

pub fn part1(input: String) -> String {
	let bits = input.split('\n').nth(0).unwrap().len() as i32;
	let values = parse(input);

	let mut gamma = 0;
	let mut epsilon = 0;

	for check_bit in 0..bits {
		let b = most_common_bit(&values, check_bit).unwrap(); // per puzzle instructions: no ties expected
		gamma += b<<check_bit;
		epsilon += (!b & 1)<<check_bit;
	}

	return (gamma * epsilon).to_string()
}

pub fn part2(input: String) -> String {
	let bits = input.split('\n').nth(0).unwrap().len() as i32;
	let ints = parse(input);

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

