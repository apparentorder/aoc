class Day25: PuzzleClass {
	func transform(subjectNumber: Int, loopSize: Int) -> Int {
		var value = 1

		for _ in 0..<loopSize {
			value *= subjectNumber
			value %= 2020_12_27
		}

		return value
	}

	func loopSize(forPublicKey key: Int) -> Int {
		let subjectNumber = 7
		var value = 1
		var loops = 0

		while true {
			guard value != key else { return loops }

			value *= subjectNumber
			value %= 2020_12_27
			loops += 1
		}
	}

	
	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let pubKeyCard = input.intArray[0]
		let pubKeyDoor = input.intArray[1]

		let lsCard = loopSize(forPublicKey: pubKeyCard)
		let lsDoor = loopSize(forPublicKey: pubKeyDoor)

		debug("loop size: card: \(lsCard), door: \(lsDoor)")

		let privKey1 = transform(subjectNumber: pubKeyDoor, loopSize: lsCard)
		let privKey2 = transform(subjectNumber: pubKeyCard, loopSize: lsDoor)

		debug("private keys: \(privKey1), \(privKey2)")

		return privKey1
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return -2
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromString: "17607508 15065270"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "5764801 17807724"), result: 14897079),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromString: "17607508 15065270"),
			tests: [
				//PuzzleTest(PuzzleInput(fromString: "5764801 17807724"), result: 14897079),
			]
		),
	]

	required init() {}
}

