use crate::aoc;
use std::collections::HashMap;

// afterthought: all two-dimensional logic could be dropped and the whole thing could
// be built as one large string, without newlines, which should be significantly more efficient.
// in the end, each "enhance" operation is a simple string replacement (successively replace each
// two- or three-character sequence with the corresponding three- or four-character sequence,
// respectively). of course that only became clear once part 2 was known.

type Square = Vec<Vec<bool>>;
type RuleList = HashMap<Square, Square>;

// The program always begins with this pattern:
//     .#.
//     ..#
//     ###
const STARTING_PATTERN: &str = ".#./..#/###";

fn make_art(initial: Square, rules: RuleList, iterations: i32) -> Square {
	let mut grid = initial;

	for _ in 0..iterations {
		let grid_sub_size;
		let new_grid_sub_size;
		if grid.len() % 2 == 0 {
			// If the size is evenly divisible by 2, break the pixels up into 2x2 squares
			grid_sub_size = 2;
			// and convert each 2x2 square into a 3x3 square
			new_grid_sub_size = 3;
		} else {
			// Otherwise, the size is evenly divisible by 3; break the pixels up into 3x3 squares
			grid_sub_size = 3;
			// and convert each 3x3 square into a 4x4
			new_grid_sub_size = 4;
		}

		let new_grid_size = grid.len() / grid_sub_size * new_grid_sub_size;

		let mut new_grid: Square = vec![vec![false; new_grid_size]; new_grid_size];

		for sub_row in 0..(grid.len() / grid_sub_size) {
			for sub_col in 0..(grid.len() / grid_sub_size) {
				enhance(&rules, &grid, grid_sub_size, &mut new_grid, sub_row, sub_col);
			}
		}

		grid = new_grid;
		if false {
			print_square(&grid);
			println!();
		}
	}

	return grid
}

fn enhance(rules: &RuleList, grid: &Square, sub_size: usize, new_grid: &mut Square, sub_row: usize, sub_col: usize) {
	let mut lookup: Square = vec![vec![false; sub_size]; sub_size];
	for row in 0..sub_size {
		for col in 0..sub_size {
			lookup[row][col] = grid[sub_row * sub_size + row][sub_col * sub_size + col];
		}
	}

	let new_sub = rules.get(&lookup).unwrap();
	let new_sub_size = new_sub.len();
	for row in 0..new_sub_size {
		for col in 0..new_sub_size {
			new_grid[sub_row * new_sub_size + row][sub_col * new_sub_size + col] = new_sub[row][col];
		}
	}
}

fn print_square(s: &Square) {
	for row in s {
		for b in row {
			print!("{}", if *b { "#" } else { "." });
		}
		println!();
	}
}

fn parse_rules(input: String) -> RuleList {
	let mut r: RuleList = HashMap::new();

	for line in input.split('\n') {
		// input is "row1/row2/.../rowN => row1/row2/.../rowN"
		let mut parts = line.split_whitespace();

		let mut input_square = parse_rule_square(parts.next().unwrap());
		let _ = parts.next().unwrap(); // drop "=>"
		let output_square = parse_rule_square(parts.next().unwrap());

		let mut input_squares: Vec<Square> = vec![input_square.to_vec()];
		for _ in 0..3 {
			rotate(&mut input_square);
			input_squares.push(input_square.to_vec());
		}
		flip_vertical(&mut input_square);
		input_squares.push(input_square.to_vec());
		for _ in 0..3 {
			rotate(&mut input_square);
			input_squares.push(input_square.to_vec());
		}

		for i in input_squares {
			r.insert(i, output_square.to_vec());
		}
	}

	return r
}

fn flip_vertical(s: &mut Square) {
	let old = s.to_vec();

	for row in 0..old.len() {
		for col in 0..old.len() {
			s[row][col] = old[old.len() - row - 1][col];
		}
	}
}

fn rotate(s: &mut Square) {
	let old = s.to_vec();

	for row in 0..old.len() {
		for col in 0..old.len() {
			s[row][col] = old[old.len() - 1 - col][row];
		}
	}
}

fn parse_rule_square(input: &str) -> Square {
	let mut r: Square = vec![];

	for row_string in input.split('/') {
		let mut row: Vec<bool> = vec![];

		for char in row_string.chars() {
			let c = match char {
				'.' => false,
				'#' => true,
				_ => panic!("invalid char in rule"),
			};
			row.push(c);
		}

		r.push(row);
	}

	return r
}

pub fn part1(input: String) -> String {
	let starting_square = parse_rule_square(STARTING_PATTERN);
	let iterations = if input.len() < 200 { /* test */ 2 } else { 5 };

	let rules = parse_rules(input);
	let grid = make_art(starting_square, rules, iterations);

	let count = grid.iter().fold(0, |count, row| count + row.iter().filter(|&&b| b).count());
	return count.to_string()
}

pub fn part2(input: String) -> String {
	let starting_square = parse_rule_square(STARTING_PATTERN);
	let iterations = 18;

	let rules = parse_rules(input);
	let grid = make_art(starting_square, rules, iterations);

	let count = grid.iter().fold(0, |count, row| count + row.iter().filter(|&&b| b).count());
	return count.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 21,
	input: "file:21-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("12", "file:21-input-test"),
	],
	tests_part2: &[
	],
};

