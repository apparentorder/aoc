class Day08: PuzzleClass {
	var grid = [[Character]]()

	func makeGrid(_ instructions: [String]) {
		if instructions[0] == "TEST" {
			// hack: no other way of knowing if this is a test run or the 'real' puzzle input
			// TEST is a 7x3 pixel grid
			grid = Array(repeating: Array(repeating: Character("."), count: 7), count: 3)
		} else {
			// actual puzzle is a 50x6 grid
			grid = Array(repeating: Array(repeating: Character("."), count: 50), count: 6)
		}
	}

	func parse(_ instructions: [String]) -> PuzzleResult {
		for i in instructions {
			let parts = i.components(separatedBy: " " )

			if parts[0] == "TEST" {
				// NOP

			} else if parts[0] == "rect" {
				let AxB = parts[1].components(separatedBy: "x")
				let a = Int(AxB[0])!
				let b = Int(AxB[1])!

				for x in 0..<a {
					for y in 0..<b {
						grid[y][x] = "#"
					}
				}

			} else if parts[0] == "rotate" {
				let which = Int(parts[2].dropFirst(2))! // drop "x=" or "y="
				let by = Int(parts[4])!

				let oldGrid = grid
				if parts[1] == "row" {
					let len = grid[0].count
					for column in 0..<len {
						grid[which][(column + by) % len] = oldGrid[which][column]
					}
				} else if parts[1] == "column" {
					let len = grid.count
					for row in 0..<len {
						grid[(row + by) % len][which] = oldGrid[row][which]
					}
				} else {
					err("invalid rotate instruction: \(i)")
				}
			} else {
				err("invalid instruction: \(i)")
			}

			debug("After instruction: \(i)")
			grid.forEach {
				debug(String($0))
			}
			debug("")
		}

		return grid.flatMap {$0}.filter { $0 == "#" }.count
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		makeGrid(input.lines)
		return parse(input.lines)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return "AFBUPZBJPS"
		// solved by hand: read letters from part 1 grid output
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "08-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "08-input-test"), result: 6),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "08-input"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "08-test1"), result: 241861950),
			]
		),
	]

	required init() {}

}

