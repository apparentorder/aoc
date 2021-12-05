use crate::aoc;
use std::collections::HashMap;

type Grid = HashMap<(i32, i32), i32>;

fn map_vents(input: String, skip_diagonal: bool) -> Grid {
	let mut grid: Grid = HashMap::new();

	for line in input.split('\n') {
		let mut parts = line.split_whitespace();

		let mut coord1 = parts.next().unwrap().split(',');
		let x1: i32 = coord1.next().unwrap().parse().unwrap();
		let y1: i32 = coord1.next().unwrap().parse().unwrap();

		let _arrow = parts.next().unwrap(); // drop `->`

		let mut coord2 = parts.next().unwrap().split(',');
		let x2: i32 = coord2.next().unwrap().parse().unwrap();
		let y2: i32 = coord2.next().unwrap().parse().unwrap();

		if skip_diagonal && (x1 != x2 && y1 != y2) {
			continue
		}

		let move_x = if x1 == x2 { 0 } else if x1 > x2 { -1 } else { 1 };
		let move_y = if y1 == y2 { 0 } else if y1 > y2 { -1 } else { 1 };

		let mut current_x = x1;
		let mut current_y = y1;

		// if both x and y move, it will be strictly diagonal (both distances will be the same)
		loop {
			grid.insert((current_x, current_y), *grid.get(&(current_x, current_y)).unwrap_or(&0) + 1);

			if current_x == x2 && current_y == y2 {
				break
			}

			current_x += move_x;
			current_y += move_y;
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

