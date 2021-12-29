use crate::aoc;

#[derive(Debug)]
struct Parameters {
	add_to_x: Vec<i64>,
	add_to_y: Vec<i64>,
	div: Vec<i64>,
}

fn find_model_number(number: i64, z_input: i64, params: &Parameters, find_min: bool) -> Option<i64> {
	let position = if number == 0 { 0 } else { (number as f64).log10().floor() as usize + 1 };

	if position == 14 {
		return match z_input {
			0 => Some(number),
			_ => None,
		}
	}

	// `z` is reduced at each position *sometimes* (params.div[pos] says either /1 or /26)
	// but `z` is increased always when x!=w, i.e. in almost all cases: z*26 + w + add_to_y
	// many `x` values will not even be in a range 1..=9 and therefore can never match digit `w`.
	//
	// strategy: take every chance to pick the exact `w` that produces x==w,
	// so `z` will finally become zero again at the last position (so the model number is valid).
	// brute force all other digits.

	let x = (z_input % 26) + params.add_to_x[position];

	let reverse_digits;
	let digits_range;
	if (1..=9).contains(&x) {
		// we can pick our exact `w`
		digits_range = x..=x;
		reverse_digits = false;
	} else {
		digits_range = 1..=9;
		reverse_digits = !find_min;
	}

	for w in digits_range {
		// sadly, this is the least painful way to have a dynamic and reversible Range
		let w = if reverse_digits { 10 - w } else { w };

		let mut z = z_input;
		z /= params.div[position];

		if w != x {
			z *= 26;
			z += w + params.add_to_y[position];
		}

		// check that this `z` can finish, else continue
		// note that each iteration can have exactly two outcomes:
		// - z/div[pos] for x==w (meaning any z%26 is carried forward for /1, or zero for /26), or
		// - z/div[pos] * 26 + w + add_to_y, in which case z%26 is replaced
		//   (but it's never >=26, so a future z/26 will be unaffected either way!)
		let mut z_end = z;
		for remaining_position in (position+1)..=13 {
			z_end /= params.div[remaining_position];
			if params.add_to_x[remaining_position] > 9 {
				// for add_to_x>9, x==w can never be true
				z_end *= 26;
			}
		}

		if z_end > 0 {
			continue
		}

		let next_number = number * 10 + w;
		if let Some(valid_number) = find_model_number(next_number, z, params, find_min) {
			return Some(valid_number)
		}
	}

	return None
}

// for reference: this is the plain algorithm for each digit
fn _z_at(pos: usize, z: i64, w: i64, params: &Parameters) -> i64 {
	let mut z = z;

	let x = (z % 26) + params.add_to_x[pos];
	z /= params.div[pos];

	if x != w {
		z *= 26;
		z += w + params.add_to_y[pos];
	}

	//println!("z_at pos{} w{} z_in {} z_out {}", pos, w, zstart, z);
	return z
}

fn extract_parameters(input: &str) -> Parameters {
	let mut add_to_x = Vec::<i64>::new();
	let mut add_to_y = Vec::<i64>::new();
	let mut div = Vec::<i64>::new();

	let mut read_next_y = false;
	for line in input.lines() {
		let parts = line.split_whitespace().collect::<Vec<_>>();

		// first parameter: "add x" after "div z"
		if parts[0] == "add" && parts[1] == "x" && parts[2] != "z" {
			if parts[2] != "z" {
				add_to_x.push(parts[2].parse().unwrap());
			}
		}

		// second parameter: "add y" immediately after "add y w"
		// (we keep track of the latter to know which "add y" to use)
		if parts[0] == "add" && parts[1] == "y" {
			if read_next_y {
				add_to_y.push(parts[2].parse().unwrap());
				read_next_y = false;
			} else if parts[2] == "w" {
				read_next_y = true;
			}
		}

		// third parameter: the (only) "div" instruction right after "mod x 26".
		if parts[0] == "div" {
			div.push(parts[2].parse().unwrap());
		}
	}

	return Parameters { add_to_x, add_to_y, div }
}

pub fn part1(input: String) -> String {
	let params = extract_parameters(&input);
	return find_model_number(0, 0, &params, false).unwrap().to_string()
}

pub fn part2(input: String) -> String {
	let params = extract_parameters(&input);
	return find_model_number(0, 0, &params, true).unwrap().to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 24,
	input: "file:24-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("99598963999971", "file:24-input-penny"),
	],
	tests_part2: &[
		("93151411711211", "file:24-input-penny"),
	],
};

