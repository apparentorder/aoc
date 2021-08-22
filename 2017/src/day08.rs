use crate::aoc;
use std::collections::HashMap;

#[derive(Debug)]
enum Operation {
	Increment,
	Decrement,
}

#[derive(Debug)]
enum Comparison {
	Eq,
	Ne,
	Lt,
	Le,
	Gt,
	Ge,
}

#[derive(Debug)]
struct Instruction {
	register: String,
	operation: Operation,
	value: i32,
	condition_register: String,
	condition_comparison: Comparison,
	condition_value: i32,
}

fn exec(program: Vec<Instruction>) -> (HashMap<String, i32>, i32) {
	let mut registers: HashMap<String, i32> = HashMap::new();
	let mut highest_value: i32 = -2^31;

	for instruction in program {
		//println!("{:?}", instruction);
		if !check_condition(&instruction, &registers) {
			continue
		}

		let new_value = match instruction.operation {
			Operation::Increment => registers.get(&instruction.register).unwrap_or(&0) + instruction.value,
			Operation::Decrement => registers.get(&instruction.register).unwrap_or(&0) - instruction.value,
		};

		registers.insert(instruction.register.to_string(), new_value);

		if new_value > highest_value {
			highest_value = new_value;
		}
	}

	return (registers, highest_value)
}

fn check_condition(instruction: &Instruction, registers: &HashMap<String, i32>) -> bool {
	let lhs = registers.get(&instruction.condition_register).unwrap_or(&0);
	let rhs = instruction.condition_value;

	return match &instruction.condition_comparison {
		Comparison::Eq => (*lhs == rhs),
		Comparison::Ne => (*lhs != rhs),
		Comparison::Lt => (*lhs <  rhs),
		Comparison::Le => (*lhs <= rhs),
		Comparison::Gt => (*lhs >  rhs),
		Comparison::Ge => (*lhs >= rhs),
	}
}

fn parse(input: String) -> Vec<Instruction> {
	let mut r: Vec<Instruction> = vec![];

	for line in input.split("\n") {
		let mut parts = line.split_whitespace();

		let reg = parts.next().unwrap();

		let op = match parts.next().unwrap() {
			"inc" => Operation::Increment,
			"dec" => Operation::Decrement,
			_ => panic!("unknown operation"),
		};

		let value: i32 = parts.next().unwrap().parse().unwrap();

		let _ = parts.next().unwrap(); // drop "if"

		let cond_reg = parts.next().unwrap();

		let cond_op = match parts.next().unwrap() {
			"<"  => Comparison::Lt,
			"<=" => Comparison::Le,
			">"  => Comparison::Gt,
			">=" => Comparison::Ge,
			"==" => Comparison::Eq,
			"!=" => Comparison::Ne,
			_ => panic!("unknown comparison"),
		};

		let cond_value: i32 = parts.next().unwrap().parse().unwrap();

		r.push(Instruction{
			register: reg.to_string(),
			operation: op,
			value: value,
			condition_register: cond_reg.to_string(),
			condition_comparison: cond_op,
			condition_value: cond_value,
		});
	}

	return r
}

pub fn part1(input: String) -> String {
	let program = parse(input);
	let (registers, _) = exec(program);
	println!("{:?}", registers);
	return registers.values().max().unwrap().to_string();
}

pub fn part2(input: String) -> String {
	let program = parse(input);
	let (_, highest_value) = exec(program);
	return highest_value.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 08,
	input: "file:08-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("1", "file:08-input-test"),
	],
	tests_part2: &[
		("10", "file:08-input-test"),
	],
};

