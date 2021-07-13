use crate::aoc;
use std::collections::HashMap;

fn solve(input: String) -> String {
	let mut layer = 0;
	let mut sidelen = -1;
	let mut bottom_right = 1;

	let wanted: i32 = input.parse().unwrap();

	while bottom_right < wanted {
		layer += 1;
		sidelen = 1 + layer*2;
		bottom_right += sidelen * 4 - 4;
	}

	println!("wanted {} found layer {} sidelen {} bottomright {}", wanted, layer, sidelen, bottom_right);

	// distance is *at least* `layer` steps (straight line from `wanted` to `1`).
	// distance is increased by steps towards a corner, with the corner as the maximum distance:
	// `layer` + `sidelen/2`.

	let mut corner = bottom_right;
	while wanted < corner {
		corner -= sidelen - 1;
	}

	let additional_steps = (wanted - (corner + sidelen/2)).abs();

	return (layer + additional_steps).to_string();
}

pub fn part1(input: String) -> String {
	return solve(input);
}

// ----- part2 ---------------------------------------------------------

type Grid = HashMap<Coordinates, i32>;

#[derive(PartialEq, Eq, Hash, Clone)]
struct Coordinates {
	x: i32,
	y: i32,
}

fn fill_grid_position(grid: &mut Grid, position: &Coordinates) -> i32 {
	let adjacent_positions = [
		Coordinates { x: position.x + 1, y: position.y     }, // right
		Coordinates { x: position.x - 1, y: position.y     }, // left
		Coordinates { x: position.x    , y: position.y + 1 }, // below
		Coordinates { x: position.x    , y: position.y - 1 }, // above
		Coordinates { x: position.x + 1, y: position.y + 1 }, // lower-right
		Coordinates { x: position.x - 1, y: position.y + 1 }, // lower-left
		Coordinates { x: position.x + 1, y: position.y - 1 }, // upper-right
		Coordinates { x: position.x - 1, y: position.y - 1 }, // upper-left
	];

	let mut sum = 0;

	for ap in adjacent_positions {
		if let Some(value) = grid.get(&ap) {
			sum += value;
		}
	}

	grid.insert(position.clone(), sum);
	return sum
}

pub fn part2(input: String) -> String {
	let mut grid: Grid = HashMap::new();

	let mut position = Coordinates{x: 0, y: 0};
	let mut layer = 0;
	let mut bottom_right = 0;

	grid.insert(Coordinates{x: 0, y: 0}, 1);

	let input_number = input.parse().unwrap();

	while bottom_right < input_number {
		layer += 1;
		let sidelen = 1 + layer * 2;

		// step right from the previous box's bottom right corner
		position.x += 1;
		fill_grid_position(&mut grid, &position);

		// move up (sidelen-2) positions to the top right corner
		for _ in 0..(sidelen-2) {
			position.y -= 1;
			fill_grid_position(&mut grid, &position);
		}

		// move left (sidelen-1) positions to the top left corner
		for _ in 0..(sidelen-1) {
			position.x -= 1;
			fill_grid_position(&mut grid, &position);
		}

		// move down (sidelen-1) positions to the bottom left corner
		for _ in 0..(sidelen-1) {
			position.y += 1;
			fill_grid_position(&mut grid, &position);
		}

		// move right (sidelen-1) positions to the bottom right corner
		for _ in 0..(sidelen-1) {
			position.x += 1;
			bottom_right = fill_grid_position(&mut grid, &position);
		}

		println!("after layer {}: bottom right {}", layer, bottom_right);
	}

	let mut top_values: Vec<&i32> =  grid.values().filter(|v| v >= &&input_number).collect();
	top_values.sort();
	return top_values.first().unwrap().to_string();
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 03,
	input: "347991",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("0", "1"),
		("3", "12"),
		("2", "23"),
		("31", "1024"),
	],
	tests_part2: &[
	],
};

