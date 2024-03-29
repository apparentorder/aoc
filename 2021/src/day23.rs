use crate::aoc;
use std::collections::HashSet;

type Hallway = Vec<Option<Amphipod>>;
type Floor = Vec<Amphipod>;

#[derive(Clone, Debug, PartialEq, Eq, Hash)]
struct State {
	hallway: Hallway,
	amber: Floor,
	bronze: Floor,
	copper: Floor,
	desert: Floor,
	energy_used: i32,
	floor_capacity: usize,
}

// hallway, 11 items:
//                                  01234567890
// hallway/floor connection points:   ^ ^ ^ ^
const HALLWAY_INTERSECTIONS: &[usize; 4] = &[2,4,6,8];

impl State {
	fn floor(&self, a: Amphipod) -> &Floor {
		match a {
			Amphipod::Amber => &self.amber,
			Amphipod::Bronze => &self.bronze,
			Amphipod::Copper => &self.copper,
			Amphipod::Desert => &self.desert,
		}
	}

	fn floor_mut(&mut self, a: Amphipod) -> &mut Floor {
		match a {
			Amphipod::Amber => &mut self.amber,
			Amphipod::Bronze => &mut self.bronze,
			Amphipod::Copper => &mut self.copper,
			Amphipod::Desert => &mut self.desert,
		}
	}

	fn floor_has_wrong_amphipods(&self, a: Amphipod) -> bool {
		let floor = self.floor(a);
		return floor.iter().filter(|&fa| fa != &a).count() > 0
	}

	fn floor_is_empty(&self, amphipod: Amphipod) -> bool {
		let floor = self.floor(amphipod);
		return floor.is_empty()
	}

	fn floor_done(&self, amphipod: Amphipod) -> bool {
		let c = self.floor(amphipod).iter().filter(|&fa| fa == &amphipod).count();
		return c == self.floor_capacity
	}

	fn floor_pop(&mut self, amphipod: Amphipod) -> (Amphipod, usize) {
		let floor = self.floor_mut(amphipod);
		let found = floor.pop().unwrap();
		return (found, floor.len())
	}

	fn floor_push(&mut self, a: Amphipod) -> i32 {
		let floor = self.floor_mut(a);
		floor.push(a);
		return (floor.len() - 1) as i32
	}

	fn is_blocked(&self, pos1: usize, pos2: usize) -> bool {
		let i_min = pos1.min(pos2);
		let i_max = pos1.max(pos2);
		for i in (i_min+1)..=(i_max-1) {
			if let Some(_) = self.hallway[i] {
				return true
			}
		}

		return false
	}
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
enum Amphipod {
	Amber = 1,
	Bronze = 10,
	Copper = 100,
	Desert = 1000,
}

impl Amphipod {
	fn from_char(c: char) -> Amphipod {
		match c {
			'A' => Amphipod::Amber,
			'B' => Amphipod::Bronze,
			'C' => Amphipod::Copper,
			'D' => Amphipod::Desert,
			_ => panic!(),
		}
	}

