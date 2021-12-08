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
	segments[1] = note.patterns.clone().into_iter().filter(|o| o.len() == 2).nth(0).unwrap();
	segments[4] = note.patterns.clone().into_iter().filter(|o| o.len() == 4).nth(0).unwrap();
	segments[7] = note.patterns.clone().into_iter().filter(|o| o.len() == 3).nth(0).unwrap();
	segments[8] = note.patterns.clone().into_iter().filter(|o| o.len() == 7).nth(0).unwrap();

	// length 6
	segments[9] = note.patterns.clone().into_iter().filter(|o| o.len() == 6)
		.filter(|candidate| candidate.is_superset(&segments[4]))
		.nth(0).unwrap();

	segments[0] = note.patterns.clone().into_iter().filter(|o| o.len() == 6)
		.filter(|candidate| candidate.is_superset(&segments[7]) && *candidate != segments[9])
		.nth(0).unwrap();

	segments[6] = note.patterns.clone().into_iter().filter(|o| o.len() == 6)
		.filter(|candidate| *candidate != segments[0] && *candidate != segments[9])
		.nth(0).unwrap();

	// length 5
	segments[3] = note.patterns.clone().into_iter().filter(|o| o.len() == 5)
		.filter(|candidate| candidate.is_superset(&segments[1]))
		.nth(0).unwrap();

	segments[5] = note.patterns.clone().into_iter().filter(|o| o.len() == 5)
		.filter(|candidate| segments[6].is_superset(candidate) && *candidate != segments[3])
		.nth(0).unwrap();

	segments[2] = note.patterns.clone().into_iter().filter(|o| o.len() == 5)
		.filter(|candidate| *candidate != segments[5] && *candidate != segments[3])
		.nth(0).unwrap();

	let mut digits_str = "".to_string();
	for o in &note.outputs {
		let digit = segments.iter().position(|segment| segment == o).unwrap();
		digits_str.push_str(&digit.to_string());
	}

	return digits_str.parse().unwrap()
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

