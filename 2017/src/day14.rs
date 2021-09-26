use crate::aoc;
use crate::day10;

pub fn part1(input: String) -> String {
	let mut count = 0;

	for row in 0..128 {
		let hash_input = input.to_string() + "-" + &row.to_string();
		let hash = day10::part2(hash_input);
		let n = u128::from_str_radix(&hash, 16).unwrap();

		count += (0..128).filter(|b| n&(1<<b) == 1<<b).count();

		if false {
			for i in (0..128).rev() {
				print!("{}", if n&(1<<i)==1<<i { "#" } else { "." });
			}
			println!();
		}
	}

	return count.to_string();
}

fn nuke_group(grid: &mut Vec<Vec<bool>>, x: usize, y: usize) {
	if !grid[y][x] {
		return
	}

	grid[y][x] = false;

	if x > 0   { nuke_group(grid, x - 1, y    ) };
	if x < 127 { nuke_group(grid, x + 1, y    ) };
	if y > 0   { nuke_group(grid, x    , y - 1) };
	if y < 127 { nuke_group(grid, x    , y + 1) };
}

pub fn part2(input: String) -> String {
	let mut grid: Vec<Vec<bool>> = vec![vec![false; 128]; 128];

	for row in 0..128 {
		let hash_input = input.to_string() + "-" + &row.to_string();
		let hash = day10::part2(hash_input);
		let n = u128::from_str_radix(&hash, 16).unwrap();

		for i in 0..128 {
			if n & 1<<i == 1<<i {
				grid[row][i] = true;
			}
		}
	}

	let mut groups = 0;

	for x in 0..128 {
		for y in 0..128 {
			if grid[y][x] {
				nuke_group(&mut grid, x, y);
				groups += 1;
			}
		}
	}

	return groups.to_string();
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 14,
	input: "vbqugkhl",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("8108", "flqrgnkx"),
	],
	tests_part2: &[
		("1242", "flqrgnkx"),
	],
};

