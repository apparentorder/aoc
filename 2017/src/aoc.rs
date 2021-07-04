use crate::*;

#[derive(Eq, PartialEq, Debug)]
pub enum PuzzlePart {
	Part1,
	Part2,
}

pub struct Puzzle {
	pub day: u8,
	pub input: &'static str,
	pub implementation_part1: fn(String) -> String,
	pub implementation_part2: fn(String) -> String,
	pub tests_part1: &'static [(&'static str, &'static str)],
	pub tests_part2: &'static [(&'static str, &'static str)],
}

impl PartialEq for Puzzle {
	fn eq(&self, other: &Self) -> bool {
		return self.day == other.day
	}
}

pub fn run_puzzles_from_args() {
	let args: Vec<String> = std::env::args().collect();

	if args.len() == 1 {
		for p in aocdata::PUZZLES {
			run_puzzle(&p, None);
		}
		return
	} else if args.len() > 2 {
		eprintln!("too many arguments");
		std::process::exit(64);
	}

	let parts: Vec<&str> = args[1].split('.').collect();

	let day: u8;
	let mut limit_part: Option<&PuzzlePart> = None;

	match parts.len() {
		1 => { day = args[1].parse().unwrap(); }
		2 => {
			day = parts[0].parse().unwrap();

			match parts[1] {
				"1" => limit_part = Some(&PuzzlePart::Part1),
				"2" => limit_part = Some(&PuzzlePart::Part2),
				_ => {
					eprintln!("invalid argument: {}", &args[1]);
					std::process::exit(69);
				},
			}
		}
		_ => {
			eprintln!("invalid argument: {}", &args[1]);
			std::process::exit(65);
		}
	}

	for pm in aocdata::PUZZLES {
		if pm.day == day {
			run_puzzle(&pm, limit_part);
		}
	}
}

fn resolve_input(s: &str) -> String {
	return match s.strip_prefix("file:") {
		Some(x) => std::fs::read_to_string("Data/".to_owned() + x).unwrap().trim().to_string(),
		None => String::from(s),
	}
}

pub fn run_puzzle(pm: &Puzzle, limit_part: Option<&PuzzlePart>) {
	if limit_part == None || limit_part.unwrap() == &PuzzlePart::Part1 {
		run_puzzle_part(pm, &PuzzlePart::Part1);
	}

	if limit_part == None || limit_part.unwrap() == &PuzzlePart::Part2 {
		run_puzzle_part(pm, &PuzzlePart::Part2);
	}
}

pub fn run_puzzle_part(pm: &Puzzle, part: &PuzzlePart) {
	let implementation = match part {
		PuzzlePart::Part1 => pm.implementation_part1,
		PuzzlePart::Part2 => pm.implementation_part2,
	};

	let tests = match part {
		PuzzlePart::Part1 => pm.tests_part1,
		PuzzlePart::Part2 => pm.tests_part2,
	};

	for (expected_result, input) in tests {
		println!("Day {} {:?}: Running test({}) ...", pm.day, part, expected_result);

		let r = (implementation)(resolve_input(input));

		if r != expected_result.to_string() {
			eprintln!("TEST FAILED for day {} {:?}", pm.day, part);
			eprintln!("Expected result: {}", expected_result);
			eprintln!("Actual result:   {}", r);
			std::process::exit(1);
		}
	}

	println!("Day {} {:?}: Running puzzle ...", pm.day, part);
	let r = (implementation)(resolve_input(pm.input));
	println!("Day {} {:?}: RESULT: {}", pm.day, part, r);
	println!("");
}

