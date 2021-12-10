use crate::aoc;
use std::collections::HashMap;

fn parse(input: String) -> i64 {
	let mut depth: HashMap<char, i64> = HashMap::new();
	let mut illegals: HashMap<char, i64> = HashMap::new();
	let mut stack: Vec<char> = vec![];

	for line in input.lines() {
		for char in line.chars() {
			match char {
				'(' | '[' | '{' | '<' => {
					depth.insert(char, depth.get(&char).unwrap_or(&0) + 1);
					stack.push(char);
				},
				')' | ']' | '}' | '>' => {
					if stack.is_empty() {
						break; // ok for now
					}

					let expected_char = match stack.iter().last().unwrap() {
						'(' => ')',
						'[' => ']',
						'{' => '}',
						'<' => '>',
						_ => panic!(),
					};

					if expected_char != char {
						illegals.insert(char, illegals.get(&char).unwrap_or(&0) + 1);
						//println!("line {} char {} stack {:?}", line, char, stack);
						break;
					}
					depth.insert(char, depth.get(&char).unwrap_or(&0) - 1);
					stack.remove(stack.len() - 1);
				},
				_ => panic!(),
			}
		}
	}

	let mut score = 0;
	score += illegals.get(&')').unwrap_or(&0) * 3;
	score += illegals.get(&']').unwrap_or(&0) * 57;
	score += illegals.get(&'}').unwrap_or(&0) * 1197;
	score += illegals.get(&'>').unwrap_or(&0) * 25137;

	return score
}

fn parse2(input: String) -> i64 {
	let mut depth: HashMap<char, i64> = HashMap::new();
	let mut stack: Vec<char> = vec![];
	let mut scores: Vec<i64> = vec![];

	'line: for line in input.lines() {
		stack.clear();

		for char in line.chars() {
			match char {
				'(' | '[' | '{' | '<' => {
					depth.insert(char, depth.get(&char).unwrap_or(&0) + 1);
					stack.push(char);
				},
				')' | ']' | '}' | '>' => {
					let expected_char = match stack.iter().last().unwrap() {
						'(' => ')',
						'[' => ']',
						'{' => '}',
						'<' => '>',
						_ => panic!(),
					};

					if expected_char != char {
						// skip broken lines
						continue 'line
					}
					depth.insert(char, depth.get(&char).unwrap_or(&0) - 1);
					stack.remove(stack.len() - 1);
				},
				_ => panic!(),
			}
		}

		if !stack.is_empty() {
			stack.reverse();
			let mut closing: Vec<char> = vec![];
			for c in &stack {
				let closing_char = match c {
					'(' => ')',
					'[' => ']',
					'{' => '}',
					'<' => '>',
					_ => panic!(),
				};

				closing.push(closing_char);
			}

			println!("line {} closing {:?}", line, closing);

			let mut score = 0;
			for c in closing {
				score *= 5;
				score += match c {
					')' => 1,
					']' => 2,
					'}' => 3,
					'>' => 4,
					_ => panic!(),
				};
			}

			println!("score {}", score);
			scores.push(score);
		}
	}

	scores.sort();
	return scores[scores.len() / 2]
}

pub fn part1(input: String) -> String {
	return parse(input).to_string()
}

pub fn part2(input: String) -> String {
	return parse2(input).to_string()
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

