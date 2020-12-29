enum Heading: Coordinates {
	case north = "(0,-1)"
	case south = "(0,1)"
	case east = "(1,0)"
	case west = "(-1,0)"

	mutating func rotateRight(_ times: Int = 1) {
		for _ in 0..<times {
			switch self {
				case .north: self = .east
				case .east: self = .south
				case .south: self = .west
				case .west: self = .north
			}
		}
	}
}

struct Coordinates: ExpressibleByStringLiteral, Equatable, CustomStringConvertible, Hashable {
	var x: Int
	var y: Int

	var description: String { "(\(x),\(y))" }

	init(stringLiteral value: String) {
		let xy = value
			.dropFirst()
			.dropLast()
			.components(separatedBy: ",")
			.map { Int($0)! }

		self.x = xy[0]
		self.y = xy[1]
	}

	init(_ x: Int, _ y: Int) {
		self.x = x
		self.y = y
	}

	static func == (lhs: Coordinates, rhs: Coordinates) -> Bool {
		return lhs.x == rhs.x && lhs.y == rhs.y
	}
}

