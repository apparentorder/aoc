use crate::aoc;
use std::collections::{HashMap, HashSet};

type Path<'a> = HashSet<&'a str>;
type CaveMap<'a> = HashMap<&'a str, Path<'a>>;

fn find_paths(
	map: &CaveMap,
	path_so_far: Path,
	next_cave: &str,
	small_twice_allowed: bool,
	small_twice_used: bool
) -> i32 {
	let mut paths = 0;

	if next_cave == "end" {
		return 1
	}

	for next_cave in map.get(&next_cave).unwrap() {
		let mut next_cave_visited_twice = small_twice_used;

		if next_cave.chars().nth(0).unwrap().is_lowercase() && path_so_far.contains(next_cave) {
			if !small_twice_allowed || small_twice_used {
				continue
			}

			next_cave_visited_twice = true;
		}

		let mut this_psf = path_so_far.clone();
		this_psf.insert(next_cave.clone());

		paths += find_paths(&map, this_psf, next_cave, small_twice_allowed, next_cave_visited_twice);
	}

	return paths
}

fn parse(input: &str) -> CaveMap {
	let mut r = CaveMap::new();

	for line in input.lines() {
		let caves = line.split('-').collect::<Vec<_>>();

		let a = r.entry(&caves[0]).or_insert(HashSet::new());
		a.insert(&caves[1]);

		let b = r.entry(&caves[1]).or_insert(HashSet::new());
		b.insert(&caves[0]);
	}

	// don't make connections back to `start` (it's never allowed to go back there)
	for (_, connections) in &mut r {
		connections.retain(|&adj| adj != "start");
	}

	return r
}

pub fn part1(input: String) -> String {
	let map = parse(&input);
	let paths = find_paths(&map, HashSet::new(), "start", false, false);
	return paths.to_string()
}

pub fn part2(input: String) -> String {
	let map = parse(&input);
	let paths = find_paths(&map, HashSet::new(), "start", true, false);
	return paths.to_string()
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

