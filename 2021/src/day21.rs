use crate::aoc;
use std::collections::HashMap;

type Cache = HashMap<State, (i64, i64)>;

#[derive(Clone, Eq, PartialEq, Hash)]
struct State {
	pos1: i64,
	pos2: i64,
	score1: i64,
	score2: i64,
}

const DIRAC_ROLLS: &[i64; 27] = &[3, 4, 5, 4, 5, 6, 5, 6, 7, 4, 5, 6, 5, 6, 7, 6, 7, 8, 5, 6, 7, 6, 7, 8, 7, 8, 9];

fn play(pos1: i64, pos2: i64, max_score: i64) -> i64 {
	let mut dice = 1;
	let mut score1 = 0;
	let mut score2 = 0;
	let mut pos1 = pos1;
	let mut pos2 = pos2;
	let mut rolls = 0;

	loop {
		let mut step;

		step = roll(&mut dice);
		rolls += 3;
		pos1 = pos(pos1 + step);
		score1 += pos1;
		//println!("p1 rolls {} pos {} score {}", step, pos1, score1);
		if score1 >= max_score { break }

		step = roll(&mut dice);
		rolls += 3;
		pos2 = pos(pos2 + step);
		score2 += pos2;
		//println!("p2 rolls {} pos {} score {}", step, pos2, score2);
		if score2 >= max_score { break }
	}

	let loser = score1.min(score2);
	return loser * rolls
}

fn play2(state: &State, cache: &mut Cache, max_score: i64) -> (i64, i64, bool) {
	let mut wins1 = 0;
	let mut wins2 = 0;

	if let Some((w1,w2)) = cache.get(state) {
		return (*w1, *w2, true)
	}

	for roll1 in DIRAC_ROLLS {
		let pos1 = pos(state.pos1 + roll1);
		let score1 = state.score1 + pos1;

		if score1 >= max_score {
			wins1 += 1;
			continue
		}

		for roll2 in DIRAC_ROLLS {
			let pos2 = pos(state.pos2 + roll2);
			let score2 = state.score2 + pos2;

			if score2 >= max_score {
				wins2 += 1;
				continue
			}

			let next_state = State {
				pos1,
				pos2,
				score1,
				score2,
			};

			let (w1, w2, was_cached) = play2(&next_state, cache, max_score);
			if !was_cached {
				cache.insert(next_state, (w1, w2));
			}
			wins1 += w1;
			wins2 += w2;
		}
	}

	return (wins1, wins2, false)
}

fn pos(pos: i64) -> i64 {
	let mut pos = pos;
	while pos > 10 {
		pos -= 10;
	}
	return pos
}

fn roll(dice: &mut i64) -> i64 {
	let mut r = 0;
	for _ in 0..3 {
		r += *dice;
		*dice += 1;
		if *dice > 100 {
			*dice -= 100;
		}
	}

	return r
}

fn parse(input: &str) -> (i64, i64) {
	let pos = input.lines().map(|line| line.split_whitespace().last().unwrap().parse::<i64>().unwrap()).collect::<Vec<_>>();
	return (pos[0], pos[1])
}

pub fn part1(input: String) -> String {
	let (pos1, pos2) = parse(&input);
	return play(pos1, pos2, 1000).to_string();
}

pub fn part2(input: String) -> String {
	let (pos1, pos2) = parse(&input);
	let state = State {
		pos1,
		pos2,
		score1: 0,
		score2: 0,
	};
	let mut cache = Cache::new();
	let (w1, w2, _) = play2(&state, &mut cache, 21);
	return w1.max(w2).to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 21,
	input: "Player 1 starting position: 2\nPlayer 2 starting position: 1",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("739785", "Player 1 starting position: 4\nPlayer 2 starting position: 8"),
	],
	tests_part2: &[
		("444356092776315", "Player 1 starting position: 4\nPlayer 2 starting position: 8"),
	],
};

