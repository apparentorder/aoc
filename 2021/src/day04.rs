use crate::aoc;

type Board = Vec<Vec<i32>>;

fn play(numbers: Vec<i32>, boards: Vec<Board>, find_last: bool) -> i32 {
	let mut last_number_index_by_board: Vec<Option<usize>> = vec![None; boards.len()];

	for (board_index, board) in boards.iter().enumerate() {
		for rowcol in 0..5 {
			// rows
			if let Some(wi) = winning_number_index(&numbers, &board[rowcol]) {
				if wi < last_number_index_by_board[board_index].unwrap_or(usize::MAX) {
					last_number_index_by_board[board_index] = Some(wi);
				}
			}

			// columns
			let column: Vec<i32> = board.iter().map(|row| *row.iter().nth(rowcol).unwrap()).collect();
			if let Some(wi) = winning_number_index(&numbers, &column) {
				if wi < last_number_index_by_board[board_index].unwrap_or(usize::MAX) {
					last_number_index_by_board[board_index] = Some(wi);
				}
			}
		}
	}

	let winning_board_last_number_index;
	if find_last {
		winning_board_last_number_index = last_number_index_by_board.iter().map(|&i| i.unwrap()).max().unwrap();
	} else {
		winning_board_last_number_index = last_number_index_by_board.iter().map(|&i| i.unwrap()).min().unwrap();
	}

	let winning_board_last_number = numbers[winning_board_last_number_index];
	let winning_board_index = last_number_index_by_board
		.iter()
		.position(|&lni| lni.unwrap() == winning_board_last_number_index)
		.unwrap();

	let mut unmarked_sum = 0;
	for row in &boards[winning_board_index] {
		for n in row {
			if !numbers[..=winning_board_last_number_index].contains(n) {
				unmarked_sum += n;
			}
		}
	}

	println!("winner board index {} unmarked sum {} last number {}",
		winning_board_index,
		unmarked_sum,
		winning_board_last_number);

	return unmarked_sum * winning_board_last_number;
}

fn winning_number_index(numbers: &Vec<i32>, row: &Vec<i32>) -> Option<usize> {
	let mut winning_indexes: Vec<usize> = vec![];

	for row_number in row {
		if let Some(i) = numbers.iter().position(|n| n == row_number) {
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

