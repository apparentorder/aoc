use crate::aoc;
use std::collections::HashSet;

type Grid = HashSet<Coord>;
type Coord = (i32, i32);
type Folds = Vec<Coord>;

fn fold(old_grid: Grid, folds: Folds) -> Grid {
	let mut grid = old_grid.clone();

	for (fold_x, fold_y) in folds {
		let mut new_grid = grid.clone();

		for &(dot_x, dot_y) in &grid {
			if fold_x == -1 && dot_y > fold_y {
				new_grid.insert((dot_x, fold_y - (dot_y - fold_y)));
				new_grid.remove(&(dot_x, dot_y));
			} else if fold_y == -1 && dot_x > fold_x {
				new_grid.insert((fold_x - (dot_x - fold_x), dot_y));
				new_grid.remove(&(dot_x, dot_y));
			}
		}

		grid = new_grid;
	}

	return grid
}

fn print_grid(grid: Grid) {
	let max_x = grid.iter().map(|&(x, _)| x).max().unwrap();
	let max_y = grid.iter().map(|&(_, y)| y).max().unwrap();

	for y in 0..=max_y {
		let line = (0..=max_x).map(|x| if grid.contains(&(x, y)) { '#' } else { '.' }).collect::<String>();
		println!("{}", line);
	}
}

fn parse(input: &str) -> (Grid, Folds) {
	let mut grid = Grid::new();
	let mut folds = Folds::new();

	for line in input.lines() {
		if line == "" {
			continue
		}

		let parts = line.split(&[' ', ',', '='][..]).collect::<Vec<_>>();

		if parts[0] == "fold" {
			let v = parts[3].parse::<i32>().unwrap();
			let c = if parts[2] == "x" { (v, -1) } else { (-1, v) };
			folds.push(c);
			continue
		}

		grid.insert((parts[0].parse().unwrap(), parts[1].parse().unwrap()));
	}

	//println!("grid {:?}", grid);
	//println!("folds {:?}", folds);
	return (grid, folds)
}

pub fn part1(input: String) -> String {
	let (grid, folds) = parse(&input);
	let first_fold = [folds.into_iter().nth(0).unwrap()].to_vec();
	let folded_grid = fold(grid, first_fold);
	return folded_grid.len().to_string()
}

pub fn part2(input: String) -> String {
	let (grid, folds) = parse(&input);
	let folded_grid = fold(grid, folds);
	print_grid(folded_grid);
	return 0.to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 13,
	input: "file:13-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("17", "file:13-input-test"),
	],
	tests_part2: &[
	],
};

