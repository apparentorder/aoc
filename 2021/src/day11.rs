use crate::aoc;

type Coord = (usize, usize);
type OctoMap = Vec<Vec<i32>>;

fn flashes(map: &mut OctoMap, max_steps_for_count: i32) -> (i32, i32) {
	let mut flash_count_after_max_steps = 0;
	let mut steps = 0;

	loop {
		for y in 0..map.len() {
			for x in 0..map[y].len() {
				map[y][x] += 1;
			}
		}

		for y in 0..map.len() {
			for x in 0..map[y].len() {
				check_flash(map, x, y);
			}
		}

		steps += 1;

		let flashs_this_step = map.iter().fold(0, |sum, line| sum + line.iter().filter(|&col| col == &0).count() as i32);

		if steps <= max_steps_for_count {
			flash_count_after_max_steps += flashs_this_step;
		}

		if flashs_this_step == (map.len() * map[0].len()) as i32 {
			// sync flash of all octos
			return (flash_count_after_max_steps, steps)
		}
	}
}

fn check_flash(map: &mut OctoMap, x: usize, y: usize) {
	if map[y][x] <= 9 {
		return
	}

	map[y][x] = 0;
	for (adj_x, adj_y) in adjacent_coordinates(&map, x, y) {
		if map[adj_y][adj_x] != 0 {
			map[adj_y][adj_x] += 1;
			check_flash(map, adj_x, adj_y);
		}
	}
}

fn adjacent_coordinates(map: &OctoMap, xu: usize, yu: usize) -> Vec<Coord> {
	let max_x = map[0].len() as i32 - 1;
	let max_y = map.len() as i32 - 1;
	let x = xu as i32;
	let y = yu as i32;
	let mut r: Vec<(i32, i32)> = vec![];

	r.push((x - 1, y - 1));
	r.push((x    , y - 1));
	r.push((x + 1, y - 1));

	r.push((x - 1, y    ));
	r.push((x + 1, y    ));

	r.push((x - 1, y + 1));
	r.push((x    , y + 1));
	r.push((x + 1, y + 1));

	r.retain(|&(x, y)| x >= 0 && x <= max_x && y >= 0 && y <= max_y);
	return r.iter().map(|&(x, y)| (x as usize, y as usize)).collect()
}

fn parse(input: String) -> OctoMap {
	let mut r: OctoMap = vec![];

	for line in input.lines() {
		r.push(line.chars().map(|d| ((d as u8) - 48) as i32).collect());
	}

	return r
}

pub fn part1(input: String) -> String {
	let mut map = parse(input);
	let (flashes, _) = flashes(&mut map, 100);
	return flashes.to_string()
}

pub fn part2(input: String) -> String {
	let mut map = parse(input);
	let (_, sync_after) = flashes(&mut map, 100);
	return sync_after.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 11,
	input: "file:11-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		//("9", "11111\n19991\n19191\n19991\n11111"),
		("1656", "file:11-input-test"),
	],
	tests_part2: &[
		("195", "file:11-input-test"),
	],
};

