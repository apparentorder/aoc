use crate::aoc;

fn dance(input: String, program_count: usize, dance_count: u64) -> String {
	// init `r` with chars starting from 'a' (ascii 97)
	let mut r: Vec<char> = (0..program_count).map(|i| (97u8 + i as u8) as char).collect();

	// save initial state of `r` for loop detection
	let initial_state = r.to_vec();

	let mut spin = 0;

	let mut iteration: u64 = 0;
	while iteration < dance_count {
		if r == initial_state && iteration > 0 {
			println!("repeat at {}", iteration);

			// loop detected; jump ahead as many iterations as possible
			let remaining = dance_count - iteration;
			iteration += iteration * (remaining/iteration);
		}

		iteration += 1;

		for mut instruction in input.split(",") {
			//println!("r={:?} next={}", r, instruction);

			let action = instruction.chars().nth(0).unwrap();
			instruction = &instruction[1..];

			assert!(['s', 'p', 'x'].contains(&action));

			if action == 's' { // spin
				let new_spin: usize = instruction.parse().unwrap();
				spin = (spin + program_count - new_spin) % program_count;
				continue
			}

			let mut swap_a: usize = 0;
			let mut swap_b: usize = 0;

			if action == 'x' { // exchange (swap by index)
				let mut positions = instruction.split("/");
				swap_a = positions.next().unwrap().parse().unwrap();
				swap_b = positions.next().unwrap().parse().unwrap();

				// adjust according to current spin
				swap_a = (swap_a + spin) % program_count;
				swap_b = (swap_b + spin) % program_count;
			}

			if action == 'p' { // partner (swap by program name)
				let mut programs = instruction.split("/");
				let program_a = programs.next().unwrap().chars().nth(0).unwrap();
				let program_b = programs.next().unwrap().chars().nth(0).unwrap();

				swap_a = r.iter().position(|&p| p == program_a).unwrap();
				swap_b = r.iter().position(|&p| p == program_b).unwrap();
			}

			let swap_x = r[swap_b];
			r[swap_b] = r[swap_a];
			r[swap_a] = swap_x;
		}
	}

	// re-order according to spin
	let r_spun = (0..program_count).map(|i| r[(i + spin) % program_count]).collect();

	return r_spun
}

pub fn part1(input: String) -> String {
	let program_count = if input.len() < 100 { 5 } else { 16 };
	let dance_count = 1;

	return dance(input, program_count, dance_count)
}

pub fn part2(input: String) -> String {
	let program_count = if input.len() < 100 { 5 } else { 16 };
	let dance_count = if input.len() < 100 { 2 } else { 1_000_000_000 };

	return dance(input, program_count, dance_count)
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 16,
	input: "file:16-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("baedc", "s1,x3/4,pe/b"),
	],
	tests_part2: &[
		("ceadb", "s1,x3/4,pe/b"),
	],
};

