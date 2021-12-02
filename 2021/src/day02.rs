use crate::aoc;

fn dive(input: String, is_part2: bool) -> i32 {
	let mut x = 0;
	let mut y = 0;
	let mut aim = 0;

	for line in input.split('\n') {
		let mut parts = line.split_whitespace();

		let movement = parts.next().unwrap();
		let val: i32 = parts.next().unwrap().parse().unwrap();

		if is_part2 {
			match movement {
				"up" => aim -= val,
				"down" => aim += val,
				"forward" => {
					x += val;
					y += aim * val;
				},
				_ => panic!(),
			}
		} else /* part1 */ {
			match movement {
				"up" => y -= val,
				"down" => y += val,
				"forward" => x += val,
				_ => panic!(),
			}
		}
	}

	return x*y
}

pub fn part1(input: String) -> String {
	dive(input, false).to_string()
}

pub fn part2(input: String) -> String {
	dive(input, true).to_string()
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
		("900", "file:02-input-test"),
	],
};

