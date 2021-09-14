use crate::aoc;
use std::collections::HashSet;
use std::collections::HashMap;

type ProgramConnections = HashMap<i32, Vec<i32>>;

fn group_count(connections: &ProgramConnections) -> i32 {
	let mut remaining_programs: Vec<i32> = connections.keys().cloned().collect();
	let mut group_count: i32 = 0;

	while let Some(start) = remaining_programs.pop() {
		let group_members = reachable_programs(&connections, start);
		remaining_programs.retain(|p| !group_members.contains(p));

		group_count += 1;
	}

	return group_count
}

fn reachable_programs(connections: &ProgramConnections, starting_at: i32) -> HashSet<i32> {
	let mut destinations: HashSet<i32> = HashSet::new();
	let mut to_check: Vec<i32> = connections[&starting_at].to_vec();

	while let Some(n) = to_check.pop() {
		if destinations.contains(&n) {
			// already explored
			continue
		}

		destinations.insert(n);
		to_check.append(&mut connections[&n].to_vec())
	}

	return destinations
}

fn parse(input: String) -> ProgramConnections {
	let mut r: ProgramConnections = HashMap::new();

	for line in input.split('\n') {
		let mut destinations: Vec<i32> = vec![];

		let mut parts = line.split_whitespace();

		let from: i32 = parts.next().unwrap().parse().unwrap();
		let _ = parts.next(); // drop "<->"

		while let Some(dest_str) = parts.next() {
			let mut dest_string = dest_str.to_string();
			dest_string.retain(|c| c != ',');
			let dest: i32 = dest_string.parse().unwrap();
			destinations.push(dest);
		}

		r.insert(from, destinations);
	}

	return r
}

pub fn part1(input: String) -> String {
	let connections = parse(input);
	return reachable_programs(&connections, 0).len().to_string()
}

pub fn part2(input: String) -> String {
	let connections = parse(input);
	return group_count(&connections).to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 12,
	input: "file:12-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("6", "file:12-input-test"),
	],
	tests_part2: &[
		("2", "file:12-input-test"),
	],
};

