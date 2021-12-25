use crate::aoc;
use std::collections::HashMap;

type Coord = (i32, i32);
type CucumberMap = HashMap<Coord, Direction>;

struct SeaFloor {
	x_max: i32,
	y_max: i32,
	cucumbers: CucumberMap,
}

#[derive(Clone, PartialEq, Copy)]
enum Direction {
	East,
	South,
}

impl Direction {
	fn from_char(c: char) -> Option<Direction> {
		match c {
			'>' => Some(Direction::East),
			'v' => Some(Direction::South),
			_ => None
		}
	}

	fn to_char(&self) -> char {
		match self {
			Direction::East => '>',
			Direction::South => 'v',
		}
	}
}

impl SeaFloor {
	fn from_str(input: &str) -> SeaFloor {
		let mut map = CucumberMap::new();
		let x_max = input.lines().nth(0).unwrap().len() - 1;
		let y_max = input.lines().count() - 1;

		for (y, line) in input.lines().enumerate() {
			for (x, c) in line.chars().enumerate() {
				if let Some(dir) = Direction::from_char(c) {
					map.insert((x as i32, y as i32), dir);
				}
			}
		}

		return SeaFloor {
			x_max: x_max as i32,
			y_max: y_max as i32,
			cucumbers: map,
		}
	}

	fn move_cucumbers(&mut self, dir: Direction) -> i32 {
		let mut new_map = self.cucumbers.clone();
		let mut movements = 0;

		let cucus = self.cucumbers.iter().filter(|&c| c.1 == &dir);
		for (&pos, &dir) in cucus {
			let next_pos = self.next_pos(pos, dir);
			if !self.cucumbers.contains_key(&next_pos) {
				movements += 1;
				new_map.remove(&pos);
				new_map.insert(next_pos, dir);
			}
		}

		self.cucumbers = new_map;
		return movements
	}

	fn pos_char(&self, pos: Coord) -> char {
		if let Some(dir) = self.cucumbers.get(&pos) {
			return dir.to_char()
		}
		return '.'
	}

	fn next_pos(&self, pos: Coord, dir: Direction) -> Coord {
		match dir {
			Direction::East  => ((pos.0 + 1) % (self.x_max + 1), pos.1),
			Direction::South => (pos.0, (pos.1 + 1) % (self.y_max + 1)),
		}
	}
}

impl std::fmt::Debug for SeaFloor {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		let mut s = String::new();

		for y in 0..=self.y_max {
			s.push_str(&(0..=self.x_max).map(|x| self.pos_char((x,y))).collect::<String>());
			s.push_str(&"\n");
		}

		return write!(f, "{}", s)
	}
}

pub fn part1(input: String) -> String {
	let mut floor = SeaFloor::from_str(&input);
	let mut steps = 0;

	loop {
		let mut movements = 0;
		movements += floor.move_cucumbers(Direction::East);
		movements += floor.move_cucumbers(Direction::South);
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

