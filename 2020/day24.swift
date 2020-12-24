class Day24: PuzzleClass {
	struct HexCoordinate: Hashable, CustomStringConvertible {
		let x: Int
		let y: Int

		var isOffsetRight: Bool { abs(y) % 2 == 1 }
		var description: String { "(\(x),\(y)\(isOffsetRight ? "R" : ""))" }
		var neighbors: [String:HexCoordinate] {
			//
			// we treat the floor as a simple x-by-y grid, 
			// with tiles in uneven rows offset to the right:
			//
			// (0,0) (1,0)
			//    (0,1) (1,1) <-- offset to right
			// (0,2) (1,2)
			//    (0,3) (1,3) <-- offset to right
			//
			isOffsetRight ?
				[
					"e":  HexCoordinate(x + 1, y    ),
					"w":  HexCoordinate(x - 1, y    ),
					"nw": HexCoordinate(x    , y - 1),
					"ne": HexCoordinate(x + 1, y - 1),
					"sw": HexCoordinate(x    , y + 1),
					"se": HexCoordinate(x + 1, y + 1),
				]
			:
				[
					"e":  HexCoordinate(x + 1, y    ),
					"w":  HexCoordinate(x - 1, y    ),
					"nw": HexCoordinate(x - 1, y - 1),
					"ne": HexCoordinate(x    , y - 1),
					"sw": HexCoordinate(x - 1, y + 1),
					"se": HexCoordinate(x    , y + 1),
				]
		}

		init(_ x: Int, _ y: Int) {
			self.x = x
			self.y = y
		}
	}

	struct blackTileMap: CustomStringConvertible {
		var blackTiles = Set<HexCoordinate>()
		var countBlack: Int { blackTiles.count }

		func isBlack(_ c: HexCoordinate) -> Bool {
			blackTiles.contains(c)
		}

		mutating func flip(_ c: HexCoordinate) {
			if blackTiles.contains(c) {
				blackTiles.remove(c)
			} else {
				blackTiles.insert(c)
			}
		}

		mutating func flip(usingTileList tileList: [String]) {
			for var line in tileList {
				var currentTile = HexCoordinate(0, 0)
				var path = ""

				while !line.isEmpty {
					var direction = String(line.removeFirst())
					if direction == "n" || direction == "s" {
						direction += String(line.removeFirst())
					}

					currentTile = currentTile.neighbors[direction]!
					path += "\(direction)=\(currentTile) "
				}

				flip(currentTile)
				debug("path: \(path)")
				debug("tile \(currentTile) is now \(isBlack(currentTile) ? "black" : "white")")
				debug("")
			}
		}

		mutating func conway() {
			var nextMap = self

			// we have no inventory of white tiles, so we
			// just check all black tiles and their neighbors
			let coordsToCheck = blackTiles.union(blackTiles.flatMap { $0.neighbors.values })

			for tileCoord in coordsToCheck {
				let blackTileCount = tileCoord.neighbors.values
					.filter { isBlack($0) }
					.count

				if isBlack(tileCoord) && (blackTileCount == 0 || blackTileCount > 2) {
					// Any black tile with zero or more than 2 black tiles
					// immediately adjacent to it is flipped to white.
					nextMap.flip(tileCoord)
				} else if !isBlack(tileCoord) && (blackTileCount == 2) {
					// Any white tile with exactly 2 black tiles immediately
					// adjacent to it is flipped to black.
					nextMap.flip(tileCoord)
				}
			}

			self = nextMap
		}

		var description: String {
			let xMin = blackTiles.map { $0.x }.min()!
			let xMax = blackTiles.map { $0.x }.max()!
			let yMin = blackTiles.map { $0.y }.min()!
			let yMax = blackTiles.map { $0.y }.max()!

			var s = ""
			for y in yMin...yMax {
				if HexCoordinate(0, y).isOffsetRight {
					s += " "
				}
				for x in xMin...xMax {
					s += isBlack(HexCoordinate(x, y)) ? "# " : ". "
				}
				s += "\n"
			}

			return s
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		var floor = blackTileMap()
		floor.flip(usingTileList: input.lines)
		return floor.countBlack
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		var floor = blackTileMap()
		floor.flip(usingTileList: input.lines)

		debug("Day 0: \(floor.countBlack) -->")
		debug(floor)

		for day in 1...100 {
			floor.conway()
			debug("Day \(day): \(floor.countBlack) -->")
			debug(floor)
		}

		return floor.countBlack
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "24-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "esew"), result: 1),
				PuzzleTest(PuzzleInput(fromString: "nwwswee"), result: 1),
				PuzzleTest(PuzzleInput(fromFile: "24-input-test"), result: 10),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "24-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "24-input-test"), result: 2208),
			]
		),
	]

	required init() {}
}

