#!/usr/bin/env swift -g -O

import Foundation

struct Game: CustomStringConvertible {
	enum TileState {
		case Empty
		case Infested
		case RecursiveGrid
	}

	enum Side {
		case Top
		case Left
		case Right
		case Bottom
	}

	public let height: Int
	public let width: Int

	struct Map {
		public var tiles: [[TileState]]

		init(width: Int, height: Int) {
			tiles = Array(repeating: Array(repeating: .Empty, count: width), count: height)

			// overwrite middle position with '?'
			tiles[width/2][height/2] = .RecursiveGrid
		}

		public var bugCount: Int {
			return tiles.flatMap{$0}.filter{$0 == .Infested}.count
		}
	}

	public var recursiveMaps = Dictionary<Int, Map>()

	public var bugCount: Int {
		return self.recursiveMaps.keys.map { recursiveMaps[$0]!.bugCount }.reduce(0, + )
	}

	init(fromFileName fileName: String) {
		let contents = try! String(contentsOfFile: fileName, encoding: .utf8)
		let inputLines = contents.split(separator: "\n")

		self.height = inputLines.count
		self.width = inputLines[0].count

		var map = Map(width: self.width, height: self.height)

		for (y, line) in inputLines.enumerated() {
			for (x, c) in line.enumerated() {
				switch(c) {
				case ".": map.tiles[x][y] = .Empty
				case "#": map.tiles[x][y] = .Infested
				case "?": map.tiles[x][y] = .RecursiveGrid
				default: fatalError("invalid input char \(c)")
				}
			}
		}

		// overwrite middle position with '?' (again)
		map.tiles[self.width/2][self.height/2] = .RecursiveGrid

		self.recursiveMaps[0] = map
	}

	private func isBugTile(_ x: Int, _ y: Int, depth: Int) -> Bool {
		// check if that level even exists yet, otherwise it doesn't count as bugged
		guard let m = self.recursiveMaps[depth] else { return false }

		return m.tiles[x][y] == .Infested
	}

	private func bugsAtSide(depth: Int, side: Side) -> Int {
		// check if that level even exists yet, otherwise it doesn't count as bugged
		guard self.recursiveMaps[depth] != nil else { return 0 }

		var ret = 0

		switch side {
		case .Left:
			for y in 0 ..< self.height {
				ret += isBugTile(0, y, depth: depth) ? 1 : 0
			}
		case .Right:
			for y in 0 ..< self.height {
				ret += isBugTile(self.width - 1, y, depth: depth) ? 1 : 0
			}
		case .Top:
			for x in 0 ..< self.width {
				ret += isBugTile(x, 0, depth: depth) ? 1 : 0
			}
		case .Bottom:
			for x in 0 ..< self.width {
				ret += isBugTile(x, self.height - 1, depth: depth) ? 1 : 0
			}
		}

		return ret
	}

	private func bugsNearby(_ x: Int, _ y: Int, depth: Int) -> Int {
		precondition(x != self.width/2 || y != self.height/2,
			"bugsNearby() called for depth \(depth) middle position (\(x),\(y))?!")

		var ret = 0

		// check x values (left/right)
		for checkx in [x - 1, x + 1] {
			if checkx == self.width/2 && y == self.height/2 {
				// check side of inner map depth+1
				ret += bugsAtSide(depth: depth+1, side: (checkx > x) ? .Left : .Right)
				continue
			}

			switch checkx {
			case -1:
				// check the tile to our left on the outer map depth-1
				ret += isBugTile(self.width/2 - 1, self.height/2, depth: depth-1) ? 1 : 0
			case self.width:
				// check the tile to our right on the outer map depth+1
				ret += isBugTile(self.width/2 + 1, self.height/2, depth: depth-1) ? 1 : 0
			default:
				ret += isBugTile(checkx, y, depth: depth) ? 1 : 0
			}
		}

		// check y values (up/down)
		for checky in [y - 1, y + 1] {
			if x == self.width/2 && checky == self.height/2 {
				// check side of inner map depth+1
				ret += bugsAtSide(depth: depth+1, side: (checky > y) ? .Top : .Bottom)
				continue
			}

			switch checky {
			case -1:
				// check the tile to our top on the outer map depth-1
				ret += isBugTile(self.width/2, self.height/2 - 1, depth: depth-1) ? 1 : 0
			case self.height:
				// check the tile to our right on the outer map depth-1
				ret += isBugTile(self.width/2, self.height/2 + 1, depth: depth-1) ? 1 : 0
			default:
				ret += isBugTile(x, checky, depth: depth) ? 1 : 0
			}
		}

		//print("(\(x),\(y)) => \(ret) nearby")
		return ret
	}

	public mutating func mutate() {
		var newRecursiveMaps = recursiveMaps

		// with each mutation, add new depth at both ends
		let mindepth = recursiveMaps.keys.min()!
		let maxdepth = recursiveMaps.keys.max()!
		newRecursiveMaps[mindepth - 1] = Map(width: self.width, height: self.height)
		newRecursiveMaps[maxdepth + 1] = Map(width: self.width, height: self.height)

		for depth in newRecursiveMaps.keys.sorted() {
			for y in 0 ..< self.height {
				for x in 0 ..< self.width {
					//print("mutate for depth \(depth), (\(x),\(y))")

					// try to use current map data as input, but instead
					// use an empty map when the given depth doesn't
					// exist in the current maps
					let oldmap = self.recursiveMaps[depth] ??
						Map(width: self.width, height: self.height)

					if oldmap.tiles[x][y] == .RecursiveGrid {
						continue
					}

					let b = bugsNearby(x, y, depth: depth)

					if oldmap.tiles[x][y] == .Infested {
						if b != 1 {
							newRecursiveMaps[depth]!.tiles[x][y] = .Empty
						}
					}

					if oldmap.tiles[x][y] == .Empty {
						if 1 ... 2 ~= b {
							newRecursiveMaps[depth]!.tiles[x][y] = .Infested
						}
					}
				}
			}
		}

		recursiveMaps = newRecursiveMaps
	}

	public func mapString(depth: Int) -> String {
		var ret = ""

		for y in 0 ..< self.height {
			for x in 0 ..< self.width {
				switch self.recursiveMaps[depth]!.tiles[x][y] {
				case .Infested: ret += "#"
				case .Empty: ret += "."
				case .RecursiveGrid: ret += "?"
				}
			}
			ret += "\n"
		}

		return ret
	}

	public var description: String {
		var s = ""

		for depth in self.recursiveMaps.keys.sorted() {
			if self.recursiveMaps[depth]!.bugCount > 0 {
				s += "Depth \(depth):\n"
				s += mapString(depth: depth)
				s += "\n"
			}
		}

		s += "bug count: \(self.bugCount)\n"

		return s
	}
}

var game = Game(fromFileName: "input")
print(game)

let iter = 200
for _ in 1 ... iter {
	game.mutate()
}

print("------------------------------------------------------------------------")
print("After \(iter)")
print(game)

