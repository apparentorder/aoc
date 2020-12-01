
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
	// ...
]

