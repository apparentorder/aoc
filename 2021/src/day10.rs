use crate::aoc;
use std::collections::HashMap;

fn parse(input: String) -> (i64, i64) {
	let closing_char = HashMap::from([
		('(', ')'),
		('[', ']'),
		('{', '}'),
		('<', '>')
	]);

	let mut score_illegal: i64 = 0;
	let mut scores_closing: Vec<i64> = vec![];

	'line: for line in input.lines() {
		let mut stack: Vec<char> = vec![];

		for char in line.chars() {
			match char {
				'(' | '[' | '{' | '<' => stack.push(char),
				')' | ']' | '}' | '>' => {
					let expected_char = closing_char.get(stack.iter().last().unwrap()).unwrap();

					if expected_char != &char {
						score_illegal += char_score(char, true);
						continue 'line // skip broken lines
					}
					stack.remove(stack.len() - 1);
				},
				_ => panic!(),
			}
		}

		stack.reverse();

		let score = stack.iter().fold(0, |score, &c| score*5 + char_score(*closing_char.get(&c).unwrap(), false));
		scores_closing.push(score);
	}

	scores_closing.sort();
	return (score_illegal, scores_closing[scores_closing.len() / 2])
}

fn char_score(c: char, illegal: bool) -> i64 {
	match c {
		')' => if illegal { 3     } else { 1 },
		']' => if illegal { 57    } else { 2 },
		'}' => if illegal { 1197  } else { 3 },
		'>' => if illegal { 25137 } else { 4 },
		_ => panic!(),
	}
}

pub fn part1(input: String) -> String {
	let (r, _) = parse(input);
	return r.to_string()
}

pub fn part2(input: String) -> String {
	let (_, r) = parse(input);
	return r.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 10,
	input: "file:10-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("26397", "file:10-input-test"),
	],
	tests_part2: &[
		("288957", "file:10-input-test"),
	],
};

