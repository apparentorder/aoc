use crate::aoc;

// key insight: the scanners' up-and-down movements can be interpreted as a
// circle, i.e. a scanner reaches its top position every (range*2 - 2) cycles.
//
// as a packet always travels at one "depth" per time index, depth and time are
// the same (plus delay, for part 2).

type Layers = Vec<i32>;

fn severity(layers: &Layers, delay: i32) -> i32 {
	let mut severity = 0;

	for (depth, range) in layers.iter().enumerate() {
		if *range == 0 { continue }

		let circle_range = range * 2 - 2;
		let delayed_depth = depth as i32 + delay;

		if delayed_depth % circle_range == 0 {
			// caught!
			// note for part 2: we may get caught at depth 0, which would
			// be a severity of zero for (range*depth), yet violates the
			// part 2 rule "don't get caught". for the example, this condition
			// occurs at depth=4.
			// therefore, we add delay to the severity calculation.
			severity += range * delayed_depth;

			// no need to keep going for part 2
			if delay > 0 { break }
		}
	}

	return severity
}

fn _scanner_position(layers: &Layers, depth: usize, time: i32) -> Option<i32> {
	// this turned out to be superfluous but demonstrates the circle concept.

	let range = layers[depth];

	match range {
		0 => return None,
		1 => return Some(1),
		_ => {},
	}

	let circle_range = range * 2 - 2;
	let mut pos = time % circle_range;
	if pos >= range {
		pos = circle_range - pos;
	}

	return Some(pos)
}

fn parse(input: String) -> Layers {
	let lines: Vec<String> = input.split("\n").map(|s| s.to_string()).collect();
	let max_layer: usize = lines.last().unwrap().split(":").next().unwrap().parse().unwrap();
	let mut r: Layers = vec![0; max_layer + 1];

	for mut line in lines {
		line.retain(|c| c != ':');
		let mut parts = line.split_whitespace();
		let depth: usize = parts.next().unwrap().parse().unwrap();
		let range: i32 = parts.next().unwrap().parse().unwrap();

		r[depth] = range;
	}

	return r
}

fn _run(layers: &Layers) {
	for time in 0..=10 {
		println!("t={}", time);
		for depth in 0..layers.len() {
			println!("depth {} scanner at {:?}", depth, _scanner_position(&layers, depth, time));
		}
		println!();
	}
}

pub fn part1(input: String) -> String {
	let layers = parse(input);
	// println!("{:?}", layers);
	// _run(&layers);
	return severity(&layers, 0).to_string();
}

pub fn part2(input: String) -> String {
	let layers = parse(input);

	let mut i = 0;
	loop {
		if severity(&layers, i) == 0 {
			return i.to_string()
		}

		i += 1;
	}
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 13,
	input: "file:13-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("24", "file:13-input-test"),
	],
	tests_part2: &[
		("10", "file:13-input-test"),
	],
};

