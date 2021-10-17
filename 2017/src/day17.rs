use crate::aoc;

fn spinlock(step_size: i32, insertions: i32) -> Vec<i32> {
	let mut buffer: Vec<i32> = Vec::with_capacity(insertions as usize + 1);

	let mut pos: usize = 0;
	buffer.push(0);

	for insert_value in 1..=insertions {
		pos += step_size as usize;
		pos %= insert_value as usize;
		pos += 1; // "The inserted value becomes the current position"

		buffer.insert(pos, insert_value);
	}

	return buffer
}

fn spinlock_after_zero(step_size: i32, insertions: i32) -> Result<i32, String> {
	let mut pos: usize = 0;
	let mut observed_value: Result<i32, String> = Err("Not found".to_string());
	let mut pos_of_zero = 0;

	for insert_value in 1..=insertions {
		pos += step_size as usize;
		pos %= insert_value as usize;
		pos += 1; // "The inserted value becomes the current position"

		if pos <= pos_of_zero {
			pos_of_zero += 1;
		} else if pos == pos_of_zero + 1 {
			observed_value = Ok(insert_value);
		}
	}

	return observed_value
}

pub fn part1(input: String) -> String {
	let steps: i32 = input.parse().unwrap();
	let final_value = 2017;
	let buffer = spinlock(steps, final_value);

	let pos_of_final_value = buffer.iter().position(|&v| v == final_value).unwrap();
	return buffer[pos_of_final_value + 1].to_string()
}

pub fn part2(input: String) -> String {
	let steps: i32 = input.parse().unwrap();
	let final_value = 50_000_000;
	return spinlock_after_zero(steps, final_value).unwrap().to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 17,
	input: "356",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("638", "3"),
	],
	tests_part2: &[
	],
};

