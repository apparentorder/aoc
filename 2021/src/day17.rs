use crate::aoc;

#[derive(Debug)]
struct Target {
	min_x: i32,
	max_x: i32,
	min_y: i32,
	max_y: i32,
}

fn try_all(target: &Target) -> (i32, i32) {
	let mut count = 0;
	let mut max_y = 0;

	let mut min_velocity_x = 0;
	while target.min_x >= (min_velocity_x * (min_velocity_x + 1) / 2) {
		min_velocity_x += 1;
	}

	let max_velocity_x = target.max_x;
	let min_velocity_y = target.min_y;
	let max_velocity_y = max_velocity_x;

	for vx in min_velocity_x..=max_velocity_x {
		for vy in min_velocity_y..=max_velocity_y {
			let (is_on_target, this_max_y) = shoot(target, vx, vy);

			max_y = max_y.max(this_max_y);

			if is_on_target {
				count += 1;
			}
		}
	}

	return (max_y, count)
}

fn shoot(target: &Target, velocity_x: i32, velocity_y: i32) -> (bool, i32) {
	let mut position_x = 0;
	let mut position_y = 0;

	let mut velocity_x = velocity_x;
	let mut velocity_y = velocity_y;

	let mut max_y = 0;

	while position_x <= target.max_x && position_y >= target.min_y {
		position_x += velocity_x;
		position_y += velocity_y;

		velocity_x -= velocity_x.signum();
		velocity_y -= 1;

		max_y = max_y.max(position_y);

		let x_on_target = position_x >= target.min_x && position_x <= target.max_x;
		let y_on_target = position_y >= target.min_y && position_y <= target.max_y;
		if x_on_target && y_on_target {
			return (true, max_y)
		}
	}

	return (false, 0)
}

fn parse(input: &str) -> Target {
	let parts = input.split(&['=', '.', ','][..]).collect::<Vec<_>>();

	let min_x = parts[1].parse::<i32>().unwrap();
	let max_x = parts[3].parse::<i32>().unwrap();
	let min_y = parts[5].parse::<i32>().unwrap();
	let max_y = parts[7].parse::<i32>().unwrap();

	return Target { min_x, max_x, min_y, max_y }
}

pub fn part1(input: String) -> String {
	let target = parse(&input);
	let (max_y, _) = try_all(&target);
	return max_y.to_string()
}

pub fn part2(input: String) -> String {
	let target = parse(&input);
	let (_, count) = try_all(&target);
	return count.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 17,
	input: "target area: x=144..178, y=-100..-76",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("45", "target area: x=20..30, y=-10..-5"),
	],
	tests_part2: &[
		("112", "target area: x=20..30, y=-10..-5"),
	],
};

