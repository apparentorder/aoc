#!/usr/bin/env swift -g

import Foundation

infix operator **
// exponentiation, modulo m
func **(lhs: Int, rhs: Int) -> Int {
        var x = lhs
        var n = rhs
        var y = 1

        if n == 0 { return 1 }

        while n > 1 {
                if n.isMultiple(of: 2) {
                        x *= x
                        n /= 2
                } else {
                        y *= x
                        x *= x
                        n = (n - 1) / 2
                }
        }

        return x * y
}

struct Game: CustomStringConvertible {
	enum TileState {
		case Empty
		case Infested
	}

	public let height: Int
	public let width: Int
	public var map: [[TileState]]
	public var previousMaps = [[[TileState]]]()

	init(fromFileName fileName: String) {
		let contents = try! String(contentsOfFile: fileName, encoding: .utf8)
		let inputLines = contents.split(separator: "\n")
		height = inputLines.count
		width = inputLines[0].count

		map = Array(repeating: Array(repeating: .Empty, count: width), count: height)

		for (y, line) in inputLines.enumerated() {
			for (x, c) in line.enumerated() {
				switch(c) {
				case ".": map[x][y] = .Empty
				case "#": map[x][y] = .Infested
				default: fatalError("invalid input char \(c)")
				}
			}
		}
	}

	private func bugsNearby(_ x: Int, _ y: Int) -> Int {
		var ret = 0

		for checkx in [x - 1, x + 1] {
			//print("for (\(x),\(y)) checking (\(checkx),\(y))")
			guard checkx >= 0                else {continue}
			guard checkx <  self.width       else {continue}

			if self.map[checkx][y] == .Infested {
				ret += 1
			}
		}

		for checky in [y - 1, y + 1] {
			//print("for (\(x),\(y)) checking (\(x),\(checky))")
			guard checky >= 0                else {continue}
			guard checky < self.height       else {continue}

			if self.map[x][checky] == .Infested {
				ret += 1
			}
		}

		//print("(\(x),\(y)) => \(ret) nearby")
		return ret
	}

	public mutating func mutate() {
		var newMap = map

		self.previousMaps += [map]

		for y in 0 ..< self.height {
			for x in 0 ..< self.width {
				let b = bugsNearby(x, y)

				if map[x][y] == .Infested {
					if b != 1 {
						newMap[x][y] = .Empty
					}
				}

				if map[x][y] == .Empty {
					if 1 ... 2 ~= b {
						newMap[x][y] = .Infested
					}
				}
			}
		}

		map = newMap
	}

	public func mapString(map thisMap: [[TileState]]) -> String {
		var ret = ""

		for y in 0 ..< self.height {
			for x in 0 ..< self.width {
				switch thisMap[x][y] {
				case .Infested: ret += "#"
				case .Empty: ret += "."
				}
			}
			ret += "\n"
		}

		return ret
	}

	public var description: String {
		return mapString(map:self.map)
	}

	public var biodiversity: Int {
		var ret = 0
		for y in 0 ..< self.height {
			for x in 0 ..< self.width {
				if self.map[x][y] == .Infested {
					ret += 2 ** (y * self.width + x)
				}
			}
		}

		return ret
	}
}

func test1() {
	var game = Game(fromFileName: "example1")
	outer: while true {
		game.mutate()

		for m in game.previousMaps {
			if m == game.map {
				let bd = game.biodiversity
				precondition(bd == 2129920, "example1 failed, " +
					"returned \(bd) instead of 2129920")
				break outer
			}
		}
	}
}

test1()

// now for real
var game = Game(fromFileName: "input")
print(game)

var i = 0
outer: while true {
	i += 1
	game.mutate()
	print("After \(i)")
	print(game)

	for m in game.previousMaps {
		if m == game.map {
			print("done, biodiversity is \(game.biodiversity)")
			break outer
		}
	}
}

