use crate::aoc;

type CuboidList = Vec<Cuboid>;

struct Cuboid {
	layer: i64,
	x_min: i64, x_max: i64,
	y_min: i64, y_max: i64,
	z_min: i64, z_max: i64,
	is_on: bool,
}

impl Cuboid {
	fn count_distinct(&self, all_cuboids: &CuboidList) -> i64 {
		let mut count = self.count();
		//println!("@{} total count={}, {:?}", self.layer, count, self);

		for other_cuboid in all_cuboids.iter().filter(|r| r.layer > self.layer) {
			if let Some(overlap) = self.overlap(other_cuboid) {
				//println!("self  {:?}", self);
				//println!("other {:?}", other_cuboid);
				//println!("overl {:?}", overlap);
				//println!("");
				count -= overlap.count_distinct(all_cuboids);
			}
		}

		//println!("@{} distinct count={}, {:?}", self.layer, count, self);
		return count
	}

	fn count(&self) -> i64 {
		let count_x = (self.x_max - self.x_min) + 1;
		let count_y = (self.y_max - self.y_min) + 1;
		let count_z = (self.z_max - self.z_min) + 1;

		return count_x * count_y * count_z
	}

	fn count_on(&self, all_cuboids: &CuboidList) -> i64 {
		if !self.is_on {
			return 0
		}

		return self.count_distinct(all_cuboids);
	}

	fn is_initialization_cube(&self) -> bool {
		let min = [self.x_min, self.y_min, self.z_min].iter().min().unwrap().abs();
		let max = [self.x_max, self.y_max, self.z_max].iter().max().unwrap().abs();
		return min <= 50 && max <= 50
	}

	fn overlap(&self, other: &Cuboid) -> Option<Cuboid> {
		let overlaps_x = other.x_min <= self.x_max && other.x_max >= self.x_min;
		let overlaps_y = other.y_min <= self.y_max && other.y_max >= self.y_min;
		let overlaps_z = other.z_min <= self.z_max && other.z_max >= self.z_min;

		if !(overlaps_x && overlaps_y && overlaps_z) {
			return None
		}

		let overlap_x_min = self.x_min.max(other.x_min);
		let overlap_x_max = self.x_max.min(other.x_max);

		let overlap_y_min = self.y_min.max(other.y_min);
		let overlap_y_max = self.y_max.min(other.y_max);

		let overlap_z_min = self.z_min.max(other.z_min);
		let overlap_z_max = self.z_max.min(other.z_max);

		return Some(Cuboid {
			layer: other.layer,
			x_min: overlap_x_min, x_max: overlap_x_max,
			y_min: overlap_y_min, y_max: overlap_y_max,
			z_min: overlap_z_min, z_max: overlap_z_max,
			is_on: false, // irrelevant
		})
	}

	fn from_str(line: &str, layer: i64) -> Cuboid {
		let parts = line.split(&[' ', '=', ',', '.'][..]).collect::<Vec<_>>();

		//println!("{:?}", parts);
		let x_min = parts[2].parse::<i64>().unwrap();
		let x_max = parts[4].parse::<i64>().unwrap();
		let y_min = parts[6].parse::<i64>().unwrap();
		let y_max = parts[8].parse::<i64>().unwrap();
		let z_min = parts[10].parse::<i64>().unwrap();
		let z_max = parts[12].parse::<i64>().unwrap();

		return Cuboid {
			layer,
			x_min, x_max,
			y_min, y_max,
			z_min, z_max,
			is_on: parts[0] == "on",
		}
	}
}

impl std::fmt::Debug for Cuboid {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		write!(f, "(x={}..{} y={}..{} z={}..{})",
			self.x_min, self.x_max,
			self.y_min, self.y_max,
			self.z_min, self.z_max,
		)
	}
}

fn parse(input: &str) -> CuboidList {
	input
		.lines()
		.enumerate()
		.map(|(layer, line)| Cuboid::from_str(line, layer as i64))
		.collect()
}

pub fn part1(input: String) -> String {
	let mut all_cuboids = parse(&input);
	all_cuboids.retain(|r| r.is_initialization_cube());

	let count = all_cuboids.iter().map(|r| r.count_on(&all_cuboids)).sum::<i64>();
	return count.to_string()
}

pub fn part2(input: String) -> String {
	let all_cuboids = parse(&input);

	let count = all_cuboids.iter().map(|r| r.count_on(&all_cuboids)).sum::<i64>();
	return count.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 22,
	input: "file:22-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("39", "file:22-input-test"),
		("590784", "file:22-input-test2"),
	],
	tests_part2: &[
		("2758514936282235", "file:22-input-test-part2"),
	],
};

