use crate::aoc;

// this runs reasonably fast (significantly ~1s) with release optimizations.
// without optimizations, though, it runs 15-20sec.

type ComponentList = Vec<Component>;
type ComponentIndexList = Vec<usize>;
struct Component {
	type_a: i32,
	type_b: i32,
}

impl Component {
	fn strength(&self) -> i32 {
		return self.type_a + self.type_b
	}

	fn opposite_of(&self, one_value: i32) -> Option<i32> {
		if one_value == self.type_a {
			Some(self.type_b)
		} else if one_value == self.type_b {
			Some(self.type_a)
		} else {
			None
		}
	}
}

fn build_bridges(components: &ComponentList, used_components: ComponentIndexList, port_type: i32) -> Vec<ComponentIndexList> {
	let mut r: Vec<ComponentIndexList> = vec![];

	//println!("uc={:?} pt={}", used_components, port_type);

	for candidate_index in (0..components.len()).filter(|i| !used_components.contains(i)) {
		if let Some(next_port_type) = components[candidate_index].opposite_of(port_type) {
			let mut next_used_components = used_components.to_vec();
			next_used_components.push(candidate_index);

			let mut possible_bridges = build_bridges(components, next_used_components, next_port_type);
			r.append(&mut possible_bridges);
		}
	}

	r.push(used_components);
	return r
}

fn strongest_bridge_strength(components: ComponentList) -> i32 {
	let bridges = build_bridges(&components, vec![], 0);

	let mut max_strength = 0;
	for b in bridges {
		let mut strength = 0;

		//print!("bridge: ");
		for i in b {
			//print!("{}/{}--", components[i].type_a, components[i].type_b);
			strength += components[i].strength();
		}

		//println!(" (strength {})", strength);
		max_strength = max_strength.max(strength);
	}

	return max_strength
}

fn longest_bridge_strength(components: ComponentList) -> i32 {
	let bridges = build_bridges(&components, vec![], 0);

	let max_length = bridges.iter().map(|b| b.len()).max().unwrap();

	let mut max_strength = 0;
	for b in bridges.iter().filter(|&b| b.len() == max_length) {
		let strength = b.iter().fold(0, |s, &i| s + components[i].strength());
		max_strength = max_strength.max(strength);
	}

	return max_strength
}

fn parse(input: String) -> ComponentList {
	let mut r: ComponentList = vec![];

	for line in input.split('\n') {
		let mut parts = line.split('/');
		let type_a: i32 = parts.next().unwrap().parse().unwrap();
		let type_b: i32 = parts.next().unwrap().parse().unwrap();

		r.push(Component { type_a: type_a, type_b: type_b });
	}

	return r
}

pub fn part1(input: String) -> String {
	let components = parse(input);
	return strongest_bridge_strength(components).to_string();
}

pub fn part2(input: String) -> String {
	let components = parse(input);
	return longest_bridge_strength(components).to_string();
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 24,
	input: "file:24-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("31", "file:24-input-test"),
	],
	tests_part2: &[
		("19", "file:24-input-test"),
	],
};

