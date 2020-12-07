class Day08: PuzzleClass {
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
			input: PuzzleInput(fromFile: "08-input"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "08-input-test"), result: 42),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "08-input"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "08-input-test"), result: 42),
			]
		),
	]

	required init() {}
}

