use crate::aoc;
use std::collections::HashMap;

type Grid = HashMap<(i32, i32), i32>;

fn map_vents(input: String, skip_diagonal: bool) -> Grid {
	let mut grid: Grid = HashMap::new();

	for line in input.lines() {
		let ints: Vec<i32> = line
			.split(&[',', ' '][..])
			.filter_map(|s| s.parse().ok())
			.collect();

		let (x1, y1) = (ints[0], ints[1]);
		let (x2, y2) = (ints[2], ints[3]);

		if skip_diagonal && (x1 != x2 && y1 != y2) {
			continue
		}

		let (move_x, move_y) = ((x2 - x1).signum(), (y2 - y1).signum());

		// if both x and y move, it will be strictly diagonal (both distances will be the same)
		let (mut x, mut y) = (x1, y1);
		loop {
			grid.insert((x, y), *grid.get(&(x, y)).unwrap_or(&0) + 1);

			if x == x2 && y == y2 {
				break
			}

			x += move_x;
			y += move_y;
		}
	}

	return grid
}

pub fn part1(input: String) -> String {
	let grid = map_vents(input, true);
	return grid.values().filter(|&v| v > &1).count().to_string();
}

pub fn part2(input: String) -> String {
	let grid = map_vents(input, false);
	return grid.values().filter(|&v| v > &1).count().to_string();
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 5,
	input: "file:05-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("5", "file:05-input-test"),
	],
	tests_part2: &[
	],
};

