class Day18: PuzzleClass {
	enum Tile: Character {
		case safe = "."
		case trap = "^"
	}

	struct TileRow: CustomStringConvertible {
		var tiles: [Tile]
		var safeCount: Int

		var description: String { tiles.reduce(into: "") { $0 += [$1.rawValue] } }

		var nextRow: TileRow {
			var r = self
			r.safeCount = 0

			for i in 0..<tiles.count {
				let leftTile: Tile = (i == 0) ? .safe : tiles[i - 1]
				let centerTile = tiles[i]
				let rightTile: Tile = (i == tiles.count - 1) ? .safe : tiles[i + 1]

				let newTile: Tile

				if leftTile == .trap && centerTile == .trap && rightTile == .safe {
					// Its left and center tiles are traps, but its right tile is not.
					newTile = .trap
				} else if leftTile == .safe && centerTile == .trap && rightTile == .trap {
					// Its center and right tiles are traps, but its left tile is not.
					newTile = .trap
				} else if leftTile == .trap && centerTile == .safe && rightTile == .safe {
					// Only its left tile is a trap.
					newTile = .trap
				} else if leftTile == .safe && centerTile == .safe && rightTile == .trap {
					// Only its right tile is a trap.
					newTile = .trap
				} else {
					newTile = .safe
					r.safeCount += 1
				}

				r.tiles[i] = newTile

				//debug("new tile \(i) = \(newTile) (left \(leftTile) center \(centerTile) right \(rightTile)")
			}

			return r
		}

		init(_ s: String) {
			self.tiles = Array(s).map { Tile(rawValue: $0)! }
			self.safeCount = tiles.filter { $0 == .safe }.count
		}
	}

	func makeFloor(firstRow firstRowString: String, count rowCount: Int, countOnly: Bool) -> ([TileRow], Int) {
		let firstRow = TileRow(firstRowString)

		var r = countOnly ? [TileRow]() : [firstRow]

		var prevRow = firstRow
		var safeCount = firstRow.safeCount

		for _ in 0..<(rowCount - 1) {
			let nextRow = prevRow.nextRow

			safeCount += nextRow.safeCount
			if !countOnly {
				r += [r.last!.nextRow]
			}

			prevRow = nextRow
		}

		return (r, safeCount)
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		// N.B.: Input amended to include expected row count
		let c = input.raw.components(separatedBy: " ")
		let rowCount = Int(c[0])!
		let firstRow = c[1]

		let (floor, safeCount) = makeFloor(
			firstRow: firstRow,
			count: rowCount,
			countOnly: rowCount >= 100
		)

		floor.forEach { debug($0) }

		return safeCount
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return part1(input)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromString: "40 ^.^^^..^^...^.^..^^^^^.....^...^^^..^^^^.^^.^^^^^^^^.^^.^^^^...^^...^^^^.^.^..^^..^..^.^^.^.^......."),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "3 ..^^."), result: 6),
				PuzzleTest(PuzzleInput(fromString: "10 .^^.^.^^^^"), result: 38),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromString: "400000 ^.^^^..^^...^.^..^^^^^.....^...^^^..^^^^.^^.^^^^^^^^.^^.^^^^...^^...^^^^.^.^..^^..^..^.^^.^.^......."),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "18-test1"), result: 241861950),
			]
		),
	]

	required init() {}

}

