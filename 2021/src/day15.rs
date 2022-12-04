use crate::aoc;

#[derive(Debug)]
struct CaveMap {
	risk_at: Vec<Vec<i32>>,
	count_x: usize,
	count_y: usize,
}

fn lowest_risk(map: &CaveMap) -> i32 {
	// for each position, track the lowest risk possible to reach it.
	let mut risk_to = vec![vec![i32::MAX; map.count_x]; map.count_y];

	// a list of the current position of each path-finding attempt.
	let mut path_positions: Vec<(usize, usize)>;

	// *starting* at 0,0 incurs no risk, but entering 0,0 does incur the position's risk. therefore,
	// start with *two* states (the first two possible steps) and set their `risk_to` accordingly for
	// each respective first step.
	path_positions = [(1,0), (0,1)].to_vec();
	risk_to[1][0] = map.risk_at[1][0];
	risk_to[0][1] = map.risk_at[0][1];

	// for every grid position, figure out what the lowest risk possible is.
	while !path_positions.is_empty() {
		let mut next_path_positions: Vec<(usize, usize)> = Vec::with_capacity(path_positions.len());

		for (posx, posy) in path_positions {
			// for every current position, set as candidates the four possible next steps
			// (up, down, left, right)

			let mut candidate_positions: Vec<(usize, usize)> = Vec::with_capacity(4);
			if posx+1 < map.count_x { candidate_positions.push((posx+1, posy)); }
			if posy+1 < map.count_y { candidate_positions.push((posx, posy+1)); }
			if posx > 0 { candidate_positions.push((posx-1, posy)); }
			if posy > 0 { candidate_positions.push((posx, posy-1)); }

			for (candidate_x, candidate_y) in candidate_positions {
				let risk_to_candidate = risk_to[posx][posy] + map.risk_at[candidate_x][candidate_y];
				if risk_to[candidate_x][candidate_y] > risk_to_candidate {
					// if the candidate position has merit, i.e. the current path has
					// a lower risk to this position, update its `risk_to` and add the
					// candidate for further exploration in the next loop iteration.
					//
					// otherwise, stop exploring this path.

					risk_to[candidate_x][candidate_y] = risk_to_candidate;
					next_path_positions.push((candidate_x, candidate_y));
				}
			}
		}

		path_positions = next_path_positions;
	}

	return risk_to[map.count_x - 1][map.count_y - 1]
}

fn parse(input: String) -> CaveMap {
	let count_y = input.lines().count();
	let count_x = input.lines().nth(0).unwrap().len();
	let mut risk_at = vec![vec![0; count_y]; count_x];

	for y in 0..count_y {
		for x in 0..count_x {
			risk_at[x][y] = (input.lines().nth(y).unwrap().as_bytes()[x] - 48) as i32;
		}
	}

	return CaveMap { risk_at, count_x, count_y }
}

fn five_times(tile: &CaveMap) -> CaveMap {
	let count_y = tile.count_y * 5;
	let count_x = tile.count_x * 5;
	let mut risk_at = vec![vec![0; count_y]; count_x];

	for copy_y in 0..5 {
		for copy_x in 0..5 {
			for tile_y in 0..tile.count_y {
				for tile_x in 0..tile.count_x {
					let mut target_value = tile.risk_at[tile_x][tile_y] + copy_y as i32 + copy_x as i32;
					target_value = 1 + ((target_value - 1) % 9);

					let target_x = tile.count_x * copy_x + tile_x;
					let target_y = tile.count_y * copy_y + tile_y;
					risk_at[target_x][target_y] = target_value;
				}
			}
		}
	}

	return CaveMap { risk_at, count_x, count_y }
}

pub fn part1(input: String) -> String {
	let map = parse(input);
	return lowest_risk(&map).to_string()
}

pub fn part2(input: String) -> String {
	let tile = parse(input);
	let map = five_times(&tile);
	return lowest_risk(&map).to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 15,
	input: "file:15-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("40", "file:15-input-test"),
		("386", "file:15-input-test-penny"),
	],
	tests_part2: &[
		("315", "file:15-input-test"),
		("2806", "file:15-input-test-penny"),
	],
};

