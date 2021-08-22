use crate::aoc;

fn parse(input: String, is_part2: bool) -> i32 {
	let mut level = 0;
	let mut score = 0;
	let mut ignore_once = false;
	let mut parsing_garbage = false;
	let mut garbage_removed = 0;

	for c in input.chars() {
		//println!("at c={} (i={} g={})", c, ignore_once, parsing_garbage);
		if ignore_once {
			ignore_once = false;
			continue
		}

		if parsing_garbage {
			match c {
				'>' => parsing_garbage = false,
				'!' => ignore_once = true,
				_ => garbage_removed += 1,
			};

			continue
		}

		match c {
			'{' => { level += 1; score += level; },
			'}' => { level -= 1; },
			'<' => parsing_garbage = true,
			',' => {}, // NOP
			_ => panic!("invalid character in non-garbage: {}", c),
		};
	}

	assert!(level == 0, "not back at level 0 after parsing");

	return if is_part2 { garbage_removed } else { score }
}

pub fn part1(input: String) -> String {
	return parse(input, false).to_string();
}

pub fn part2(input: String) -> String {
	return parse(input, true).to_string();
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 09,
	input: "file:09-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("1", "{}"),
		("6", "{{{}}}"),
		("5", "{{},{}}"),
		("16", "{{{},{},{{}}}}"),
		("1", "{<a>,<a>,<a>,<a>}"),
		("9", "{{<ab>},{<ab>},{<ab>},{<ab>}}"),
		("9", "{{<!!>},{<!!>},{<!!>},{<!!>}}"),
		("3", "{{<a!>},{<a!>},{<a!>},{<ab>}}"),
	],
	tests_part2: &[
		("0", "<>"),
		("17", "<random characters>"),
		("3", "<<<<>"),
		("2", "<{!>}>"),
		("0", "<!!>"),
		("0", "<!!!>>"),
		("10", "<{o\"i!a,<{i<a>"),
	],
};

