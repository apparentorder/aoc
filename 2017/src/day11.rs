use crate::aoc;
use std::cmp::{min,max};

fn distance(pos_x: i32, pos_y: i32) -> i32 {
	let distance_x = pos_x.abs();
	let distance_y = pos_y.abs();

	// move diagonally as much as possible: one step means moving one position on both the x and the y axis
	let mut steps = min(distance_x, distance_y);

	if distance_x > distance_y {
		// each x-axis movement is two steps (e.g. ne+se to end up on the same x again)
		steps += (distance_x - distance_y) * 2;
	} else {
		// each step along the y-axis is a grid movement of *2*
		let remaining_y = (distance_y - distance_x);
		steps += remaining_y / 2;
		steps += remaining_y % 2;
	}

	return steps
}

fn path_distance(input: String, is_part2: bool) -> i32 {
	let mut pos_x: i32 = 0;
	let mut pos_y: i32 = 0;
	let mut max_distance = 0;

	for step in input.split(",") {
		match step {
			"n" =>  {             pos_y += 2; },
			"ne" => { pos_x += 1; pos_y += 1; },
			"se" => { pos_x += 1; pos_y -= 1; },
			"s"  => {             pos_y -= 2; },
			"sw" => { pos_x -= 1; pos_y -= 1; },
			"nw" => { pos_x -= 1; pos_y += 1; },
			_ => { panic!("invalid step: {}", step); }
		}

		if is_part2 {
			max_distance = max(max_distance, distance(pos_x, pos_y));
		}
	}

	return if is_part2 { max_distance } else { distance(pos_x, pos_y) }
}

pub fn part1(input: String) -> String {
	return path_distance(input, false).to_string();
}

pub fn part2(input: String) -> String {
	return path_distance(input, true).to_string();
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 11,
	input: "file:11-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("3", "ne,ne,ne"),
		("0", "ne,ne,sw,sw"),
		("2", "ne,ne,s,s"),
		("3", "se,sw,se,sw,sw"),
	],
	tests_part2: &[
	],
};

