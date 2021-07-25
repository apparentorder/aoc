use crate::aoc;

fn solve(input: String, is_part2: bool) -> String {
	let mut instructions: Vec<i32> = vec![];
	let mut ptr: usize = 0;
	let mut steps = 0;

	for line in input.split('\n') {
		instructions.push(line.parse().unwrap());
	}

	loop {
		let jump_to = (ptr as i32) + instructions[ptr];
		steps += 1;

		if !(0..instructions.len() as i32).contains(&jump_to) {
			break
		}

		if is_part2 && instructions[ptr] >= 3 {
			instructions[ptr] -= 1;
		} else {
			instructions[ptr] += 1;
		}

		ptr = jump_to as usize;
	}

	return steps.to_string()
}

pub fn part1(input: String) -> String {
	return solve(input, false);
}

pub fn part2(input: String) -> String {
	return solve(input, true);
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 05,
	input: "file:05-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("5", "file:05-input-test"),
	],
	tests_part2: &[
		("10", "file:05-input-test"),
	],
};

