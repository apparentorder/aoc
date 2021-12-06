use crate::aoc;

fn model(input: String, days: i32) -> Vec<i64> {
	let fishs: Vec<i64> = input.split(',').map(|s| s.parse().unwrap()).collect();
	let mut counts: Vec<i64> = (0..=8).map(|i| fishs.iter().filter(|&f| i == *f).count() as i64).collect();

	for _ in 0..days {
		let spawns = counts[0];
		for i in 0..=7 {
			counts[i] = counts[i + 1];
		}
		counts[6] += spawns;
		counts[8] = spawns;
	}

	//println!("counts {:?}", counts);
	return counts
}

pub fn part1(input: String) -> String {
	return model(input, 80).iter().sum::<i64>().to_string()
}

pub fn part2(input: String) -> String {
	return model(input, 256).iter().sum::<i64>().to_string()
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

