class Day11: PuzzleClass {
	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return foo(input, isPart2: false)
	}

	func checkDirection(map: Matrix, fromX: Int, fromY: Int, xIncrement: Int, yIncrement: Int, maxIncrement: Int? = nil) -> Character? {
		var currentX = fromX
		var currentY = fromY

		debug("checkDirection from \(fromX),\(fromY) moving \(xIncrement),\(yIncrement)")

		while true {
			currentX += xIncrement
			currentY += yIncrement

			guard currentX >= 0 && currentX < map.columns else { return nil }
			guard currentY >= 0 && currentY < map.rows else { return nil }

			let c = map.getChar(atCoordinates: currentX, currentY)

			if c != "." {
				debug("checkDirection match: \(c) at \(currentX),\(currentY)")
				return c
			}
		}
	}

	func foo(_ input: PuzzleInput, isPart2: Bool) -> PuzzleResult {
		var changes = 0
		var mapPrev = input.matrix
		let maxPeople = isPart2 ? 5 : 4

		debug("map rows=\(mapPrev.rows) cols=\(mapPrev.columns)")
		repeat {
			var map = mapPrev
			changes = 0
			for x in 0..<map.columns {
				for y in 0..<map.rows {
					debug("AT \(x),\(y)")

					var surroundings = [Character]()
					if !isPart2 {
						debug("check \(x-1),\(y-1)")
						surroundings += (x > 0 && y > 0) ? [mapPrev.getChar(atCoordinates: x - 1, y - 1)] : []
						debug("check \(x-1),\(y)")
						surroundings += (x > 0) ? [mapPrev.getChar(atCoordinates: x - 1, y)] : []
						debug("check \(x-1),\(y+1)")
						surroundings += (x > 0 && y+1 < map.rows) ? [mapPrev.getChar(atCoordinates: x - 1, y + 1)] : []
						debug("check \(x),\(y-1)")
						surroundings += (y > 0) ? [mapPrev.getChar(atCoordinates: x, y - 1)] : []
						//debug("check \(x),\(y)")
						//surroundings += [mapPrev.getChar(atCoordinates: x, y)]
						debug("check \(x),\(y+1)")
						surroundings += (y+1 < map.rows) ? [mapPrev.getChar(atCoordinates: x, y + 1)] : []
						debug("check \(x+1),\(y-1)")
						surroundings += (x+1 < map.columns && y > 0) ? [mapPrev.getChar(atCoordinates: x + 1, y - 1)] : []
						debug("check \(x+1),\(y)")
						surroundings += (x+1 < map.columns) ? [mapPrev.getChar(atCoordinates: x + 1, y)] : []
						debug("check \(x+1),\(y+1)")
						surroundings += (x+1 < map.columns && y+1 < map.rows) ? [mapPrev.getChar(atCoordinates: x + 1, y + 1)] : []
					}

					if isPart2 {
						var c: Character?

						c = checkDirection(map: mapPrev, fromX: x, fromY: y, xIncrement: -1, yIncrement: -1)
						surroundings += (c == nil) ? [] : [c!]

						c = checkDirection(map: mapPrev, fromX: x, fromY: y, xIncrement: 0, yIncrement: -1)
						surroundings += (c == nil) ? [] : [c!]

						c = checkDirection(map: mapPrev, fromX: x, fromY: y, xIncrement: +1, yIncrement: -1)
						surroundings += (c == nil) ? [] : [c!]

						c = checkDirection(map: mapPrev, fromX: x, fromY: y, xIncrement: -1, yIncrement: 0)
						surroundings += (c == nil) ? [] : [c!]

						c = checkDirection(map: mapPrev, fromX: x, fromY: y, xIncrement: +1, yIncrement: 0)
						surroundings += (c == nil) ? [] : [c!]

						c = checkDirection(map: mapPrev, fromX: x, fromY: y, xIncrement: -1, yIncrement: +1)
						surroundings += (c == nil) ? [] : [c!]

						c = checkDirection(map: mapPrev, fromX: x, fromY: y, xIncrement: 0, yIncrement: +1)
						surroundings += (c == nil) ? [] : [c!]

						c = checkDirection(map: mapPrev, fromX: x, fromY: y, xIncrement: +1, yIncrement: +1)
						surroundings += (c == nil) ? [] : [c!]

					}

					debug(surroundings)

					switch mapPrev.getChar(atCoordinates: x, y) {
					case ".": break
					case "#":
						if surroundings.filter({ $0 == "#" }).count >= maxPeople {
							map.data[y][x] = "L"
							changes += 1
						}
					case "L":
						if surroundings.filter({ $0 == "#" }).count == 0 {
							map.data[y][x] = "#"
							changes += 1
						}

					default: err("seat?")
					}
				}
			}

			debug("------------------------------------------------------------------------")
			map.data.forEach { debug(String($0)) }

			mapPrev = map
		} while changes > 0

		return mapPrev.data.reduce(0, { $0 + $1.filter({ $0 == "#" }).count })
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return foo(input, isPart2: true)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "11-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "11-input-test"), result: 37),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "11-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "11-input-test"), result: 26),
			]
		),
	]

	required init() {}
}

