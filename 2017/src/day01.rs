use crate::aoc;

fn solve(input: &String, compare_distance: usize) -> String {
	let digits = input.as_bytes();
	let mut r: u32 = 0;

	for i in 0..digits.len() {
		// n.b.: we're accessing the numbers' ASCII codes, therefore we need to do -= 48
		// to get the actual digits (digits 0..=9 start at ASCII 48).
		let this_digit = digits[i] - 48;
		let next_digit = digits[(i + compare_distance) % digits.len()] - 48;

		if this_digit == next_digit {
			println!("matching: {}", this_digit);
			r += this_digit as u32;
		}
	}

	return r.to_string();
}

pub fn part1(input: String) -> String {
	return solve(&input, 1);
}

pub fn part2(input: String) -> String {
	return solve(&input, input.len() / 2);
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 1,
	input: "file:01-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("3", "1122"),
		("4", "1111"),
		("0", "1234"),
		("9", "91212129"),
	],
	tests_part2: &[
		("6", "1212"),
		("0", "1221"),
		("4", "123425"),
		("12", "123123"),
		("4", "12131415"),
	],
};

