use crate::aoc;
use std::collections::HashMap;

type Coord = (i32, i32);
type Algorithm = Vec<bool>;
type ImageData = HashMap<Coord, bool>;

#[derive(Clone)]
struct Image {
	default_is_active: bool,
	algorithm: Algorithm,
	data: ImageData,
}

impl Image {
	fn enhance(&mut self) {
		let mut new_image = self.clone();

		let (min_x, min_y) = self.pos_min();
		let (max_x, max_y) = self.pos_max();

		for y in (min_y-1)..=(max_y+1) {
			for x in (min_x-1)..=(max_x+1) {
				if self.enhanced_pixel_is_active((x,y)) {
					new_image.set((x,y));
				} else {
					new_image.clear((x,y));
				}
			}
		}

		if self.algorithm[0] {
			new_image.default_is_active = !self.default_is_active;
		}

		*self = new_image
	}

	fn enhanced_pixel_is_active(&self, pos: Coord) -> bool {
		let mut r = 0;
		for (rely, y) in ((pos.1-1)..=(pos.1+1)).enumerate() {
			for (relx, x) in ((pos.0-1)..=(pos.0+1)).enumerate() {
				let digit = 8 - (rely*3 + relx);
				if self.pixel_is_active((x,y)) {
					r |= 1<<digit;
				}
				//println!("{:?}, digit={} r={} pixel={}", (x,y), digit, r, pixel(image, (x,y)));
			}
		}

		//println!("algo input number {} for pos {:?}", r, pos);
		return self.algorithm[r]
	}

	fn _pixel(&self, pos: Coord) -> char {
		if self.pixel_is_active(pos) { '#' } else { '.' }
	}

	fn pixel_is_active(&self, c: Coord) -> bool {
		*self.data.get(&c).unwrap_or(&self.default_is_active)
	}

	fn count_lit(&self) -> i32 {
		self.data.values().filter(|&b| *b).count() as i32
	}

	fn set(&mut self, pos: Coord) {
		self.data.insert(pos, true);
	}

	fn clear(&mut self, pos: Coord) {
		self.data.insert(pos, false);
	}

	fn pos_min(&self) -> Coord {
		let min_x = self.data.keys().map(|p| p.0).min().unwrap();
		let min_y = self.data.keys().map(|p| p.1).min().unwrap();
		return (min_x, min_y);
	}

	fn pos_max(&self) -> Coord {
		let max_x = self.data.keys().map(|p| p.0).max().unwrap();
		let max_y = self.data.keys().map(|p| p.1).max().unwrap();
		return (max_x, max_y);
	}

	fn _print(&self) {
		let (min_x, min_y) = self.pos_min();
		let (max_x, max_y) = self.pos_max();

		for y in min_y..=max_y {
			println!("{}", (min_x..=max_x).map(|x| self._pixel((x, y))).collect::<String>());
		}

		println!();
	}

	fn from_input(input: &str) -> Image {
		let mut line_iter = input.lines();

		let algorithm = line_iter.next().unwrap().chars().map(|c| c == '#').collect::<Vec<_>>();
		let _empty_line = line_iter.next();

		let mut image = Image {
			default_is_active: false,
			algorithm,
			data: ImageData::new(),
		};

		for (y, line) in line_iter.enumerate() {
			for (x, char) in line.chars().enumerate() {
				if char == '#' {
					image.set((x as i32, y as i32));
				} else {
					image.clear((x as i32, y as i32));
				}
			}
		}

		return image
	}
}

pub fn part1(input: String) -> String {
	let mut image = Image::from_input(&input);

	for _ in 0..2 {
		image.enhance();
		//image._print();
	}

	return image.count_lit().to_string()
}

pub fn part2(input: String) -> String {
	let mut image = Image::from_input(&input);

	for _ in 0..50 {
		image.enhance();
	}

	//image.print();
	return image.count_lit().to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 20,
	input: "file:20-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("35", "file:20-input-test"),
	],
	tests_part2: &[
		("3351", "file:20-input-test"),
	],
};

