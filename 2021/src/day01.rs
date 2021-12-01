use crate::aoc;

pub fn part1(input: String) -> String {
	let mut prev = i32::MAX;
	let mut count = 0;

	for line in input.split('\n') {
		let i: i32 = line.parse().unwrap();

		if i > prev {
			count += 1;
		}

		prev = i;
	}

	return count.to_string()
}


pub fn part2(input: String) -> String {
	let mut prev = i32::MAX;
	let mut count = 0;
	let mut window = vec![];

	for line in input.split('\n') {
		let i: i32 = line.parse().unwrap();

		window.push(i);

		if window.len() >= 3 {
			let sum = window.iter().sum();
			//println!("sum {}", sum);

			if sum > prev {
				count += 1;
			}

			prev = sum;
			window.remove(0);
		}
	}

	return count.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 1,
	input: "file:01-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("7", "file:01-input-test"),
	],
	tests_part2: &[
		("5", "file:01-input-test"),
	],
};

