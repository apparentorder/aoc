use crate::aoc;

#[derive(Clone)]
struct Pair {
	left: Value,
	right: Value,
	depth: i32,
}

#[derive(Clone)]
enum Value {
	Number(i32),
	Pair(Box<Pair>),
}

#[derive(Debug)]
struct ExplosionResult {
	did_explode: bool,
	left: Option<i32>,
	right: Option<i32>,
}

enum Direction {
	Left,
	Right,
}

impl ExplosionResult {
	fn nope() -> ExplosionResult {
		ExplosionResult {
			did_explode: false,
			left: None,
			right: None,
		}
	}
}

impl Pair {
	fn increase_depth(&mut self) {
		self.depth += 1;
		self.left.increase_depth();
		self.right.increase_depth();
	}

	fn magnitude(&self) -> i32 {
		let mag_left = 3 * self.left.magnitude();
		let mag_right = 2 * self.right.magnitude();
		return mag_left + mag_right
	}

	fn add(&self, other: Pair) -> Pair {
		let pair_self = Value::Pair(Box::new(self.clone()));
		let pair_other = Value::Pair(Box::new(other.clone()));
		let mut pair = Pair { left: pair_self, right: pair_other, depth: 0 };
		pair.increase_depth();
		pair.reduce();
		return pair

		// clever but slower alternative:
		//let mut s = format!("[{:?},{:?}]", self, other);
		//return Pair::from_str(&s)
	}

	fn reduce(&mut self) {
		loop {
			if self.explode().did_explode {
				//println!("after explode: {:?}", self);
				continue
			}

			if self.split() {
				//println!("after split:   {:?}", self);
				continue
			}

			break
		}
	}

	fn split(&mut self) -> bool {
		return self.left.split(self.depth) || self.right.split(self.depth)
	}

	fn increase(&mut self, result: &mut ExplosionResult, coming_from: Direction) {
		match coming_from {
			Direction::Left => self.left.increase(result, coming_from),
			Direction::Right => self.right.increase(result, coming_from),
		}
	}

	fn explode(&mut self) -> ExplosionResult {
		let mut result_left = self.left.explode();
		if result_left.did_explode {
			self.right.increase(&mut result_left, Direction::Left);
			return result_left
		}

		let mut result_right = self.right.explode();
		if result_right.did_explode {
			self.left.increase(&mut result_right, Direction::Right);
			return result_right
		}

		return ExplosionResult::nope()
	}

	fn from_str(input: &str) -> Pair {
		let (mut n, _) = Pair::from_str_internal(input, 1);
		n.reduce();
		return n
	}

	fn from_str_internal(input: &str, depth: i32) -> (Pair, usize) {
		assert!(input.starts_with("["));

		let mut parsed_chars = 1;

		let (left, pc) = Value::from_str_internal(&input[parsed_chars..], depth + 1);
		parsed_chars += pc;

		assert!(&input[parsed_chars..=parsed_chars] == ",");
		parsed_chars += 1;

		let (right, pc) = Value::from_str_internal(&input[parsed_chars..], depth + 1);
		parsed_chars += pc;

		parsed_chars += 1; // final ']'

		let pair = Pair { left, right, depth };
		return (pair, parsed_chars)
	}

}

impl Value {
	fn increase_depth(&mut self) {
		match self {
			Value::Pair(pair) => pair.increase_depth(),
			Value::Number(_) => (),
		}
	}

	fn magnitude(&self) -> i32 {
		match self {
			Value::Pair(pair) => pair.magnitude(),
			Value::Number(number) => *number,
		}
	}

	fn increase(&mut self, result: &mut ExplosionResult, coming_from: Direction) {
		match self {
			Value::Pair(pair) => pair.increase(result, coming_from),
			Value::Number(number) => {
				let spillover;
				match coming_from {
					Direction::Left => {
						spillover = result.right;
						result.right = None;
					},
					Direction::Right => {
						spillover = result.left;
						result.left = None;
					},
					_ => panic!(),
				}

				if let Some(spillover) = spillover {
					*self = Value::Number(*number + spillover);
				}
			}
		}
	}

	fn split(&mut self, parent_depth: i32) -> bool {
		match self {
			Value::Number(n) => {
				if *n < 10 {
					return false
				}

				let half = *n as f32 / 2f32;
				let left = Value::Number(half.floor() as i32);
				let right = Value::Number(half.ceil() as i32);
				let pair = Pair { left, right, depth: parent_depth + 1 };
				*self = Value::Pair(Box::new(pair));
				return true
			},
			Value::Pair(n) => n.split(),
		}
	}

	fn explode(&mut self) -> ExplosionResult {
		if let Value::Pair(pair) = self {
			if pair.depth < 5 {
				return pair.explode();
			}

			let left = match pair.left {
				Value::Number(left) => left,
				_ => panic!(),
			};

			let right = match pair.right {
				Value::Number(right) => right,
				_ => panic!(),
			};

			*self = Value::Number(0);
			return ExplosionResult {
				did_explode: true,
				left: Some(left),
				right: Some(right),
			}
		}

		return ExplosionResult::nope();
	}

	fn from_str_internal(input: &str, depth: i32) -> (Value, usize) {
		//println!("ppv {}", input);
		if !input.starts_with("[") {
			return (Value::Number(input[0..=0].parse().unwrap()), 1)
		}

		let (pair, parsed) = Pair::from_str_internal(input, depth);
		return (Value::Pair(Box::new(pair)), parsed)
	}
}

impl std::fmt::Debug for Pair {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		//write!(f, "[{}:{:?},{:?}]", self.depth, self.left, self.right)
		write!(f, "[{:?},{:?}]", self.left, self.right)
	}
}

impl std::fmt::Debug for Value {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		match self {
			Value::Number(number) => write!(f, "{:?}", number),
			Value::Pair(pair) => write!(f, "{:?}", pair),
		}
	}
}

fn parse(input: &str) -> Vec<Pair> {
	let mut r = Vec::<Pair>::new();

	for line in input.lines() {
		let pair = Pair::from_str(line);
		r.push(pair);
	}

	return r
}

pub fn part1(input: String) -> String {
	let pairs = parse(&input);
	let mut sum = pairs[0].clone();
	for i in 1..pairs.len() {
		sum = sum.add(pairs[i].clone());
	}
	//println!("sum: {:?}", sum);
	return sum.magnitude().to_string()
}

pub fn part2(input: String) -> String {
	let pairs = parse(&input);

	let mut max_mag = 0;

	for a in &pairs {
		for b in &pairs {
			let mut sum = a.clone();
			sum = sum.add(b.clone());
			max_mag = max_mag.max(sum.magnitude());

			let mut sum = b.clone();
			sum = sum.add(a.clone());
			max_mag = max_mag.max(sum.magnitude());
		}
	}

	return max_mag.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 18,
	input: "file:18-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		//("_", "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"),
		("4140", "file:18-input-test"),
	],
	tests_part2: &[
		("3993", "file:18-input-test"),
	],
};

