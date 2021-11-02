use crate::aoc;
use std::collections::HashSet;

// i have no idea what "in the long term" is supposed to mean.
// we're simply doing 1_000 ticks. as i understand it, even after 1_000 it
// theoretically possible that some particle overtakes another particle (for possibly
// excessive starting values). but this seems to do it. *shrug*

#[derive(PartialEq, Clone)]
struct Particle {
	position: Coord,
	velocity: Coord,
	acceleration: Coord,
}

#[derive(PartialEq, Clone, Eq, Hash)]
struct Coord {
	x: i32,
	y: i32,
	z: i32,
}

impl Particle {
	fn manhattan(&self) -> i32 {
		self.position.x.abs() + self.position.y.abs() + self.position.z.abs()
	}
}

fn tick(particles: &mut Vec<Particle>, collisions_enabled: bool) {
	let mut all_positions: HashSet<Coord> = HashSet::with_capacity(particles.len());
	let mut duplicate_positions: HashSet<Coord> = HashSet::new();

	for mut particle in &mut *particles {
		particle.velocity.x += particle.acceleration.x;
		particle.velocity.y += particle.acceleration.y;
		particle.velocity.z += particle.acceleration.z;
		particle.position.x += particle.velocity.x;
		particle.position.y += particle.velocity.y;
		particle.position.z += particle.velocity.z;

		if collisions_enabled {
			if all_positions.contains(&particle.position) {
				duplicate_positions.insert(particle.position.clone());
			} else {
				all_positions.insert(particle.position.clone());
			}
		}
	}

	if collisions_enabled {
		particles.retain(|p| !duplicate_positions.contains(&&p.position));
	}
}

fn parse(input: String) -> Vec<Particle> {
	let mut r: Vec<Particle> = vec![];

	for line in input.split('\n') {
		let mut attributes = line.split(", ");

		let p = parse_attribute(attributes.next().unwrap());
		let v = parse_attribute(attributes.next().unwrap());
		let a = parse_attribute(attributes.next().unwrap());

		r.push(Particle{ position: p, velocity: v, acceleration: a });
	}

	return r
}

fn parse_attribute(s: &str) -> Coord {
	let mut values = s.split(&['<', ',', '>'][..]);

	let _ = values.next().unwrap(); // drop `p=<`

	let x: i32 = values.next().unwrap().trim().parse().unwrap();
	let y: i32 = values.next().unwrap().trim().parse().unwrap();
	let z: i32 = values.next().unwrap().trim().parse().unwrap();

	return Coord{ x: x, y: y, z: z}
}

pub fn part1(input: String) -> String {
	let mut particles = parse(input);

	for _wtf in 0..=1_000 {
		tick(&mut particles, false);
	}

	let mut lowest_distance = i32::MAX;
	let mut lowest_distance_id: i32 = -1;

	for (i, p) in particles.iter().enumerate() {
		let m = p.manhattan();
		if m < lowest_distance {
			lowest_distance = m;
			lowest_distance_id = i as i32;
		}
	}

	return lowest_distance_id.to_string()
}

pub fn part2(input: String) -> String {
	let mut particles = parse(input);

	for _wtf in 0..=1_000 {
		tick(&mut particles, true);
	}

	return particles.len().to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 20,
	input: "file:20-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("0", "file:20-input-test"),
	],
	tests_part2: &[
	],
};

