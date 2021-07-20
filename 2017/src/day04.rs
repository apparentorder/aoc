use crate::aoc;
use std::collections::HashSet;

pub fn solve(input: String, check_anagram: bool) -> String {
	let mut valid_phrases = 0;

	'next_line: for line in input.split('\n') {
		let mut words: HashSet<&str> = HashSet::new();

		for candidate_word in line.split_whitespace() {
			if words.contains(candidate_word) {
				// duplicates are invalid
				continue 'next_line
			}

			for prev_word in &words {
				if check_anagram && is_anagram(&prev_word, candidate_word) {
					continue 'next_line
				}
			}

			words.insert(candidate_word);
		}

		valid_phrases += 1;
	}

	return valid_phrases.to_string();
}

fn is_anagram(w1: &str, w2: &str) -> bool {
	// we see an anagram when
	// - both words have the same length
	// - both words have the same counts of the same letters

	if w1.len() != w2.len() {
		return false
	}

	for char in w1.bytes() {
		let count_w1 = w1.bytes().filter(|w| w == &char).count();
		let count_w2 = w2.bytes().filter(|w| w == &char).count();

		if count_w1 != count_w2 {
			return false
		}
	}

	return true
}

pub fn part1(input: String) -> String {
	return solve(input, false);
}

pub fn part2(input: String) -> String {
	return solve(input, true);
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 04,
	input: "file:04-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("2", "file:04-input-test"),
	],
	tests_part2: &[
		("3", "file:04-input-test-part2"),
	],
};

