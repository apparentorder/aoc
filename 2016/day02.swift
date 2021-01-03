class Day02: PuzzleClass {
	func code(_ lines: [String], buttons: Dictionary<Coordinates, String>) -> String {
		var pos = buttons.first(where: { $0.value == "5" })!.key
		var r = ""

		for instruction in lines {
			for movement in instruction {
				var tryPos = pos
				switch movement {
					case "U": tryPos.y -= 1
					case "D": tryPos.y += 1
					case "L": tryPos.x -= 1
					case "R": tryPos.x += 1
					default: err("bad input: \(instruction)")
				}

				guard buttons.keys.contains(tryPos) else {
					// illegal moves are to be ignored
					continue
				}

				pos = tryPos
			}

			r += buttons[pos]!
		}

		return r
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let buttons = [
			Coordinates(0, 0): "1",
			Coordinates(1, 0): "2",
			Coordinates(2, 0): "3",

			Coordinates(0, 1): "4",
			Coordinates(1, 1): "5",
			Coordinates(2, 1): "6",

			Coordinates(0, 2): "7",
			Coordinates(1, 2): "8",
			Coordinates(2, 2): "9",
		]

		return code(input.lines, buttons: buttons)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let buttons = [
			//Coordinates(0, 0): nil,
			//Coordinates(1, 0): nil,
			Coordinates(2, 0): "1",
			//Coordinates(3, 0): nil,
			//Coordinates(4, 0): nil,

			//Coordinates(0, 1): nil,
			Coordinates(1, 1): "2",
			Coordinates(2, 1): "3",
			Coordinates(3, 1): "4",
			//Coordinates(4, 1): nil,

			Coordinates(0, 2): "5",
			Coordinates(1, 2): "6",
			Coordinates(2, 2): "7",
			Coordinates(3, 2): "8",
			Coordinates(4, 2): "9",

			//Coordinates(0, 3): nil,
			Coordinates(1, 3): "A",
			Coordinates(2, 3): "B",
			Coordinates(3, 3): "C",
			//Coordinates(4, 3): nil,

			//Coordinates(0, 4): nil,
			//Coordinates(1, 4): nil,
			Coordinates(2, 4): "D",
			//Coordinates(3, 4): nil,
			//Coordinates(4, 4): nil,
		]

		return code(input.lines, buttons: buttons)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "02-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "02-input-test"), result: 1985),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "02-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "02-input-test"), result: "5DB3")
			]
		),
	]

	required init() {}
}

