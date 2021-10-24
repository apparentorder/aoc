use crate::aoc;
use std::collections::HashMap;

type Program = Vec<Instruction>;
type Registers = HashMap<char, i64>;

#[derive(Debug)]
struct State {
	id: i64,
	iptr: i64,
	frequency: i64,
	reg: Registers,
	queue: Vec<i64>,
	send_count: i64,
	running: bool,
}

#[derive(Debug)]
struct Instruction {
	operation: String,
	arg1: RegisterOrValue,
	arg2: RegisterOrValue,
}

#[derive(Debug)]
enum RegisterOrValue {
	Register(char),
	Value(i64),
	None,
}

impl RegisterOrValue {
	fn from_opt_str(s: Option<&str>) -> RegisterOrValue {
		if let Some(operand_string) = s {
			let operand_char = operand_string.chars().nth(0).unwrap();
			if ('a'..='z').contains(&operand_char) {
				return RegisterOrValue::Register(operand_char)
			} else {
				return RegisterOrValue::Value(operand_string.parse().unwrap())
			};
		}

		return RegisterOrValue::None
	}

	fn to_char(&self) -> char {
		match self {
			RegisterOrValue::Register(c) => *c,
			_ => panic!(),
		}
	}

	fn to_i64(&self, reg: &Registers) -> i64 {
		match self {
			RegisterOrValue::Register(c) => *reg.get(c).unwrap_or(&0),
			RegisterOrValue::Value(i) => *i,
			RegisterOrValue::None => panic!(),
		}
	}
}

fn parse(input: String) -> Program {
	let mut r: Program = vec![];

	for line in input.split('\n') {
		let mut parts =  line.split_whitespace();
		let op = parts.next().unwrap();
		let arg1 = RegisterOrValue::from_opt_str(parts.next());
		let arg2 = RegisterOrValue::from_opt_str(parts.next());

		r.push(Instruction{ operation: op.to_string(), arg1: arg1, arg2: arg2 });
	}

	return r
}

fn run(program: &Program, state: &mut State) -> Vec<i64> {
	let mut send_queue: Vec<i64> = vec![];

	loop {
		if !(0..program.len() as i64).contains(&state.iptr) {
			println!("program id {} terminated (iptr out of bounds)", state.id);
			state.running = false;
			return send_queue
		}

		let instruction = &program[state.iptr as usize];

		//println!("iptr = {} reg = {:?} instruction = {:?}", state.iptr, state.reg, instruction);

		match instruction.operation.as_str() {
			"snd" => {
				//println!("id{} send {}", state.id, instruction.arg1.to_i64(&state.reg));
				send_queue.push(instruction.arg1.to_i64(&state.reg));
				state.send_count += 1;
				state.iptr += 1;
			},
			"set" => {
				let reg = instruction.arg1.to_char();
				let value = instruction.arg2.to_i64(&state.reg);
				state.reg.insert(reg, value);
				state.iptr += 1;
			},
			"add" => {
				let reg = instruction.arg1.to_char();
				let value1 = instruction.arg1.to_i64(&state.reg);
				let value2 = instruction.arg2.to_i64(&state.reg);
				state.reg.insert(reg, value1 + value2);
				state.iptr += 1;
			},
			"mul" => {
				let reg = instruction.arg1.to_char();
				let value1 = instruction.arg1.to_i64(&state.reg);
				let value2 = instruction.arg2.to_i64(&state.reg);
				state.reg.insert(reg, value1 * value2);
				state.iptr += 1;
			},
			"mod" => {
				let reg = instruction.arg1.to_char();
				let value1 = instruction.arg1.to_i64(&state.reg);
				let value2 = instruction.arg2.to_i64(&state.reg);
				state.reg.insert(reg, value1 % value2);
				state.iptr += 1;
			},
			"rcv" => {
				// here, it *should* read:
				//
				//     if instruction.arg1.to_i64(&state.reg) != 0 { ...
				//
				// but this must not be present for part 2 and does make no difference for part 1,
				// so we ignore this.

				if state.queue.len() == 0 {
					// n.b.: we don't advance iptr so the next run() will restart here
					//println!("id{} empty receive", state.id);
					return send_queue
				}

				state.reg.insert(instruction.arg1.to_char(), state.queue.remove(0));
				//println!("id{} received {}", state.id, state.reg[&instruction.arg1.to_char()]);
				state.iptr += 1;
			},
			"jgz" => {
				state.iptr += if instruction.arg1.to_i64(&state.reg) > 0 {
					instruction.arg2.to_i64(&state.reg)
				} else {
					1
				};
			},
			_ => panic!(),
		};
	}
}

pub fn part1(input: String) -> String {
	let program = parse(input);
	let mut state0 = State{ id: 0, iptr: 0, frequency: 0, reg: HashMap::new(), queue: vec![], running: true, send_count: 0 };

	return run(&program, &mut state0).last().unwrap().to_string()
}

pub fn part2(input: String) -> String {
	let program = parse(input);

	let mut reg0 = HashMap::new();
	let mut reg1 = HashMap::new();
	reg0.insert('p', 0);
	reg1.insert('p', 1);

	let mut state0 = State{ id: 0, iptr: 0, frequency: 0, reg: reg0, queue: vec![], running: true, send_count: 0 };
	let mut state1 = State{ id: 1, iptr: 0, frequency: 0, reg: reg1, queue: vec![], running: true, send_count: 0 };

	loop {
		let mut queue0 = run(&program, &mut state0);
		state1.queue.append(&mut queue0);

		let mut queue1 = run(&program, &mut state1);
		state0.queue.append(&mut queue1);

		// if both instances are stopped OR both queues have run dry, we're done.
		if (!state0.running && !state1.running) || state0.queue.len() + state1.queue.len() == 0 {
			return state1.send_count.to_string()
		}
	}
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 18,
	input: "file:18-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("4", "file:18-input-test"),
	],
	tests_part2: &[
		("3", "file:18-input-test-part2"),
	],
};

