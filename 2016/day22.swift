class Day22: PuzzleClass {
	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return -1
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return -2
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "22-input"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "22-test1"), result: 514579),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "22-input"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "22-test1"), result: 241861950),
			]
		),
	]

	required init() {}

}

