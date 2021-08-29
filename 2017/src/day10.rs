use crate::aoc;

fn hash(input: Vec<usize>, string_length: usize, times: usize) -> Vec<usize> {
	let mut string: Vec<usize> = (0..string_length).collect();
	let mut current_position = 0;
	let mut skip_size = 0;

	for _ in 0..times {
		for length in &input {
			assert!(length <= &string_length, "too beaucoup: {}", length);

			for position_add in 0..length/2 {
				let pos1 = (current_position + position_add) % string_length;
				let pos2 = (current_position + length - position_add - 1) % string_length;
				//println!("swap: pos1={} v1={} <-> pos2={} v2={}", pos1, string[pos1], pos2, string[pos2]);

				let swap = string[pos1];
				string[pos1] = string[pos2];
				string[pos2] = swap;
			}

			current_position = (current_position + length + skip_size) % string_length;
			skip_size += 1;

			//println!("after l={}: {:?}", length, string);
		}
	}

	return string
}

fn parse_usize(input: String) -> Vec<usize> {
	let mut r: Vec<usize> = vec![];

	for l in input.split(|c| !(c >= '0' && c <= '9')) {
		let n: usize = l.parse().unwrap();
		r.push(n);
	}

	return r
}

fn parse_ascii(input: String) -> Vec<usize> {
	input.chars().map(|c| c as usize).collect()
}

pub fn part1(input: String) -> String {
	let lengths = parse_usize(input);

	// string length is 5 for test input but 256 for the real input
	let string_length = if lengths.len() < 6 { 5 } else { 256 };

	let hash = hash(lengths, string_length, 1);

	let check = hash[0] * hash[1];
	return check.to_string();
}

pub fn part2(input: String) -> String {
	let string_length = 256;

	let mut lengths = parse_ascii(input);
	lengths.extend([17, 31, 73, 47, 23]);

	let sparse_hash = hash(lengths, string_length, 64);

	let mut dense_hash: Vec<usize> = vec![0; string_length / 16];

	for block in 0 .. string_length / 16 {
		for i in 0..16 {
			dense_hash[block] ^= sparse_hash[block*16 + i];
		}
	}

	return dense_hash.iter().map(|b| format!("{:02x}", b)).collect()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 10,
	input: "192,69,168,160,78,1,166,28,0,83,198,2,254,255,41,12",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("12", "3,4,1,5"),
	],
	tests_part2: &[
		("a2582a3a0e66e6e86e3812dcb672a272", ""),
		("33efeb34ea91902bb2f59c9920caa6cd", "AoC 2017"),
		("3efbe78a8d82f29979031a4aa0b16a9d", "1,2,3"),
		("63960835bcdc130f0b66d7ff4f6a5a8e", "1,2,4"),
	],
};

