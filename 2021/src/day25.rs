use crate::aoc;
use std::collections::HashMap;

type Direction = char;
type CucumberMap = Vec<Vec<Direction>>;

struct SeaFloor {
	x_max: usize,
	y_max: usize,
	cucumbers: CucumberMap,
}

impl SeaFloor {
	fn from_str(input: &str) -> SeaFloor {
		let x_max = input.lines().nth(0).unwrap().len() - 1;
		let y_max = input.lines().count() - 1;
		let cucumbers = input.lines().map(|line| line.chars().collect()).collect();
		return SeaFloor { x_max, y_max, cucumbers }
	}

	fn move_cucumbers(&mut self, dir: Direction) -> i32 {
		let mut new_map = self.cucumbers.clone();
		let mut movements = 0;

		for (y, row) in self.cucumbers.iter().enumerate() {
			for (x, &c) in row.iter().enumerate() {
				if c == dir {
					let (next_x, next_y) = match c {
						'>'  => ((x + 1) % (self.x_max + 1), y),
						'v' => (x, (y + 1) % (self.y_max + 1)),
						_ => panic!(),
					};

					if self.cucumbers[next_y][next_x] == '.' {
						movements += 1;
						new_map[y][x] = '.';
						new_map[next_y][next_x] = c;
					}
				}
			}
		}

		self.cucumbers = new_map;
		return movements
	}
}

impl std::fmt::Debug for SeaFloor {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		let mut s = self
			.cucumbers
			.iter()
			.map(|row| row.iter().collect::<String>())
			.collect::<Vec<_>>()
			.join("\n");

		s.push_str("\n");
		return write!(f, "{}", s)
	}
}

pub fn part1(input: String) -> String {
	let mut floor = SeaFloor::from_str(&input);
	let mut steps = 0;

	loop {
		let mut movements = 0;
		movements += floor.move_cucumbers('>');
		movements += floor.move_cucumbers('v');
		steps += 1;

		//println!("after {}", steps);
		//println!("{:?}", floor);

		if movements == 0 {
			break
		}
	}

	return steps.to_string()
}

pub fn part2(input: String) -> String {
	let _ = input;
	return 50.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 25,
	input: "file:25-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("58", "file:25-input-test"),
	],
	tests_part2: &[
	],
};

