use crate::aoc;

fn fishs_after_days(days: i64) -> Vec<i64> {
	// returns a vec indicating how many fishs there will be after `days` days, from a single initial fish,
	// for each possible initial state (reflected by the vec's index)

	let mut fishs = vec![];
	let mut fishs_after_days = vec![];

	for initial_state in 0..7 {
		fishs.clear();
		fishs.push(initial_state);

		for _ in 0..days {
			for i in 0..fishs.len() {
				if fishs[i] == 0 {
					fishs[i] = 6;
					fishs.push(8);
				} else {
					fishs[i] -= 1;
				}
			}
		}

		fishs_after_days.push(fishs.len() as i64);
		println!("initial state {} after {} days: {}", initial_state, days, fishs.len());
	}

	return fishs_after_days
}

fn model(fishs: &mut Vec<i64>, days: i64) -> i64 {
	let fish_table = fishs_after_days(days);

	return fishs.iter().map(|&f| fish_table[f as usize]).sum()
}

pub fn part1(input: String) -> String {
	let mut fishs = input.split(',').map(|i| i.parse::<i64>().unwrap()).collect();
	return model(&mut fishs, 80).to_string()
}

pub fn part2(input: String) -> String {
	let mut fishs = input.split(',').map(|i| i.parse::<i64>().unwrap()).collect();
	return model(&mut fishs, 256).to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 6,
	input: "file:06-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("5934", "3,4,3,1,2"),
	],
	tests_part2: &[
		("26984457539", "3,4,3,1,2"),
	],
};

