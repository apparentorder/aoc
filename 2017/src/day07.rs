use crate::aoc;
use std::collections::HashMap;

//
// - discs are referred to by name (string) via HashMap
//
// - each entry has disc weight and *total* weight and sub_tower_discs (child nodes in the tree; by name/string)
//
// - step 0: get the puzzle's terminology -- "program", "tower", "sub-tower" and "disc". i tried to stick to
//           "disc" and "sub-tower" for referring to a tree node and the part of a tree starting at some node,
//           respectively.
//
// - step 1: parse() to fill in everything except total weight
//
// - step 2: find_tower_root() to find the one disc that's never referred to as a sub_tower_disc (child node)
//   (that's enough for part 1)
//
// - step 3: find_tower_weight() recurse through the tree and fill the cumulative total_weight that each disc bears
//
// - step 4: find_tower_imbalance() to recurse, taking a shortcut when there is a clearly imbalanced set of sub_towers
//

struct DiscData {
	disc_weight: i32,
	total_weight: i32,
	sub_tower_discs: Vec<String>,
}
type DiscMap = HashMap<String, DiscData>;

fn find_tower_weight(disc_map: &mut DiscMap, starting_disc: String) -> i32 {
	//println!("find {}", starting_disc);

	let mut sub_towers_weight: i32 = 0;

	// to_vec() hack to avoid im/mutable borrow horseshit
	let sub_tower_discs = &disc_map[&starting_disc].sub_tower_discs.to_vec();
	for sub_tower_disc in sub_tower_discs {
		sub_towers_weight += find_tower_weight(disc_map, sub_tower_disc.to_string());
	}

	let new_disc_data = DiscData {
		disc_weight: disc_map[&starting_disc].disc_weight,
		total_weight: disc_map[&starting_disc].disc_weight + sub_towers_weight,
		sub_tower_discs: disc_map[&starting_disc].sub_tower_discs.to_vec(),
	};

	disc_map.insert(starting_disc.to_string(), new_disc_data);
	return disc_map[&starting_disc].total_weight
}

fn find_tower_imbalance(disc_map: &DiscMap, starting_disc: String, expected_total_weight: i32) -> String {
	// assumptions:
	// - root disc has sub-towers
	// - no disc has just one sub-tower

	// to_vec() hack to avoid im/mutable borrow horseshit
	let sub_tower_discs = &disc_map[&starting_disc].sub_tower_discs.to_vec();

	let mut expected_sub_tower_weight: i32 = 0;

	if sub_tower_discs.len() >= 3 {
		// only for 3+ sub-towers we can figure which one is the outlier

		let mut weights_seen: Vec<i32> = vec![]; // could be a Set, but probably not worth it.
		for disc in sub_tower_discs {
			if weights_seen.contains(&disc_map[disc].total_weight) {
				// value appears twice, must the the correct one
				expected_sub_tower_weight = disc_map[disc].total_weight;
				break
			}

			weights_seen.push(disc_map[disc].total_weight);
		}
	}

	if expected_sub_tower_weight > 0 {
		// see if we actually have an imbalanced sub-tower
		// (if so, we don't need to search any other sub-towers)
		for disc in sub_tower_discs {
			if disc_map[disc].total_weight != expected_sub_tower_weight {
				println!(
					"disc {} sub-tower {} imbalanced: expected {} actual {}",
					starting_disc, disc,
					expected_sub_tower_weight, disc_map[disc].total_weight
				);
				return find_tower_imbalance(disc_map, disc.to_string(), expected_sub_tower_weight);
			}
		}
	}

	// all sub-towers are balanced (or just two), check if we are the problem
	if expected_total_weight > 0 && disc_map[&starting_disc].total_weight != expected_total_weight {
		let weight_diff = expected_total_weight - disc_map[&starting_disc].total_weight;
		println!(
			"disc {} has wrong weight: expected total {} actual total {} \
			expected disc {} actual disc {}",
			starting_disc,
			expected_total_weight,
			disc_map[&starting_disc].total_weight,
			disc_map[&starting_disc].disc_weight + weight_diff,
			disc_map[&starting_disc].disc_weight,
		);
		return (disc_map[&starting_disc].disc_weight + weight_diff).to_string();
	}

	// .. otherwise, dutifully check all sub-towers
	for disc in sub_tower_discs {
		let r = find_tower_imbalance(disc_map, disc.to_string(), expected_sub_tower_weight);
		if r != "" {
			return r
		}
	}

	return "".to_string();
}

fn find_tower_root(disc_map: &DiscMap) -> String {
	let mut tower_root = "";

	'outer: for try_tower in disc_map.keys() {
		for (_, disc_data) in disc_map {
			if disc_data.sub_tower_discs.contains(&try_tower) {
				continue 'outer
			}
		}
		tower_root = try_tower;
		break;
	}

	return tower_root.to_string();
}

fn parse(input: &String) -> DiscMap {
	let mut disc_map = DiscMap::new();

	for line in input.split('\n') {
		if line == "" {
			continue
		}

		let mut parts = line.split_whitespace();
		let name = parts.next().unwrap().to_string();

		let mut weight_str = parts.next().unwrap().to_string();
		weight_str.retain(|c| c >= '0' && c <= '9');
		let weight: i32 = weight_str.parse().unwrap();

		let mut sub_tower_discs: Vec<String> = vec![];

		if parts.next() != None {
			// more parts follow, so this disc has sub_tower_discs
			// (note: this check on next() eats the "->" token from the input)

			while let Some(sub_tower_disc_str) = parts.next() {
				let mut sub_tower_disc = sub_tower_disc_str.to_string();
				sub_tower_disc.retain(|c| c != ','); // strip trailing ','
				sub_tower_discs.push(sub_tower_disc);
			}
		}

		let data = DiscData {
			disc_weight: weight,
			total_weight: weight,
			sub_tower_discs: sub_tower_discs,
		};
		disc_map.insert(name, data);
	}

	return disc_map;
}

pub fn part1(input: String) -> String {
	let disc_map = parse(&input);
	return find_tower_root(&disc_map);
}

pub fn part2(input: String) -> String {
	let mut disc_map = parse(&input);
	let root_disc = find_tower_root(&disc_map);
	find_tower_weight(&mut disc_map, root_disc.to_string());
	return find_tower_imbalance(&disc_map, root_disc, 0)
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 07,
	input: "file:07-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("tknk", "file:07-input-test"),
	],
	tests_part2: &[
		("60", "file:07-input-test"),
	],
};

