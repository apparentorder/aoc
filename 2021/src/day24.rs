use crate::aoc;
use std::collections::HashMap;

type Memory = HashMap<char, i64>;
type Program<'a> = Vec<Instruction<'a>>;
type InputList = Vec<i64>;

#[derive(Debug)]
struct Instruction<'a> {
	command: &'a str,
	args: Vec<&'a str>,
}

impl Instruction<'_> {
	fn from_str(input: &str) -> Instruction {
		let mut parts = input.split_whitespace().collect::<Vec<_>>();
		let command = parts.remove(0);
		let args = parts;
		return Instruction {
			command,
			args,
		}
	}
}

fn read(memory: &Memory, key: &str) -> i64 {
	if let Ok(i) = key.parse() {
		return i
	}

	return *memory.get(&char(key)).unwrap_or(&0)
}

fn write(memory: &mut Memory, target: char, value: i64) {
	memory.insert(target, value);
}

fn char(s: &str) -> char {
	s.chars().nth(0).unwrap()
}

fn run(program: &Program, memory: &mut Memory, inputs: &InputList) {
	let mut inputs = inputs.clone();

	for instruction in program {
		println!("r {:?}", memory);
		println!("i {:?}", instruction);
		let value = match instruction.command {
			"inp" => inputs.remove(0),
			"add" => read(memory, instruction.args[0]) + read(memory, instruction.args[1]),
			"mul" => read(memory, instruction.args[0]) * read(memory, instruction.args[1]),
			"div" => read(memory, instruction.args[0]) / read(memory, instruction.args[1]),
			"mod" => read(memory, instruction.args[0]) % read(memory, instruction.args[1]),
			"add" => read(memory, instruction.args[0]) + read(memory, instruction.args[1]),
			"eql" => (read(memory, instruction.args[0]) == read(memory, instruction.args[1])) as i64,
			_ => panic!("unknown: {}", instruction.command),
		};

		let target = char(instruction.args[0]);
		write(memory, target, value);
	}
}

fn run2(program: &Program, inputs: &InputList, add1: &Vec<i64>, add2: &Vec<i64>, div: &Vec<i64>) -> i64{
	///for (i, &w) in inputs.iter().enumerate() {

	for i in 1..=9 {
		let z = zz(0, i, 12, add1, add2, div);
		if z==0 {
			println!("last: {}", z);
		}
	}

	return 0
}

fn getz(digits_so_far: &Vec<i64>, add1: &Vec<i64>, add2: &Vec<i64>, div: &Vec<i64>) -> Vec<i64> {
	let mut r = Vec::<i64>::new();

	//println!("getz: {:?}", digits_so_far);
	let mut z = 0;
	for (i, &w) in digits_so_far.iter().enumerate() {
		let x;
		x = (z % 26) + add1[i];
		z = z / div[i]; // 0|1 for z<26*2

		if z > 26*8 {
			// can never be zero again
			//println!("excess z: {}", z);
			return r
		}

		if x!=w {
			z *= 26;
			z += w+add2[i];
		}
	}

	if digits_so_far.len() == 14 {
		if z == 0 {
			//println!("match {:?}", digits_so_far);
			let digits_string = digits_so_far.iter().map(|&d| (d as u8+48) as char).collect::<String>();
			r.push(digits_string.parse().unwrap());
		} else {
			//println!("no match");
		}
		return r
	}

	for digit in 1..=9 {
		let mut next_digits = digits_so_far.clone();
		next_digits.push(digit);
		r.extend(getz(&next_digits, add1, add2, div));
	}

	return r
}

fn zz(z: i64, w: i64, digit_pos: usize, add1: &Vec<i64>, add2: &Vec<i64>, div: &Vec<i64>) -> i64 {
	return 0
}

fn parse(input: &str) -> Program {
	input.lines().map(|l| Instruction::from_str(l)).collect()
}

pub fn part1(input: String) -> String {
	let program = parse(&input);
	let mut variables = Memory::new();

	let mut add1 = Vec::<i64>::new();
	let mut div = Vec::<i64>::new();
	let mut add2 = Vec::<i64>::new();

	let mut read_next_y = false;
	for instruction in &program {
		//println!("{:?}", instruction);
		if instruction.command == "add" && instruction.args[0] == "x" {
			if instruction.args[1] != "z" {
				add1.push(instruction.args[1].parse().unwrap());
			}
		}
		if instruction.command == "add" && instruction.args[0] == "y" {
			if read_next_y {
				add2.push(instruction.args[1].parse().unwrap());
				read_next_y = false;
			}
			if instruction.args[1] == "w" {
				read_next_y = true;
			}
		}
		if instruction.command == "div" {
			div.push(instruction.args[1].parse().unwrap());
		}
	}

	let input = "13579246899999".chars().map(|c| (c as u8 - 48) as i64).collect::<Vec<_>>();
	//let x = run2(&program, &input, &add1, &add2, &div);
	let numbers = getz(&Vec::<i64>::new(), &add1, &add2, &div);
	return numbers.iter().min().unwrap().to_string()
}

pub fn part2(input: String) -> String {
	let _ = input;
	return 0.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 24,
	input: "file:24-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		//("0", "file:24-input-test"),
	],
	tests_part2: &[
	],
};

