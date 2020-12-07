class Day03: PuzzleClass {
	func treesInMatrix(_ matrix: Matrix, xIncrement: Int, yIncrement: Int) -> PuzzleResult {
		var x = xIncrement
		var y = yIncrement
		var treeCount = 0

		while y < matrix.rows {
			if matrix.getChar(atCoordinates: x, y) == "#" {
				debug("tree at \(x),\(y)")
				treeCount += 1
			} else {
				debug("NO tree at \(x),\(y)")
			}

			x = (x + xIncrement) % matrix.columns
			y += yIncrement
		}

		debug("Count for increments \(xIncrement),\(yIncrement) = \(treeCount)")
		return treeCount
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return treesInMatrix(input.matrix, xIncrement: 3, yIncrement: 1)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		var totalTreeCount = 1
		totalTreeCount *= treesInMatrix(input.matrix, xIncrement: 1, yIncrement: 1)
		totalTreeCount *= treesInMatrix(input.matrix, xIncrement: 3, yIncrement: 1)
		totalTreeCount *= treesInMatrix(input.matrix, xIncrement: 5, yIncrement: 1)
		totalTreeCount *= treesInMatrix(input.matrix, xIncrement: 7, yIncrement: 1)
		totalTreeCount *= treesInMatrix(input.matrix, xIncrement: 1, yIncrement: 2)
		return totalTreeCount
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "03-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "03-input-test1"), result: 7),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "03-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "03-input-test1"), result: 336),
			]
		),
	]

	required init() {}
}

