use crate::aoc;
use std::collections::HashMap;

// note that some of this code wouldn't be necessary; it's lazily copied from the "tablet" (day18).
// the interesting bits for part 2 are in run2().

type Program = Vec<Instruction>;
type Registers = HashMap<char, i64>;

#[derive(Debug)]
struct State {
	id: i64,
	iptr: i64,
	reg: Registers,
	mul_count: i64,
}

#[derive(Debug)]
struct Instruction {
	operation: String,
	arg1: RegisterOrValue,
	arg2: RegisterOrValue,
}

#[derive(Debug, PartialEq)]
enum RegisterOrValue {
	Register(char),
	Value(i64),
	None,
}

impl State {
	fn new() -> State {
		return State {
			id: 0,
			iptr: 0,
			reg: HashMap::new(),
			mul_count: 0
		};
	}
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

fn run(program: &Program, state: &mut State) {
	loop {
		if !(0..program.len() as i64).contains(&state.iptr) {
			println!("program id {} terminated (iptr out of bounds)", state.id);
			return
		}

		let instruction = &program[state.iptr as usize];

		//println!("iptr = {} reg = {:?} instruction = {:?}", state.iptr, state.reg, instruction);

		match instruction.operation.as_str() {
			"set" => {
				let reg = instruction.arg1.to_char();
				let value = instruction.arg2.to_i64(&state.reg);
				state.reg.insert(reg, value);
				state.iptr += 1;
			},
			"sub" => {
				let reg = instruction.arg1.to_char();
				let value1 = instruction.arg1.to_i64(&state.reg);
				let value2 = instruction.arg2.to_i64(&state.reg);
				state.reg.insert(reg, value1 - value2);
				state.iptr += 1;
			},
			"mul" => {
				let reg = instruction.arg1.to_char();
				let value1 = instruction.arg1.to_i64(&state.reg);
				let value2 = instruction.arg2.to_i64(&state.reg);
				state.reg.insert(reg, value1 * value2);
				state.iptr += 1;
				state.mul_count += 1;
			},
			"jnz" => {
				state.iptr += if instruction.arg1.to_i64(&state.reg) != 0 {
					instruction.arg2.to_i64(&state.reg)
				} else {
					1
				};
			},
			_ => panic!(),
		};
	}
}

fn is_prime(n: i64) -> bool {
	// shamelessly taken from https://en.wikipedia.org/wiki/Primality_test

	if n <= 3 {
		return n > 1
	}

	if n % 2 == 0 || n % 3 == 0 {
		return false
	}

	let mut i: i64 = 5;

	while i.pow(2) <= n {
		if n % i == 0 || n % (i + 2) == 0 {
			return false
		}

		i += 6;
	}

	return true
}

fn run2(state: &mut State, step_size: i64) -> i64 {
	let mut b = *state.reg.get(&'b').unwrap();
	let c = *state.reg.get(&'c').unwrap();
	let mut h: i64 = 0;

	println!("b={} c={} step={}", b, c, step_size);

	while b <= c {
		if !is_prime(b) {
			h += 1;
		}

		b += step_size;
	}

	return h
}

	/* scratch pad
	loop {
		f = 1;
		d = 2;
		while (d - b) != 0 {
			// the inner loop (changing `f`) is effectively a test if any `d` is
			// an even divisor for `b`.
			if b % d == 0 {
				f = 0
			}
			//e = 2;
			//while (e - b) != 0 {
			//	if (d * e) - b == 0 {
			//		f = 0;
			//	}
			//
			//	e += 1;
			//}
			d += 1;
		}

		if f == 0 {
			h += 1;
		}

		if (b - c) == 0 {
			return h
		}

		b += 17; // => 1_000 main loops
	}
	*/

pub fn part1(input: String) -> String {
	let program = parse(input);
	let mut state = State::new();

	run(&program, &mut state);
	return state.mul_count.to_string()
}

pub fn part2(input: String) -> String {
	let mut program = parse(input);
	let mut state = State::new();

	// extract step size from parsed program (last `sub` instruction for register `b`)
	let ss_instruction = program
		.iter()
		.filter(|i| i.operation == "sub" && i.arg1 == RegisterOrValue::Register('b'))
		.last()
		.unwrap();

	let step_size = match ss_instruction.arg2 {
		RegisterOrValue::Value(x) => x * -1, // we'll be adding the step size, so *-1
		_ => panic!(),
	};

	// truncate program: remove everything at and after "set f" (this is where the main loop starts)
	let loop_start = program.iter().position(|i| i.operation == "set" && i.arg1 == RegisterOrValue::Register('f')).unwrap();
	let _foo = program.split_off(loop_start);

	// adjust `a` to `1`, per puzzle
	state.reg.insert('a', 1);

	// run the truncated program, only to determine initial values of `b` and `c`
	run(&program, &mut state);

	return run2(&mut state, step_size).to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 23,
	input: "file:23-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
	],
	tests_part2: &[
	],
};

