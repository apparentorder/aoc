class Day12: PuzzleClass {
	//
	// north: y-axis < 0              ^ y>0
	// south: y-axis > 0              |
	//                       x<0  <---+--->  x>0
	// east:  x-axis > 0              |
	// west:  x-axis < 0              v y<0
	//
	// for part1, we use the waypoint coordinates as the current heading,
	// e.g. heading east is (x, y) = (1, 0)
	//

	var position = Coordinates(0, 0)
	var waypoint = Coordinates(0, 0) // or heading for part1

	func navigate(_ inputLines: [String], isPart2: Bool) -> Int {
		func move(by change: Coordinates, moveWaypoint: Bool = isPart2) {
			// by default, we moveWaypoint in part2,
			// but for the ship movement in part2, we explicitly want to
			// move the ship itself (!moveWaypoint)

			if moveWaypoint {
				waypoint.x += change.x
				waypoint.y += change.y
			} else {
				position.x += change.x
				position.y += change.y
			}
		}

		func rotateRight(by degrees: Int) {
			switch degrees {
			case 90:  waypoint = (x: waypoint.y * -1, y: waypoint.x)
			case 180: waypoint = (x: waypoint.x * -1, y: waypoint.y * -1)
			case 270: waypoint = (x: waypoint.y, y: waypoint.x * -1)
			default:
				err("rotateRight by \(degrees) degrees?!")
			}
		}

		for inputLine in inputLines {
			var line = inputLine
			let action = line.removeFirst()
			let value = Int(line)!

			debug(inputLine)

			switch action {
			case "N": move(by: (x: 0, y: value * -1))
			case "S": move(by: (x: 0, y: value * +1))
			case "E": move(by: (x: value * +1, y: 0))
			case "W": move(by: (x: value * -1, y: 0))
			case "L": rotateRight(by: 360 - value)
			case "R": rotateRight(by: value)
			case "F": move(by: (x: waypoint.x * value, y: waypoint.y * value), moveWaypoint: false)
			default: err("\(inputLine)")
			}

			debug("ship: \(position), waypoint: \(waypoint)")
		}

		return abs(position.x) + abs(position.y)
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		waypoint = (x: 1, y: 0) // start facing east
		return navigate(input.lines, isPart2: false)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		waypoint = (x: 10, y: -1) // waypoint starts 10 units east and 1 unit north
		return navigate(input.lines, isPart2: true)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "12-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "12-input-test"), result: 25),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "12-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "12-input-test"), result: 286),
			]
		),
	]

	required init() {}
}

