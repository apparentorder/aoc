use crate::aoc;
use std::collections::HashSet;

type Floor = Vec<Amphi>;
//type FloorMap = HashMap<char, Floor>;

#[derive(Clone, Debug, PartialEq, Eq, Hash)]
struct State {
	hallway: Floor,
	//floors: FloorMap,
	amber: Floor,
	bronze: Floor,
	copper: Floor,
	desert: Floor,
	energy_used: i32,
	floor_capacity: usize,
}

// hallway, ten items:
//                                  01234567890
// hallway/floor connection points:   ^ ^ ^ ^
const HALLWAY_CONNECTIONS: &[usize; 4] = &[2,4,6,8];
const HALLWAY_VALID_STOPS: &[usize; 7] = &[0,1,3,5,7,9,10];

impl State {
	fn floor(&self, a: Amphi) -> &Floor {
		match a {
			Amphi::Amber => &self.amber,
			Amphi::Bronze => &self.bronze,
			Amphi::Copper => &self.copper,
			Amphi::Desert => &self.desert,
			_ => panic!(),
		}
	}

	fn floor_mut(&mut self, a: Amphi) -> &mut Floor {
		match a {
			Amphi::Amber => &mut self.amber,
			Amphi::Bronze => &mut self.bronze,
			Amphi::Copper => &mut self.copper,
			Amphi::Desert => &mut self.desert,
			_ => panic!(),
		}
	}

	fn floor_has_wrong_amphis(&self, a: Amphi) -> bool {
		let floor = self.floor(a);
		return floor.iter().filter(|&fa| fa != &a).count() > 0
	}

	fn floor_is_full(&self, amphi: Amphi) -> bool {
		let floor = self.floor(amphi);
		return floor.len() == self.floor_capacity
	}

	fn floor_is_empty(&self, amphi: Amphi) -> bool {
		let floor = self.floor(amphi);
		return floor.is_empty()
	}

	fn floor_pop(&mut self, amphi: Amphi) -> (Amphi, usize) {
		let mut floor = self.floor_mut(amphi);
		let found = floor.pop().unwrap();
		return (found, floor.len())
	}

	fn add_to_floor(&mut self, a: Amphi) -> i32 {
		let mut floor = self.floor_mut(a);
		floor.push(a);
		return (floor.len() - 1) as i32
	}
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
enum Amphi {
	None = 0,
	Amber = 1,
	Bronze = 10,
	Copper = 100,
	Desert = 1000,
}

impl Amphi {
	fn from_char(c: char) -> Amphi {
		match c {
			'A' => Amphi::Amber,
			'B' => Amphi::Bronze,
			'C' => Amphi::Copper,
			'D' => Amphi::Desert,
			'.' => Amphi::None,
			_ => panic!(),
		}
	}

