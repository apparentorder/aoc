class Day13: PuzzleClass {
	var favoriteNumber: Int = -1

	func findPaths(
		from start: Coordinates, 
		to target: Coordinates, 
		maxSteps: Int? = nil,
		keepInvalidPaths: Bool = false
	) -> [[Coordinates]] {
		// bfs path find w/o any optimizations.
		// will return either
		// - all valid paths that use the minimum steps count, or
		// - all attempted paths with maxSteps (or, if keepInvalidPaths: all attempted paths including
		//   those with less than maxSteps, i.e. known dead ends)
		// n.b.: returned path will include the starting position! i.e. path.count <= (maxSteps + 1)

		var paths = [[start]]
		var nextPaths = [[Coordinates]]()
		var deadPaths = [[Coordinates]]()
		var targetFound = false

		while true {
			let steps = paths.first!.count
			//debug("steps: \(steps)")
			//debug("\(paths)")
			//debug("")

			nextPaths.removeAll(keepingCapacity: true)

			for path in paths {
				let pos = path.last!

				let candidates = [
					Coordinates(pos.x + 1, pos.y    ),
					Coordinates(pos.x    , pos.y + 1),
					Coordinates(pos.x - 1, pos.y    ),
					Coordinates(pos.x    , pos.y - 1),
				]

				var isValidPath = false
				for nextCoord in candidates {
					guard nextCoord.x >= 0 && nextCoord.y >= 0 else { continue }
					guard !isWall(nextCoord) else { continue }
					guard !path.contains(nextCoord) else { continue }

					isValidPath = true
					nextPaths += [path + [nextCoord]]

					if nextCoord == target {
						targetFound = true
					}
				}

				if !isValidPath && keepInvalidPaths {
					deadPaths += [path]
				}
			}

			paths = nextPaths

			guard maxSteps == nil || steps < maxSteps! else {
				return paths + deadPaths
			}

			guard !targetFound else {
				return paths.filter { $0.last! == target }
			}
		}
	}

	func isWall(_ c: Coordinates) -> Bool {
		let n = 
			c.x*c.x
			+ 3*c.x
			+ 2*c.x*c.y
			+ c.y
			+ c.y * c.y
			+ favoriteNumber

		let binary = String(n, radix: 2)
		let oneCount = binary.filter { $0 == "1" }.count

		// odd number: it's a wall
		return (oneCount % 2 == 1)
	}

	func mapSpace(size: Int, path: [Coordinates]? = nil) -> String {
		var s = ""

		for row in 0..<size {
			for col in 0..<size {
				let c = Coordinates(col, row)
				if let p = path, p.contains(c) {
					s += "O"
				} else {
					s += isWall(c) ? "#" : "."
				}
			}

			s += "\n"
		}

		return s
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		favoriteNumber = Int(input.raw)!
		let destination = (favoriteNumber == 10) ? Coordinates(7,4) : Coordinates(31,39)
		let mapSize = max(destination.x, destination.y) + 3

		debug(mapSpace(size: mapSize))

		let paths = findPaths(from: Coordinates(1,1), to: destination)
		debug("found \(paths.count) paths")

		for path in paths {
			debug("found path: \(path) -->")
			debug(mapSpace(size: mapSize, path: path))
		}

		guard let path = paths.first else {
			err("no paths found?!")
		}

		return path.count - 1 // not counting the starting position
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		favoriteNumber = Int(input.raw)!
		let destination = (favoriteNumber == 10) ? Coordinates(7,4) : Coordinates(31,39)
		let mapSize = max(destination.x, destination.y) + 3

		let paths = findPaths(from: Coordinates(1,1), to: destination, maxSteps: 50, keepInvalidPaths: true)
		let distinctCoordinates = Set(paths.flatMap { $0 })

		debug(mapSpace(size: mapSize, path: Array(distinctCoordinates)))
		debug("pathlen: \(paths.map { $0.count }.max()!)")
		return distinctCoordinates.count
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromString: "1352"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "10"), result: 11),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromString: "1352"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "13-test1"), result: 241861950),
			]
		),
	]

	required init() {}

}

