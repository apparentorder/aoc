class Day17: PuzzleClass {
	typealias Coordinates4D = (barf: Int, layer: Int, row: Int, column: Int)

	var dimension = [[[[Character]]]]()
	var nextDimension = [[[[Character]]]]()
	var maxBarf = 0
	var maxLayer = 0
	var maxRow = 0
	var maxColumn = 0
	let offset = 20

	func parse(_ input: PuzzleInput) {
		nextDimension = Array(
			repeating: Array(
				repeating: Array(
					repeating: Array(
						repeating: ".",
						count: offset*2
					),
					count: offset*2
				),
				count: offset*2
			),
			count: offset*2
		)

		for (rowIndex, row) in input.lines.enumerated() {
			for (colIndex, char) in row.enumerated() {
				writeNext(char, to: (0, 0, rowIndex, colIndex))
			}
		}

		dimension = nextDimension
	}

	func writeNext(_ c: Character, to loc: Coordinates4D) {
		nextDimension[loc.barf + offset][loc.layer + offset][loc.row + offset][loc.column + offset] = c
		maxBarf = max(maxBarf, abs(loc.barf))
		maxLayer = max(maxLayer, abs(loc.layer))
		maxRow = max(maxRow, abs(loc.row))
		maxColumn = max(maxColumn, abs(loc.column))
	}

	func read(from loc: Coordinates4D) -> Character {
		return dimension[loc.barf + offset][loc.layer + offset][loc.row + offset][loc.column + offset]
	}

	func countActiveNeighbors(_ loc: Coordinates4D) -> Int {
		var r = 0

		for moveBarf in [-1, 0, +1] {
			for moveLayer in [-1, 0, +1] {
				for moveRow in [-1, 0, +1] {
					for moveColumn in [-1, 0, +1] {
						guard moveBarf != 0 || moveLayer != 0 || moveRow != 0 || moveColumn != 0 else { continue }
						if read(from: (loc.barf + moveBarf, loc.layer + moveLayer, loc.row + moveRow, loc.column + moveColumn)) == "#" {
							r += 1
						}
					}
				}
			}
		}

		return r
	}

	func cubes(cycles: Int) -> Int {
		debug("Before any cycles:")
		debugDimension()

		for cycle in 1...cycles {
			for barf in -maxBarf-1...maxBarf+1 {
				for layer in -maxLayer-1...maxLayer+1 {
					for row in -maxRow-1...maxRow+1 {
						for column in -maxColumn-1...maxColumn+1 {
							let c = read(from: (barf, layer, row, column))

							let neigh = countActiveNeighbors((barf, layer, row, column))

							// if a cube is active
							if c == "#" {
								// and exactly 2 or 3 of its neighbors are also active
								if (neigh == 2 || neigh == 3) {
									// cube remains active
								} else {
									// cube becomes inactive
									writeNext(".", to: (barf, layer, row, column))
								}
							} else { // if a cube is inactive
								// but exactly 3 of its neighbors are active
								if neigh == 3 {
									// cube becomes active
									writeNext("#", to: (barf, layer, row, column))
								} else {
									// Otherwise, the cube remains inactive
								}
							}
						}
					}
				}
			}

			dimension = nextDimension
			debug("After cycle: \(cycle):")
			debugDimension()
		}

		return dimension
			.flatMap { $0 }
			.flatMap { $0 }
			.flatMap { $0 }
			.filter { $0 == "#" }
			.count
	}

	func debugDimension() {
		for barf in -maxBarf...maxBarf+1 {
			for layer in -maxLayer...maxLayer+1 {
				debug("z=\(layer), w=\(barf)")
				for row in -maxRow...maxRow+1 {
					var s = ""
					for column in -maxColumn...maxColumn+1 {
						s += String(read(from: (barf, layer, row, column)))
					}
					debug(s)
				}
				debug("")
			}
		}
		debug("------------------------------------------------------------------------")
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		parse(input)
		return cubes(cycles: 6)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return -2
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "17-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "17-input-test"), result: 848),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "17-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "17-input-test"), result: 868),
			]
		),
	]

	required init() {}
}

