use crate::aoc;

fn crabmarines(starting_positions: Vec<i32>, is_part2: bool) -> i32 {
	let mut cheapest = i32::MAX;
	let max_position = starting_positions.iter().max().unwrap();

	let test_positions = if is_part2 { (1..=*max_position).collect() } else { starting_positions.clone() };

	'tp: for target_position in test_positions {
		let mut fuel = 0;
		for sp in &starting_positions {
			let distance = (target_position - sp).abs();
			fuel += if !is_part2 { distance } else { distance * (distance + 1) / 2 };

			if fuel > cheapest {
				continue 'tp
			}
		}

		cheapest = cheapest.min(fuel);
	}

	return cheapest
}

pub fn part1(input: String) -> String {
	let starting_positions: Vec<i32> = input.split(',').map(|s| s.parse().unwrap()).collect();
	return crabmarines(starting_positions, false).to_string()
}

pub fn part2(input: String) -> String {
	let starting_positions: Vec<i32> = input.split(',').map(|s| s.parse().unwrap()).collect();
	return crabmarines(starting_positions, true).to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 7,
	input: "file:07-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("37", "16,1,2,0,4,2,7,1,2,14"),
	],
	tests_part2: &[
		("168", "16,1,2,0,4,2,7,1,2,14"),
	],
};

