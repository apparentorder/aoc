
// this is the mapping from puzzle input and test results to individual implementations,
// i.e. this is basically a config file.

typealias PuzzleResult = Int

struct Puzzle {
	var implementation: ((PuzzleInput) -> PuzzleResult)
	var input: PuzzleInput
	var tests: [PuzzleTest]
}

var Puzzles = [
	// DAY 01
	"day01part1": Puzzle(
		implementation: Day01.part1,
		input: PuzzleInput(fromFile: "01-input"),
		tests: [
			PuzzleTest(PuzzleInput(fromFile: "01-test1"), result: 514579),
		]
	),
	"day01part2": Puzzle(
		implementation: Day01.part2,
		input: PuzzleInput(fromFile: "01-input"),
		tests: [
			PuzzleTest(PuzzleInput(fromFile: "01-test1"), result: 241861950),
		]
	),

	// DAY 02
	"day02part1": Puzzle(
		implementation: Day02.part1,
		input: PuzzleInput(fromFile: "02-input"),
		tests: [
			PuzzleTest(PuzzleInput(fromFile: "02-input-test"), result: 2),
		]
	),
	"day02part2": Puzzle(
		implementation: Day02.part2,
		input: PuzzleInput(fromFile: "02-input"),
		tests: [
			PuzzleTest(PuzzleInput(fromFile: "02-input-test"), result: 1),
		]
	),

	// DAY 03
	"day03part1": Puzzle(
		implementation: Day03.part1,
		input: PuzzleInput(fromFile: "03-input"),
		tests: [
			PuzzleTest(PuzzleInput(fromFile: "03-input-test1"), result: 7),
		]
	),
	"day03part2": Puzzle(
		implementation: Day03.part2,
		input: PuzzleInput(fromFile: "03-input"),
		tests: [
			PuzzleTest(PuzzleInput(fromFile: "03-input-test1"), result: 336),
		]
	),

	// DAY 04
	"day04part1": Puzzle(
		implementation: Day04.part1,
		input: PuzzleInput(fromFile: "04-input"),
		tests: [
			PuzzleTest(PuzzleInput(fromFile: "04-input-test1"), result: 2),
		]
	),
	"day04part2": Puzzle(
		implementation: Day04.part2,
		input: PuzzleInput(fromFile: "04-input"),
		tests: [
			PuzzleTest(PuzzleInput(fromFile: "04-input-test-invalid"), result: 0),
			PuzzleTest(PuzzleInput(fromFile: "04-input-test-valid"), result: 4),
		]
	),

	// DAY 05
	"day05part1": Puzzle(
		implementation: Day05.part1,
		input: PuzzleInput(fromFile: "05-input"),
		tests: [
			PuzzleTest(PuzzleInput(fromString: "FBFBBFFRLR"), result: 357),
			PuzzleTest(PuzzleInput(fromString: "BFFFBBFRRR"), result: 567),
			PuzzleTest(PuzzleInput(fromString: "FFFBBBFRRR"), result: 119),
			PuzzleTest(PuzzleInput(fromString: "BBFFBBFRLL"), result: 820),
		]
	),
	"day05part2": Puzzle(
		implementation: Day05.part2,
		input: PuzzleInput(fromFile: "05-input"),
		tests: []
	),

]

