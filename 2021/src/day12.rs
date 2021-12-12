use crate::aoc;
use std::collections::HashMap;

type CaveMap = HashMap<String, Vec<String>>;

fn find_paths(map: &CaveMap, path_so_far: Vec<String>, small_twice: bool) -> Vec<Vec<String>> {
	let mut paths: Vec<Vec<String>> = vec![];

	let start = path_so_far.last().unwrap();

	for other_cave in map.get(start).unwrap() {
		if other_cave == "start" {
			continue
		}

		let mut small_visited_twice = false;
		for cave_visited in path_so_far.iter().filter(|&c| c.chars().nth(0).unwrap().is_lowercase()) {
			if path_so_far.iter().filter(|&o| o == cave_visited).count() == 2 {
				//println!("twice {} in {:?}", cave_visited, path_so_far);
				small_visited_twice = true;
			}
		}

		let count_other = path_so_far.iter().filter(|&o| o == other_cave).count();
		let max_small = if small_twice && !small_visited_twice { 1 } else { 0 };

		if other_cave.chars().nth(0).unwrap().is_lowercase() && count_other > max_small {
			// can't visit smal caves twice
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

