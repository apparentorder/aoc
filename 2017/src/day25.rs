use crate::aoc;

// n.b.:
// blueprint.states's index corrensponds to the state's character ID from the input (e.g. state C == index 2)
// blueprint.states[n].actions's index corresponds to the value condition (e.g. actions[1] is to be used if the value is 1)

#[derive(Debug)]
struct Blueprint {
	begin_state: usize,
	checksum_after: i32,
	states: Vec<State>,
}

#[derive(Debug)]
struct State {
	actions: Vec<Action>,
}

#[derive(Debug)]
struct Action {
	write_value: u8,
	move_direction: i8,
	next_state: usize,
}

fn run(blueprint: Blueprint) -> i32 {
	let mut tape: Vec<u8> = vec![0; 100_000];
	let mut position = tape.len() / 2;
	let mut current_state: usize = blueprint.begin_state;

	for _ in 0..blueprint.checksum_after {
		let action: &Action = &blueprint.states[current_state].actions[tape[position] as usize];

		tape[position] = action.write_value;
		position = (position as i32 - action.move_direction as i32) as usize;
		current_state = action.next_state;
	}

	return tape.iter().fold(0, |sum, &v| sum + v as i32)
}

fn parse(input: String) -> Blueprint {
	let mut states: Vec<State> = vec![];

	let mut line_iter = input.split('\n');

	// Begin in state A.
	let line_begin = line_iter.next().unwrap();
	let begin_state_char = line_begin.chars().rev().nth(1).unwrap();
	let begin_state = begin_state_char as usize - 65;

	// Perform a diagnostic checksum after 12656374 steps.
	let line_checksum = line_iter.next().unwrap();
	let checksum_after: i32 = line_checksum.split_whitespace().nth(5).unwrap().parse().unwrap();

	while let Some(_empty_line) = line_iter.next() {
		let mut actions: Vec<Action> = vec![];

		// In state A:
		let line_state = line_iter.next().unwrap();
		let state_id = line_state.chars().rev().nth(1).unwrap() as usize - 65;
		assert!(state_id == states.len(), "states in input are not sorted");

		// read two blocks of "If the current value is X:"
		for _ in 0..2 {
			let write_value: u8;
			let move_direction;
			let next_state;

			//   If the current value is 0:
			let line_value = line_iter.next().unwrap();
			let if_value = line_value.chars().rev().nth(1).unwrap() as u8 - 48; // char '0' or char '1'
			assert!(if_value == actions.len() as u8, "if_values in input are not sorted");

			//     - Write the value 1.
			let line_write = line_iter.next().unwrap();
			assert!(line_write.find("Write") != None, "input in unexpected order");
			write_value = line_write.chars().rev().nth(1).unwrap() as u8 - 48; // char '0' or char '1'

			//     - Move one slot to the left.
			let line_move = line_iter.next().unwrap();
			assert!(line_move.find("Move") != None, "input in unexpected order");
			move_direction = if line_move.find("left") != None { -1 } else { 1 };

			//     - Continue with state A.
			let line_next_state = line_iter.next().unwrap();
			assert!(line_next_state.find("Continue") != None, "input in unexpected order");
			next_state = line_next_state.chars().rev().nth(1).unwrap() as usize - 65; // char '0' or char '1'

			actions.push(Action {
				write_value: write_value,
				move_direction: move_direction,
				next_state: next_state,
			});
		}

		states.push(State { actions: actions });
	}

	return Blueprint {
		begin_state: begin_state,
		checksum_after: checksum_after,
		states: states,
	}
}

pub fn part1(input: String) -> String {
	let blueprint = parse(input);
	return run(blueprint).to_string();
}

pub fn part2(_no_part_2: String) -> String {
	return 0.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 25,
	input: "file:25-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("3", "file:25-input-test"),
	],
	tests_part2: &[
	],
};

