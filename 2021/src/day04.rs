use crate::aoc;

type Board = Vec<Vec<i32>>;

fn play(numbers: Vec<i32>, boards: Vec<Board>, find_last: bool) -> i32 {
	let mut last_number_index_by_board: Vec<usize> = vec![usize::MAX; boards.len()];

	// go through all board's rows and columns, checking each if it can win at all (all numbers
	// appear in `numbers`, i.e. will be actually drawn).
	//
	// as multiple rows/columns on each board might lead to a win, we take note of the first number
	// drawn that causes that board to win (indicated by the `numbers` index, which reflects the sequence
	// of numbers drawn).
	for (board_index, board) in boards.iter().enumerate() {
		for rowcol in 0..5 {
			// check all rows
			if let Some(wi) = winning_number_index(&numbers, &board[rowcol]) {
				if wi < last_number_index_by_board[board_index] {
					last_number_index_by_board[board_index] = wi;
				}
			}

			// check all columns
			let column: Vec<i32> = board.iter().map(|row| *row.iter().nth(rowcol).unwrap()).collect();
			if let Some(wi) = winning_number_index(&numbers, &column) {
				if wi < last_number_index_by_board[board_index] {
					last_number_index_by_board[board_index] = wi;
				}
			}
		}
	}

	// determine which board we're looking for (first vs. last board to win, for p1/p2 respectively)
	// and the actual last number drawn to win
	let wanted_last_number_index;
	if find_last {
		wanted_last_number_index = *last_number_index_by_board.iter().max().unwrap();
	} else {
		wanted_last_number_index = *last_number_index_by_board.iter().min().unwrap();
	}

	let wanted_last_number = numbers[wanted_last_number_index];
	let wanted_index = last_number_index_by_board.iter().position(|&lni| lni == wanted_last_number_index).unwrap();

	// now count the sum of all unmarked numbers, i.e. all those that do NOT appear
	// in the `numbers` sequence before the winning number
	let mut unmarked_sum = 0;
	for row in &boards[wanted_index] {
		for n in row {
			if !numbers[..=wanted_last_number_index].contains(n) {
				unmarked_sum += n;
			}
		}
	}

	println!("winner board index {} unmarked sum {} last number {}",
		wanted_index,
		unmarked_sum,
		wanted_last_number);

	return unmarked_sum * wanted_last_number;
}

fn winning_number_index(numbers: &Vec<i32>, candidate_numbers: &Vec<i32>) -> Option<usize> {
	// check any given row if it can win, and if so, which number (by index)
	// drawn causes it to win.

	let mut winning_indexes: Vec<usize> = vec![];

	for c in candidate_numbers {
		if let Some(i) = numbers.iter().position(|n| n == c) {
			winning_indexes.push(i);
		} else {
			return None
		}

	}

	return Some(*winning_indexes.iter().max().unwrap())
}

fn parse(input: String) -> (Vec<i32>, Vec<Board>) {
	let mut lines = input.split('\n');
	let numbers: Vec<i32> = lines.next().unwrap().split(',').map(|s| s.parse::<i32>().unwrap()).collect();
	let mut all_boards: Vec<Board> = vec![];

	while let Some(_empty_line) = lines.next() {
		let mut board: Board = vec![];

		for _ in 0..5 {
			let row: Vec<i32> = lines.next().unwrap().split_whitespace().map(|s| s.parse::<i32>().unwrap()).collect();
			board.push(row);
		}

		all_boards.push(board);
	}

	return (numbers, all_boards)
}

pub fn part1(input: String) -> String {
	let (numbers, boards) = parse(input);
	return play(numbers, boards, false).to_string()
}

pub fn part2(input: String) -> String {
	let (numbers, boards) = parse(input);
	return play(numbers, boards, true).to_string()
}

pub const PUZZLE_DATA: aoc::Puzzle = aoc::Puzzle {
	day: 4,
	input: "file:04-input",
	implementation_part1: part1,
	implementation_part2: part2,
	tests_part1: &[
		("4512", "file:04-input-test"),
	],
	tests_part2: &[
		("1924", "file:04-input-test"),
	],
};