	fn hallway_connection(&self) -> usize {
		match self {
			Amphi::Amber => HALLWAY_CONNECTIONS[0],
			Amphi::Bronze => HALLWAY_CONNECTIONS[1],
			Amphi::Copper => HALLWAY_CONNECTIONS[2],
			Amphi::Desert => HALLWAY_CONNECTIONS[3],
			_ => panic!(),
		}
	}

}

fn solve(state: &State, states_seen: &mut HashSet<State>, best_so_far: &mut i32) -> i32 {
	let mut energy = i32::MAX;

	let amber_done = state.amber == [Amphi::Amber].repeat(state.floor_capacity);
	let bronze_done = state.bronze == [Amphi::Bronze].repeat(state.floor_capacity);
	let copper_done = state.copper == [Amphi::Copper].repeat(state.floor_capacity);
	let desert_done = state.desert == [Amphi::Desert].repeat(state.floor_capacity);

	if amber_done && bronze_done && copper_done && desert_done {
		println!("YEAH! {}", state.energy_used);
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
	for floor_type in [Amphi::Amber, Amphi::Bronze, Amphi::Copper, Amphi::Desert] {
		if state.floor_is_empty(floor_type) || !state.floor_has_wrong_amphis(floor_type) {
			continue
		}

		let mut new_state = state.clone();
		let (found_a, floor_position) = new_state.floor_pop(floor_type);
		let distance = state.floor_capacity - floor_position;
		new_state.energy_used += distance as i32 * (found_a as i32);
		new_state.hallway[floor_type.hallway_connection()] = found_a;

		next_states.extend(clear_hallway_position(&new_state, states_seen, best_so_far, floor_type.hallway_connection()));
	}

	// possible movers: hallway occupants
	for i in 0..state.hallway.len() {
		next_states.extend(clear_hallway_position(state, states_seen, best_so_far, i));
	}

	//next_states.sort_by(|a, b| a.energy_used.cmp(&b.energy_used));
	//println!("{:?}", next_states);

	let b = *best_so_far;
	for ns in next_states {
		if ns.energy_used < *best_so_far {
			energy = energy.min(solve(&ns, states_seen, best_so_far));
		}
	}

	return energy
}

fn clear_hallway_position(state: &State, states_seen: &mut HashSet<State>, best_so_far: &mut i32, source_index: usize) -> Vec<State> {
	let mut energy = i32::MAX;
	let mut next_states = Vec::<State>::new();

	let a = state.hallway[source_index];
	if a == Amphi::None {
		return next_states
	}

	//println!("try state {:?}", state);

	// possible destination: matching floor

	if !state.floor_has_wrong_amphis(a) {
		// collision detection
		let mut blocked = false;
		let i_min = source_index.min(a.hallway_connection());
		let i_max = source_index.max(a.hallway_connection());
		for i in i_min..=i_max {
			if i != source_index && state.hallway[i] != Amphi::None {
				// can't move there
				blocked = true;
			}
		}

		if !blocked {
			let mut new_state = state.clone();
			new_state.hallway[source_index] = Amphi::None;

			let mut distance = (a.hallway_connection() as i32 - source_index as i32).abs();
			distance += new_state.floor_capacity as i32 - new_state.add_to_floor(a);

			new_state.energy_used += distance * (a as i32);

			next_states.push(new_state);
			return next_states
		}
	}

	if !HALLWAY_CONNECTIONS.contains(&source_index) {
		// we haven't moved away from a floor, therefore, we've been on the
		// hallway before -- rule 3: "Once an amphipod stops moving in the hallway,
		// it will stay in that spot until it can move into a room"
		return next_states // empty
	}

	// possible destinations: any other reachable hallway position
	let mut possible_destinations = Vec::<usize>::new();
	for pi in (source_index+1)..state.hallway.len() {
		if state.hallway[pi] != Amphi::None {
			break
		}
		possible_destinations.push(pi);
	}

	for pi in (0..source_index).rev() {
		if state.hallway[pi] != Amphi::None {
			break
		}
		possible_destinations.push(pi);
	}

	possible_destinations.retain(|d| !HALLWAY_CONNECTIONS.contains(d));

	for pd in possible_destinations {
		let mut new_state = state.clone();
		let distance = (source_index as i32 - pd as i32).abs();
		new_state.energy_used += distance * (a as i32);
		new_state.hallway[source_index] = Amphi::None;
		new_state.hallway[pd] = a;
		next_states.push(new_state);
	}

	return next_states
}

fn parse(input: &str, additional_fun: bool) -> State {
	let mut amber = Floor::new();
	let mut bronze = Floor::new();
	let mut copper = Floor::new();
	let mut desert = Floor::new();
	//let floors = FloorMap::new();

	let mut lines = input.lines().collect::<Vec<_>>();

	let mut floor_lines = [lines[3], lines[2]].to_vec();
	if additional_fun {
		floor_lines.insert(1, "  #D#C#B#A#  ");
		floor_lines.insert(1, "  #D#B#A#C#  ");
	}

	let hallway_count = lines[1].chars().filter(|&c| c == '.').count();
	let hallway = vec![Amphi::None; hallway_count];

	for line in floor_lines {
		let c = line.chars().collect::<Vec<_>>();
		amber.push(Amphi::from_char(c[3]));
		bronze.push(Amphi::from_char(c[5]));
		copper.push(Amphi::from_char(c[7]));
		desert.push(Amphi::from_char(c[9]));
	}

	let state = State {
		hallway,
		amber,
		bronze,
		copper,
		desert,
		energy_used: 0,
		floor_capacity: if additional_fun { 4 } else { 2 },
	};

	println!("{:?}", state);
	return state
}

pub fn part1(input: String) -> String {
	let state = parse(&input, false);
	let energy = solve(&state, &mut HashSet::<State>::new(), &mut i32::MAX);
	return energy.to_string()
}

pub fn part2(input: String) -> String {
	let state = parse(&input, true);
	let energy = solve(&state, &mut HashSet::<State>::new(), &mut i32::MAX);
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

