
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
			PuzzleTest(PuzzleInput(fromString: "12"), result: 2),
			PuzzleTest(PuzzleInput(fromString: "14"), result: 2),
			PuzzleTest(PuzzleInput(fromString: "1969"), result: 654),
			PuzzleTest(PuzzleInput(fromString: "100756"), result: 33583),
		]
	),
	"day01part2": Puzzle(
		implementation: Day01.part2,
		input: PuzzleInput(fromFile: "01-input"),
		tests: [
			PuzzleTest(PuzzleInput(fromString: "12"), result: 2),
			PuzzleTest(PuzzleInput(fromString: "1969"), result: 966),
			PuzzleTest(PuzzleInput(fromString: "100756"), result: 50346),
		]
	),

	// DAY 02
	// ...
]

