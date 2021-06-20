class Day24: PuzzleClass {
	typealias RouteId = Set<Int>
	var mazeWalls = [Coordinates:Bool]() // Coordinates is wall?
	var wires = [Int:Coordinates]() // wire-id to Coordinates
	var routes = [RouteId:Int]() // all possible "wire-id to wire-id" shortest path lengths

	func shortestWireRoute(returningHome: Bool) -> Int {
		var possiblePaths = [[Int]]()
		var nextPossiblePaths = [[0]] // the little robot starts at wire-id 0

		while !nextPossiblePaths.isEmpty {
			possiblePaths = nextPossiblePaths
			nextPossiblePaths.removeAll(keepingCapacity: true)

			for path in possiblePaths {
				for nextWire in wires.keys where !path.contains(nextWire) {
					nextPossiblePaths += [path + [nextWire]]
				}
			}
		}

		var shortestRoute = Int.max
		for path in possiblePaths {
			var steps = 0
			for i in 1..<path.count {
				let routeId = Set([path[i], path[i-1]])
				steps += routes[routeId]!
			}

			if returningHome {
				// add steps for returning from the last position to '0'
				let routeId = Set([path.last!, 0])
				steps += routes[routeId]!
			}

			if steps < shortestRoute {
				shortestRoute = steps
				debug("new shortest route (\(steps)): \(path)")
			}
		}

		return shortestRoute
	}

	func calcWireRoutes() {
		for wireA in wires.keys {
			for wireB in wires.keys where wireB != wireA {
				debug("pathing from wire \(wireA) to wire \(wireB)")

				let routeId = Set([wireA, wireB])
				let routeLength = shortestPathLength(from: wires[wireA]!, to: wires[wireB]!)

				routes[routeId] = routeLength
			}
		}
	}

	func shortestPathLength(from start: Coordinates, to destination: Coordinates) -> Int {
		//debug("pathing from \(start) to \(destination)")

		var possiblePaths = [[Coordinates]]()
		var nextPossiblePaths = [[start]]
		var positionsSeen = Set<Coordinates>()

		while !nextPossiblePaths.isEmpty {
			possiblePaths = nextPossiblePaths
			nextPossiblePaths.removeAll(keepingCapacity: true)
			//print("(pp now \(possiblePaths.count))")

			for path in possiblePaths {
				let position = path.last!

				guard position != destination else {
					// found it
					let steps = path.dropFirst() // drop starting position
					debug("found path \(steps) (\(steps.count)) out of \(possiblePaths.count) routes so far")
					return path.count - 1 // not counting starting position
				}

				let up    = Coordinates(position.x, position.y - 1)
				let down  = Coordinates(position.x, position.y + 1)
				let left  = Coordinates(position.x - 1, position.y)
				let right = Coordinates(position.x + 1, position.y)

				for nextPosition in [up, down, left, right] where !positionsSeen.contains(nextPosition) {
					guard let isWall = mazeWalls[nextPosition], !isWall else {
						continue
					}

					positionsSeen.insert(nextPosition)
					nextPossiblePaths += [path + [nextPosition]]
				}
			}
		}

		err("cannot find path from \(start) to \(destination)")
	}

	func parse(_ lines: [String]) {
		let rows = lines.count
		let columns = lines[0].count

		mazeWalls.reserveCapacity(rows * columns)

		for row in 0..<lines.count {
			for column in 0..<lines[row].count {
				// find and mark all walls
				let char = Array(lines[row])[column]

				mazeWalls[Coordinates(row, column)] = (char == "#")

				if char != "#", char != "." {
					// number field
					debug("found wire \(char) at \(Coordinates(row, column))")
					wires[Int(String(char))!] = Coordinates(row, column)
				}
			}
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		parse(input.lines)
		calcWireRoutes()
		return shortestWireRoute(returningHome: false)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		parse(input.lines)
		calcWireRoutes()
		return shortestWireRoute(returningHome: true)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "24-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "24-input-test"), result: 14),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "24-input"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "24-test1"), result: 241861950),
			]
		),
	]

	required init() {}

}