	fn hallway_intersection(&self) -> usize {
		match self {
			Amphipod::Amber => HALLWAY_INTERSECTIONS[0],
			Amphipod::Bronze => HALLWAY_INTERSECTIONS[1],
			Amphipod::Copper => HALLWAY_INTERSECTIONS[2],
			Amphipod::Desert => HALLWAY_INTERSECTIONS[3],
		}
	}
}

fn solve(state: &State, states_seen: &mut HashSet<State>, best_so_far: &mut i32) -> i32 {
	let mut energy = i32::MAX;

	let amber_done = state.floor_done(Amphipod::Amber);
	let bronze_done = state.floor_done(Amphipod::Bronze);
	let copper_done = state.floor_done(Amphipod::Copper);
	let desert_done = state.floor_done(Amphipod::Desert);

	if amber_done && bronze_done && copper_done && desert_done {
		println!("completed with energy {}", state.energy_used);
		*best_so_far = state.energy_used;
		return state.energy_used
	}

	if states_seen.contains(state) {
		return energy
	}
	states_seen.insert(state.clone());
	//println!("try state {:?}", state);

	let mut next_states = Vec::<State>::new();

	// possible movers: floor dwellers
	for floor_type in [Amphipod::Amber, Amphipod::Bronze, Amphipod::Copper, Amphipod::Desert] {
		if state.floor_is_empty(floor_type) || !state.floor_has_wrong_amphipods(floor_type) {
			continue
		}

		let mut new_state = state.clone();
		let (found_a, floor_position) = new_state.floor_pop(floor_type);
		let distance = state.floor_capacity - floor_position;
		new_state.energy_used += distance as i32 * (found_a as i32);
		new_state.hallway[floor_type.hallway_intersection()] = Some(found_a);

		next_states.append(&mut clear_hallway_position(&new_state, floor_type.hallway_intersection()));
	}

	// possible movers: hallway occupants
	for i in 0..state.hallway.len() {
		next_states.append(&mut clear_hallway_position(state, i));
	}

	for ns in next_states {
		if ns.energy_used < *best_so_far {
			energy = energy.min(solve(&ns, states_seen, best_so_far));
		}
	}

	return energy
}

fn clear_hallway_position(state: &State, source_index: usize) -> Vec<State> {
	let mut next_states = Vec::<State>::new();

	let amphipod = match state.hallway[source_index] {
		Some(x) => x,
		_ => return next_states,
	};

	//println!("try state {:?}", state);

	// possible destination: matching floor

	if !state.floor_has_wrong_amphipods(amphipod) {
		if !state.is_blocked(amphipod.hallway_intersection(), source_index) {
			let mut new_state = state.clone();
			new_state.hallway[source_index] = None;

			let mut distance = (amphipod.hallway_intersection() as i32 - source_index as i32).abs();
			distance += new_state.floor_capacity as i32 - new_state.floor_push(amphipod);

			new_state.energy_used += distance * (amphipod as i32);

			next_states.push(new_state);
			return next_states
		}
	}

	if !HALLWAY_INTERSECTIONS.contains(&source_index) {
		// we haven't moved away from a floor, therefore, we've been on the
		// hallway before -- rule 3: "Once an amphipodpod stops moving in the hallway,
		// it will stay in that spot until it can move into a room"
		return next_states // empty
	}

	let mut possible_destinations = Vec::<usize>::new();
	for pi in (source_index+1)..state.hallway.len() {
		if state.hallway[pi] != None {
			break
		}
		possible_destinations.push(pi);
	}

	for pi in (0..source_index).rev() {
		if state.hallway[pi] != None {
			break
		}
		possible_destinations.push(pi);
	}

	possible_destinations.retain(|d| !HALLWAY_INTERSECTIONS.contains(d));

	for possible_destination in possible_destinations {
		let mut new_state = state.clone();
		let distance = (source_index as i32 - possible_destination as i32).abs();
		new_state.energy_used += distance * (amphipod as i32);
		new_state.hallway[source_index] = None;
		new_state.hallway[possible_destination] = Some(amphipod);
		next_states.push(new_state);
	}

	return next_states
}

fn parse(input: &str, additional_fun: bool) -> State {
	let mut amber = Floor::new();
	let mut bronze = Floor::new();
	let mut copper = Floor::new();
	let mut desert = Floor::new();

	let lines = input.lines().collect::<Vec<_>>();

	let mut floor_lines = [lines[3], lines[2]].to_vec();
	if additional_fun {
		floor_lines.insert(1, "  #D#C#B#A#  ");
		floor_lines.insert(1, "  #D#B#A#C#  ");
	}

	let hallway_count = lines[1].chars().filter(|&c| c == '.').count();
	let hallway = vec![None; hallway_count];

	for line in &floor_lines {
		let c = line.chars().collect::<Vec<_>>();
		amber.push(Amphipod::from_char(c[3]));
		bronze.push(Amphipod::from_char(c[5]));
		copper.push(Amphipod::from_char(c[7]));
		desert.push(Amphipod::from_char(c[9]));
	}

	let state = State {
		hallway,
		amber,
		bronze,
		copper,
		desert,
		energy_used: 0,
		floor_capacity: floor_lines.len(),
	};

	return state
}

pub fn part1(input: String) -> String {
	let state = parse(&input, false);
	let mut best = i32::MAX;
	let energy = solve(&state, &mut HashSet::<State>::new(), &mut best);
	return energy.to_string()
}

pub fn part2(input: String) -> String {
	let state = parse(&input, true);
	let mut best = i32::MAX;
	let energy = solve(&state, &mut HashSet::<State>::new(), &mut best);
	return energy.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 23,
	input: "file:23-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("12521", "file:23-input-test"),
	],
	tests_part2: &[
		("44169", "file:23-input-test"),
	],
};

