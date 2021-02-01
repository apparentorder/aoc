class Day06: PuzzleClass {
	func decodeRepetition(_ input: [String], useLeastCommon: Bool = false) -> String {
		var r = Array(repeating: Character("_"), count: input[0].count)

		for pos in 0..<input[0].count {
			var letterCount = [Character:Int]()

			for code in input {
				let codeChars = Array(code)
				letterCount[codeChars[pos]] = (letterCount[codeChars[pos]] ?? 0) + 1
			}

			let filterValue = useLeastCommon ?
				letterCount.values.min()! :
				letterCount.values.max()!

			r[pos] = letterCount.filter { $0.value == filterValue }.first!.key
		}

		return String(r)
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return decodeRepetition(input.lines)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return decodeRepetition(input.lines, useLeastCommon: true)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "06-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "06-input-test"), result: "easter"),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "06-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "06-input-test"), result: "advent"),
			]
		),
	]

	required init() {}

}

