use crate::aoc;
use std::collections::HashMap;

// works fine but slow:
// ~10sec per run without compiler optimizations and ~0.5sec with --release.

type Coord = (i32, i32);
type NodeList = HashMap<Coord, State>;

enum State {
	Clean,
	Weakened,
	Infected,
	Flagged,
}

const TURN_TABLE: &'static [Coord] = &[
	// sequence of right turns
	( 0, -1), // up
	( 1,  0), // right
	( 0,  1), // down
	(-1,  0), // left
];

fn sporifica(infected_nodes: &mut NodeList, bursts: i32, is_part2: bool) -> i32 {
	let mut infectious_bursts = 0;
	let mut carrier: Coord = (0, 0);
	let mut direction = (0, -1); // start facing up

	for _ in 0..bursts {
		let node_state = infected_nodes.get(&carrier).unwrap_or(&State::Clean);
		match node_state {
			State::Clean => {
				direction = turn_right_n(direction, 3);
				if is_part2 {
					infected_nodes.insert(carrier, State::Weakened);
				} else {
					infected_nodes.insert(carrier, State::Infected);
					infectious_bursts += 1;
				}
			},
			State::Infected => {
				direction = turn_right_n(direction, 1);
				infected_nodes.insert(carrier, if is_part2 { State::Flagged } else { State::Clean });
			},
			// n.b.: states Weakened and Flagged only occur in part 2
			State::Weakened => {
				// no change of direction
				infected_nodes.insert(carrier, State::Infected);
				infectious_bursts += 1;
			},
			State::Flagged => {
				direction = turn_right_n(direction, 2);
				infected_nodes.insert(carrier, State::Clean);
			},
		};

		let (dx, dy) = direction;
		let (cx, cy) = carrier;
		carrier = (cx + dx, cy + dy);
	}

	println!("entries: {}", infected_nodes.len());
	return infectious_bursts
}

fn turn_right_n(old: Coord, times: i32) -> Coord {
	for i in 0..4 {
		if TURN_TABLE[i] == old {
			return TURN_TABLE[(i + times as usize) % 4];
		}
	}

	panic!("unreach: {:?}", old);
}

fn parse(input: String) -> NodeList {
	let mut r: NodeList = HashMap::with_capacity(1_000_000);

	let size = input.split('\n').nth(0).unwrap().len() as i32;
	let displace = size/2;

	for (y, line) in input.split('\n').enumerate() {
		for (x, char) in line.chars().enumerate() {
			if char == '#' {
				r.insert((x as i32 - displace, y as i32 - displace), State::Infected);
			}
		}
	}

	return r
}

pub fn part1(input: String) -> String {
	let mut infected_nodes = parse(input);
	let bursts = sporifica(&mut infected_nodes, 10_000, false);
	return bursts.to_string()
}

pub fn part2(input: String) -> String {
	let mut infected_nodes = parse(input);
	let bursts = sporifica(&mut infected_nodes, 10_000_000, true);
	return bursts.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 22,
	input: "file:22-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("5587", "file:22-input-test"),
	],
	tests_part2: &[
		("2511944", "file:22-input-test"),
	],
};

