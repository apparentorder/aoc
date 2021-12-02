use crate::aoc;

pub fn part1(input: String) -> String {
	let mut x = 0;
	let mut y = 0;

	for line in input.split('\n') {
		let mut parts = line.split_whitespace();

		let movement = parts.next().unwrap();
		let val: i32 = parts.next().unwrap().parse().unwrap();

		match movement {
			"forward" => x += val,
			"down" => y += val,
			"up" => y -= val,
			_ => panic!(),
		}
	}

	return (x*y).to_string()
}

pub fn part2(input: String) -> String {
	let mut x = 0;
	let mut y = 0;
	let mut aim = 0;

	for line in input.split('\n') {
		let mut parts = line.split_whitespace();

		let movement = parts.next().unwrap();
		let val: i32 = parts.next().unwrap().parse().unwrap();

		match movement {
			"forward" => {
				x += val;
				y += aim * val;
			},
			"down" => aim += val,
			"up" => aim -= val,
			_ => panic!(),
		}
	}

	return (x*y).to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 2,
	input: "file:02-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("150", "file:02-input-test"),
	],
	tests_part2: &[
	],
};

