use crate::aoc;

pub fn part1(input: String) -> String {
	let ints: Vec<i32> = input.split(',').map(|s| s.parse::<i32>().unwrap()).collect();
	let mut cheapest = i32::MAX;

	for target_position in &ints {
		let fuel = ints.iter().fold(0, |sum, i| sum + (target_position - i).abs());

		cheapest = cheapest.min(fuel);
	}

	return cheapest.to_string()
}

pub fn part2(input: String) -> String {
	let ints: Vec<i32> = input.split(',').map(|s| s.parse::<i32>().unwrap()).collect();
	let mut cheapest = i32::MAX;

	for target_position in 1..=*ints.iter().max().unwrap() {
		let fuel = ints.iter().fold(0, |sum, i| sum + (1..=((target_position - i).abs())).fold(0, |isum, i| isum + i));

		cheapest = cheapest.min(fuel);
	}

	return cheapest.to_string()
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

