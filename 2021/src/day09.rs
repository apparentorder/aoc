use crate::aoc;
use std::collections::HashSet;

type HeightMap = Vec<Vec<i32>>;

fn parse(input: String) -> HeightMap {
	let mut r: HeightMap = vec![];

	for line in input.lines() {
		r.push(line.chars().map(|d| ((d as u8) - 48) as i32).collect());
	}

	return r
}

fn adjacent_values(map: &HeightMap, x: usize, y: usize) -> Vec<i32> {
	let max_x = map[0].len() - 1;
	let max_y = map.len() - 1;
	let mut r: Vec<i32> = vec![];

	if x > 0     { r.push(map[y][x - 1]); }
	if x < max_x { r.push(map[y][x + 1]); }
	if y > 0     { r.push(map[y - 1][x]); }
	if y < max_y { r.push(map[y + 1][x]); }

	return r
}

fn find_low_points(map: &HeightMap) -> Vec<(usize, usize)> {
	let mut r: Vec<(usize, usize)> = vec![];

	for y in 0..map.len() {
		for x in 0..map[y].len() {
			let adjacent = adjacent_values(&map, x, y);
			if adjacent.iter().min().unwrap() > &map[y][x] {
				//println!("low point {}", map[y][x]);
				r.push((x, y));
			}
		}
	}

	return r
}

fn basin_size(map: &HeightMap, x: usize, y: usize) -> i32 {
	let mut seen: HashSet<(usize, usize)> = HashSet::new();
	let mut to_explore: Vec<(usize, usize)> = vec![(x, y)];

	let max_x = map[0].len() - 1;
	let max_y = map.len() - 1;

	let mut size = 0;

	while to_explore.len() > 0 {
		let mut to_explore_next: Vec<(usize, usize)> = vec![];

		for (check_x, check_y) in to_explore {
			if seen.contains(&(check_x, check_y)) {
				continue
			}
			seen.insert((check_x, check_y));

			size += 1;

			if check_x > 0     && map[check_y][check_x - 1] != 9 { to_explore_next.push((check_x - 1, check_y)); }
			if check_x < max_x && map[check_y][check_x + 1] != 9 { to_explore_next.push((check_x + 1, check_y)); }
			if check_y > 0     && map[check_y - 1][check_x] != 9 { to_explore_next.push((check_x, check_y - 1)); }
			if check_y < max_y && map[check_y + 1][check_x] != 9 { to_explore_next.push((check_x, check_y + 1)); }
		}

		to_explore = to_explore_next;
	}

	println!("basin from x={} y={} has size={}", x, y, size);
	return size
}

pub fn part1(input: String) -> String {
	let map = parse(input);
	let low_points = find_low_points(&map);

	let sum: i32 = low_points.iter().map(|&(x, y)| map[y][x] + 1).sum();

	return sum.to_string()
}

pub fn part2(input: String) -> String {
	let map = parse(input);
	let low_points = find_low_points(&map);

	let mut sizes: Vec<i32> = low_points.iter().map(|&(x, y)| basin_size(&map, x, y)).collect();
	sizes.sort();
	sizes.reverse();
	println!("sizes {:?}", sizes);
	return sizes[0..=2].iter().product::<i32>().to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 9,
	input: "file:09-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("15", "file:09-input-test"),
	],
	tests_part2: &[
		("1134", "file:09-input-test"),
	],
};

