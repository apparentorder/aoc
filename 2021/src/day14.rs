use crate::aoc;
use std::collections::HashMap;

type Rules = HashMap<(char, char), char>;
type Counts = HashMap<char, i64>;
type Cache = HashMap<(char, char, i64), Counts>;

fn min_max(template: Vec<char>, rules: Rules, steps: i64) -> (i64, i64) {
	let mut counts = Counts::new();
	let mut cache = Cache::new();

	// count the elements we're starting with
	for &c in &template {
		add(&mut counts, c, 1);
	}

	// gather counts of elements added for each pair, and merge into our total element counts
	for pair_start in 0..(template.len() - 1) {
		let pair_counts = lookup_pair(&rules, &mut cache, steps, template[pair_start], template[pair_start + 1]);
		merge_counts_into(&mut counts, &pair_counts);
	}

	return (*counts.values().min().unwrap(), *counts.values().max().unwrap())
}

fn lookup_pair<'a>(rules: &Rules, cache: &'a mut Cache, steps: i64, element1: char, element2: char) -> &'a Counts {
	let cache_key = (element1, element2, steps);

	if cache.contains_key(&cache_key) {
		// borrow checker wouldn't let me do this easier
		return cache.get(&cache_key).unwrap()
	}

	if steps == 0 {
		// borrow checker wouldn't let me do this easier
		return cache.entry(cache_key).or_insert(Counts::new());
	}

	let new_element = *rules.get(&(element1, element2)).unwrap();

	// lookup counts for both resulting pairs
	let mut counts = lookup_pair(rules, cache, steps - 1, element1, new_element).clone();
	let counts_pair2 = lookup_pair(rules, cache, steps - 1, new_element, element2);
	merge_counts_into(&mut counts, &counts_pair2);

	add(&mut counts, new_element, 1);

	// borrow checker wouldn't let me do this easier
	return cache.entry(cache_key).or_insert(counts);
}

fn merge_counts_into(into_map: &mut Counts, from_map: &Counts) {
	for (&c, &count) in from_map {
		add(into_map, c, count);
	}
}

fn add(counts: &mut Counts, c: char, count: i64) {
	counts.entry(c)
		.and_modify(|e| *e += count )
		.or_insert(count);
}

fn parse(input: &str) -> (Vec<char>, Rules) {
	let mut r = Rules::new();

	let mut line_iter = input.lines();

	let template = line_iter.next().unwrap().chars().collect();
	line_iter.next(); // drop newline

	for rule in line_iter {
		// XY -> Z
		// 0123456
		let elements = rule.chars().collect::<Vec<_>>();
		r.insert((elements[0], elements[1]), elements[6]);
	}

	return (template, r)
}

pub fn part1(input: String) -> String {
	let (template, rules) = parse(&input);
	let (emin, emax) = min_max(template, rules, 10);
	return (emax - emin).to_string()
}

pub fn part2(input: String) -> String {
	let (template, rules) = parse(&input);
	let (emin, emax) = min_max(template, rules, 40);
	return (emax - emin).to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 14,
	input: "file:14-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("1588", "file:14-input-test"),
	],
	tests_part2: &[
		("2188189693529", "file:14-input-test"),
	],
};

