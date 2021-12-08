use crate::aoc;
use std::collections::HashSet;

type Segments = HashSet<char>;

struct Note {
	patterns: Vec<Segments>,
	outputs: Vec<Segments>,
}

fn decode(note: &Note) -> i32 {
	let mut segments: Vec<Segments> = vec![HashSet::new(); 10];

	// unique length
	segments[1] = match_pattern(&note.patterns, |p| p.len() == 2);
	segments[4] = match_pattern(&note.patterns, |p| p.len() == 4);
	segments[7] = match_pattern(&note.patterns, |p| p.len() == 3);
	segments[8] = match_pattern(&note.patterns, |p| p.len() == 7);

	// length 6
	segments[9] = match_pattern(&note.patterns, |p| p.len() == 6 && p.is_superset(&segments[4]));
	segments[0] = match_pattern(&note.patterns, |p| p.len() == 6 && p.is_superset(&segments[7]) && p != &segments[9]);
	segments[6] = match_pattern(&note.patterns, |p| p.len() == 6 && p != &segments[0] && p != &segments[9]);

	// length 5
	segments[3] = match_pattern(&note.patterns, |p| p.len() == 5 && p.is_superset(&segments[1]));
	segments[5] = match_pattern(&note.patterns, |p| p.len() == 5 && segments[6].is_superset(p) && p != &segments[3]);
	segments[2] = match_pattern(&note.patterns, |p| p.len() == 5 && p != &segments[5] && p != &segments[3]);

	let digits_str: String = note.outputs.iter()
		.map(|output| segments.iter().position(|segment| segment == output).unwrap() as u32)
		.map(|digit| char::from_digit(digit, 10).unwrap())
		.collect();

	return digits_str.parse().unwrap()
}

fn match_pattern<F>(patterns: &Vec<Segments>, filter: F) -> Segments
where F: Fn(&Segments) -> bool {
	let matches: Vec<Segments> = patterns.clone().into_iter().filter(&filter).collect();
	assert!(matches.len() == 1);
	return matches.iter().nth(0).unwrap().clone()
}

fn parse(input: String) -> Vec<Note> {
	let mut r: Vec<Note> = vec![];

	for line in input.lines() {
		let parts: Vec<String> = line.split(&[' ', '|'][..]).map(|s| s.to_string()).collect();

		let p: Vec<Segments> = parts[0..=9].iter().map(|p| p.chars().collect()).collect();
		let o: Vec<Segments> = parts[12..=15].iter().map(|o| o.chars().collect()).collect();

		r.push(Note { patterns: p, outputs: o });
	}

	return r
}

pub fn part1(input: String) -> String {
	let notes = parse(input);

	return notes
		.iter()
		.map(|note| note.outputs.iter().filter(|&o| [2,4,3,7].contains(&o.len())).count() as i32)
		.sum::<i32>()
		.to_string()
}

pub fn part2(input: String) -> String {
	let notes = parse(input);

	return notes
		.iter()
		.map(|n| decode(n))
		.sum::<i32>()
		.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 8,
	input: "file:08-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("26", "file:08-input-test"),
	],
	tests_part2: &[
		("5353", "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"),
		("61229", "file:08-input-test"),
	],
};

