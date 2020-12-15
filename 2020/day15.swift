class Day15: PuzzleClass {
	func numbers(_ input: PuzzleInput, maxTurns: Int) -> PuzzleResult {
		var numberLastSpoken: [Int] = Array(repeating: 0, count: maxTurns + 1)

		for (turn, number) in input.intArray.enumerated() {
			numberLastSpoken[number] = turn + 1
		}

		var turn = input.intArray.count
		var previousNumber = input.intArray.last!
		while true {
			turn += 1

			let lastSpoken = numberLastSpoken[previousNumber]
			let numberToSpeak = lastSpoken == 0 ? 0 : (turn - 1 - lastSpoken)
			debug("Turn \(turn): speaking \(numberToSpeak) (previous: \(previousNumber), on turn \(lastSpoken))")

			numberLastSpoken[previousNumber] = turn - 1
			previousNumber = numberToSpeak

			guard turn < maxTurns else {
				return numberToSpeak
			}
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return numbers(input, maxTurns: 2020)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return numbers(input, maxTurns: 30_000_000)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromString: "12,1,16,3,11,0"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "0,3,6"), result: 436),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromString: "12,1,16,3,11,0"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "0,3,6"), result: 175594),
				PuzzleTest(PuzzleInput(fromString: "1,3,2"), result: 2578),
				PuzzleTest(PuzzleInput(fromString: "2,1,3"), result: 3544142),
				PuzzleTest(PuzzleInput(fromString: "1,2,3"), result: 261214),
				PuzzleTest(PuzzleInput(fromString: "2,3,1"), result: 6895259),
				PuzzleTest(PuzzleInput(fromString: "3,2,1"), result: 18),
				PuzzleTest(PuzzleInput(fromString: "3,1,2"), result: 362),
			]
		),
	]

	required init() {}
}

