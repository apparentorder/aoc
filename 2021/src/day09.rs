use crate::aoc;
use std::collections::HashSet;

type HeightMap = Vec<Vec<i32>>;
type Coord = (usize, usize);

fn find_low_points(map: &HeightMap) -> Vec<Coord> {
	let mut r: Vec<Coord> = vec![];

	for y in 0..map.len() {
		for x in 0..map[y].len() {
			let height = map[y][x];

			let lowest_adjacent = adjacent_coordinates(&map, x, y)
				.iter()
				.map(|&(adj_x, adj_y)| map[adj_y][adj_x])
				.min()
				.unwrap();

			if lowest_adjacent > height {
				//println!("low point {}", map[y][x]);
				r.push((x, y));
			}
		}
	}

	return r
}

fn basin_size(map: &HeightMap, x: usize, y: usize) -> i32 {
	let mut seen: HashSet<Coord> = HashSet::new();
	let mut to_explore: HashSet<Coord> = HashSet::new();
	let mut to_explore_next: HashSet<Coord> = HashSet::new();

	let mut size = 0;
	to_explore.insert((x, y));

	while to_explore.len() > 0 {
		for (check_x, check_y) in to_explore {
			if seen.contains(&(check_x, check_y)) {
				continue
			}

			seen.insert((check_x, check_y));
			size += 1;

			for (adj_x, adj_y) in adjacent_coordinates(&map, check_x, check_y) {
				if map[adj_y][adj_x] != 9 {
					to_explore_next.insert((adj_x, adj_y));
				}
			}
		}

		to_explore = to_explore_next.clone();
		to_explore_next.clear();
	}

	//println!("basin from x={} y={} has size={}", x, y, size);
	return size
}

fn adjacent_coordinates(map: &HeightMap, x: usize, y: usize) -> Vec<Coord> {
	let max_x = map[0].len() - 1;
	let max_y = map.len() - 1;
	let mut r: Vec<Coord> = vec![];

	if x > 0     { r.push((x - 1, y)); }
	if x < max_x { r.push((x + 1, y)); }
	if y > 0     { r.push((x, y - 1)); }
	if y < max_y { r.push((x, y + 1)); }

	return r
}

fn parse(input: String) -> HeightMap {
	let mut r: HeightMap = vec![];

	for line in input.lines() {
		r.push(line.chars().map(|d| ((d as u8) - 48) as i32).collect());
	}

	return r
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

