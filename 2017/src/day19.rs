use crate::aoc;

// NOTE: for easier bounds testing, make sure that the input has a border of at least one
// space character (except for the starting position). the puzzle inputs are actually provided
// that way, but it might get lost when copying the input.

type Coord = (usize, usize);
type Grid = Vec<Vec<char>>;

fn trace(grid: &Grid, start: Coord) -> (String, i32) {
	let mut r: Vec<char> = vec![];

	let (mut x, mut y) = start;

	let mut steps = 0;
	let mut step_x: i32 = 0;
	let mut step_y: i32 = 1; // start moving downwards

	loop {
		//println!("at ({}, {}) = '{}'", x, y, grid[y][x]);
		match grid[y][x] {
			'|' | '-' => {
				// NOP (keep going)
			},
			'+' => {
				// toggle horizontal/vertical movement
				if step_x != 0 {
					step_x = 0;
					step_y = if grid[y - 1][x] != ' ' { -1 } else { 1 };
				} else /* step_y != 0 */ {
					step_y = 0;
					step_x = if grid[y][x - 1] != ' ' { -1 } else { 1 };
				}
			},
			' ' => {
				// hitting a space means we're done
				return (r.iter().collect(), steps)
			},
			_ => {
				// record letter, keep going
				r.push(grid[y][x])
			},
		}

		x = (x as i32 + step_x) as usize;
		y = (y as i32 + step_y) as usize;
		steps += 1;
	}
}

fn parse(input: String) -> (Grid, Coord) {
	let mut r: Grid = vec![];
	let mut start: Coord = (0, 0);

	for (y, line) in input.split('\n').enumerate() {
		r.push(vec![]);

		for (x, char) in line.chars().enumerate() {
			//println!("({}, {}) = '{}'", x, y, char);
			r[y].push(char);

			if y == 0 && char != ' ' {
				start = (x, y);
			}
		}
	}

	assert!(start != (0, 0), "no starting point");

	return (r, start)
}

pub fn part1(input: String) -> String {
	let (grid, start) = parse(input);
	let (letters, _) = trace(&grid, start);
	return letters
}

pub fn part2(input: String) -> String {
	let (grid, start) = parse(input);
	let (_, steps) = trace(&grid, start);
	return steps.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 19,
	input: "file:19-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("ABCDEF", "file:19-input-test"),
	],
	tests_part2: &[
		("38", "file:19-input-test"),
	],
};

