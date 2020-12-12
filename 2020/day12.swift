class Day12: PuzzleClass {
	enum Degrees: Int {
		case north = 0
		case east = 90
		case south = 180
		case west = 270

		init(_ n: Int) {
			debug("deg from \(n)")
			if n >= 0 { self = Degrees(rawValue: n % 360)! }
			else { self = Degrees(rawValue: 360 + n)! }
		}
	}

	var ew = 0
	var ns = 0
	var deg = Degrees.east

	var wp_ew = 0
	var wp_ns = 0

	func part2(_ inputLines: [String]) -> Int {
		func rotateright(_ degin: Int) {
			var deg = degin
			if deg < 0 { deg += 360 }
			deg = deg % 360

			for _ in 1...Int(deg/90) {
				var x_ns = wp_ns
				var x_ew = wp_ew

				wp_ew = x_ns * -1
				wp_ns = x_ew
			}
		}

		wp_ew = 10
		wp_ns = -1

		for inputLine in inputLines {
			var line = inputLine
			let action = line.removeFirst()
			let value = Int(line)!

			debug(inputLine)

			switch action {
			case "N": wp_ns -= value
			case "S": wp_ns += value
			case "E": wp_ew += value
			case "W": wp_ew -= value
			case "L": rotateright(360 - value)
			case "R": rotateright(value)
			case "F":
				for _ in 0..<value {
					ew += wp_ew
					ns += wp_ns
				}
			default: err("\(inputLine)")
			}

			debug("ship: ns \(ns) ew \(ew), waypoint: ns \(wp_ns) ew \(wp_ew)")
		}

		return abs(ns) + abs(ew)
	}

	func part1(_ inputLines: [String]) -> Int {
		for inputLine in inputLines {
			var line = inputLine
			let action = line.removeFirst()
			let value = Int(line)!

			debug(inputLine)

			switch action {
			case "N": ns -= value
			case "S": ns += value
			case "E": ew += value
			case "W": ew -= value
			case "L": deg = Degrees(deg.rawValue - value)
			case "R": deg = Degrees(deg.rawValue + value)
			case "F":
				switch deg {
				case .north: ns -= value
				case .south: ns += value
				case .east: ew += value
				case .west: ew -= value
				}
			default: err("\(inputLine)")
			}

			debug("now at ns \(ns) ew \(ew) facing \(deg)")
		}

		return abs(ns) + abs(ew)
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return part1(input.lines)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return part2(input.lines)
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

