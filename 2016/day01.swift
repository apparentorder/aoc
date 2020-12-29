class Day01: PuzzleClass {
	func getPos(_ path: [String], stopAtSecondVisit: Bool = false) -> Coordinates {
		var heading = Heading.north
		var pos = Coordinates(0, 0)
		var visitedPlaces = Set<Coordinates>()

		for var step in path {
			if step.hasSuffix(",") {
				step.removeLast()
			}

			let turn = step.removeFirst()
			let blocks = Int(step)!

			switch turn {
				case "R": heading.rotateRight()
				case "L": heading.rotateRight(3)
				default: err("bad turn in \(step)")
			}

			for _ in 0..<blocks {
				pos.x += heading.rawValue.x
				pos.y += heading.rawValue.y

				if stopAtSecondVisit && visitedPlaces.contains(pos) {
					return pos
				}

				visitedPlaces.insert(pos)
			}
		}

		return pos
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let pos = getPos(input.tokens)
		return abs(pos.x) + abs(pos.y)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let pos = getPos(input.tokens, stopAtSecondVisit: true)
		return abs(pos.x) + abs(pos.y)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "01-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "R2, L3"), result: 5),
				PuzzleTest(PuzzleInput(fromString: "R2, R2, R2"), result: 2),
				PuzzleTest(PuzzleInput(fromString: "R5, L5, R5, R3"), result: 12),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "01-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "R8, R4, R4, R8"), result: 4),
			]
		),
	]

	required init() {}

}

