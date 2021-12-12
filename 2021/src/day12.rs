use crate::aoc;
use std::collections::HashMap;

type CaveMap = HashMap<String, Vec<String>>;

fn find_paths(map: &CaveMap, path_so_far: Vec<String>, small_twice: bool) -> Vec<Vec<String>> {
	let mut paths: Vec<Vec<String>> = vec![];

	let start = path_so_far.last().unwrap();

	for other_cave in map.get(start).unwrap() {
		if !next_cave_is_valid(&path_so_far, other_cave.to_string(), small_twice) {
			continue
		}

		let mut this_psf = path_so_far.clone();
		this_psf.push(other_cave.clone());

		if other_cave == "end" {
			paths.push(this_psf);
			continue
		}

		paths.append(&mut find_paths(&map, this_psf, small_twice));
	}

	return paths
}

fn next_cave_is_valid(path_so_far: &Vec<String>, next_cave: String, small_twice: bool) -> bool {
	if next_cave == "start" {
		// never go back to start
		return false
	}

	if !next_cave.chars().nth(0).unwrap().is_lowercase() {
		// large (uppercase) caves are always ok
		return true
	}

	// small (lowercase) caves have special considerations

	// if this cave wasn't visited yet, we're good to go
	if !path_so_far.contains(&next_cave) {
		return true
	}

	// but if this cave was already visited, we cannot go there again, unless `small_twice`
	// small caves cannot be visited twice, unless `small_twice`
	if !small_twice {
		return false
	}

	// a small cave CAN be visited twice, if `small_twice`
	// AND no other small(!) cave has been visited twice before
	for cave_visited in path_so_far.iter().filter(|&c| c.chars().nth(0).unwrap().is_lowercase()) {
		if path_so_far.iter().filter(|&o| o == cave_visited).count() == 2 {
			//println!("twice {} in {:?}", cave_visited, path_so_far);
			return false
		}
	}

	return true
}

fn parse(input: String) -> CaveMap {
	let mut r: CaveMap = HashMap::new();

	for line in input.lines() {
		let caves: Vec<String> = line.split('-').map(|c| c.to_string()).collect();

		if let Some(a) = r.get(&caves[0]) {
			let mut new = a.clone();
			new.push(caves[1].clone());
			r.insert(caves[0].clone(), new.to_vec());
		} else {
			r.insert(caves[0].clone(), [caves[1].clone()].to_vec());
		}

		if let Some(b) = r.get(&caves[1]) {
			let mut new = b.clone();
			new.push(caves[0].clone());
			r.insert(caves[1].clone(), new.to_vec());
		} else {
			r.insert(caves[1].clone(), [caves[0].clone()].to_vec());
		}
	}

	return r
}

pub fn part1(input: String) -> String {
	let map = parse(input);
	let paths = find_paths(&map, ["start".to_string()].to_vec(), false);
	return paths.len().to_string()
}

pub fn part2(input: String) -> String {
	let map = parse(input);
	let paths = find_paths(&map, ["start".to_string()].to_vec(), true);
	return paths.len().to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 12,
	input: "file:12-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("10", "file:12-input-test"),
		("19", "file:12-input-test2"),
		("226", "file:12-input-test3"),
	],
	tests_part2: &[
		("36", "file:12-input-test"),
		("103", "file:12-input-test2"),
		("3509", "file:12-input-test3"),
	],
};

