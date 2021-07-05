use crate::aoc;

fn checksum(input: &String, even_divide: bool) -> String {
	let mut checksum = 0;

	for row in input.split('\n') {
		let mut numbers: Vec<i32> =
			row
			.split_whitespace()
			.map(|number_string| {
				number_string.parse().unwrap()
			})
			.collect();

		numbers.sort();
		numbers.reverse();

		let max: &i32 = numbers.first().unwrap();
		let min: &i32 = numbers.last().unwrap();

		if !even_divide {
			checksum += max - min;
			println!("(min={} max={} diff={}) {}", min, max, max-min, row);
		} else {
			'outer: for dividend in numbers.iter() {
				for divisor in numbers.iter().filter(|n| n != &dividend) {
					if dividend % divisor == 0 {
						checksum += dividend/divisor;
						println!("({}/{}) {}", dividend, divisor, row);
						break 'outer
					}
				}
			}
		}
	}

	return checksum.to_string()
}

pub fn part1(input: String) -> String {
	return checksum(&input, false);
}

pub fn part2(input: String) -> String {
	return checksum(&input, true);
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 2,
	input: "file:02-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("18", "file:02-test"),
	],
	tests_part2: &[
		("9", "file:02-test-part2"),
	],
};

