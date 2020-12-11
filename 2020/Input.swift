
import Foundation

class PuzzleInput {
	let raw: String

	var intArray: [Int] {
		return self.tokens.map { Int($0)! }
	}

	var tokens: [String] {
		let isSeparator = { (c: Character) -> Bool in
			if c == "\n" { return true }
			if c == "," { return true }
			if c == " " { return true }
			return false
		}

		let substrings = self.raw.split(whereSeparator: isSeparator)
		return substrings.map { String($0) }
	}

	var lines: [String] {
		var lines = raw.split(separator: "\n", omittingEmptySubsequences: false).map { String($0) }
		if let x = lines.last, x.count == 0 {
			lines.removeLast()
		}
		return lines
	}

	var lineGroups: [[String]] {
		var buf = [String]()
		var r = [[String]]()

		for line in lines {
			guard !line.isEmpty else {
				r += [buf]
				buf.removeAll()
				continue
			}

			buf += [line]
		}

		// flush last one, if any
		if buf.count > 0 {
			r += [buf]
		}

		return r
	}

	var matrix: Matrix {
		Matrix(fromString: raw)
	}

	init(fromFile fileName: String) {
		do {
			raw = try String(contentsOfFile: "Data/\(fileName)")
		} catch {
			err(error.localizedDescription)
		}
	}

	init(fromString s: String) {
		raw = s
	}
}

struct Matrix: CustomStringConvertible {
	var data: [[Character]]

	var rows: Int { data.count }
	var columns: Int { data[0].count }

	var description: String {
		var d = "[Matrix, rows = \(self.rows), columns = \(self.columns)]\n"
		for row in data {
			row.forEach { d += "\($0) " }
			d += "\n"
		}
		return d
	}

	func findFirstCharacter(
		except: Character,
		inDirection increment: (x: Int, y: Int),
		fromCoordinates from: (x: Int, y: Int),
		maxIterations: Int?
	) -> Character? {
		var currentX = from.x
		var currentY = from.y
		var iterations = 0

		debug("Matrix.charactersInDirection from \(from.x),\(from.y) moving \(increment.x),\(increment.y)")

		guard increment.x != 0 || increment.y != 0 else { return nil } // nobody likes infinite loops (except Apple)

		while true {
			currentX += increment.x
			currentY += increment.y
			iterations += 1

			guard maxIterations == nil || maxIterations! >= iterations else { return nil }
			guard currentX >= 0 && currentX < self.columns else { return nil }
			guard currentY >= 0 && currentY < self.rows else { return nil }

			let c = getChar(atCoordinates: currentX, currentY)
			guard c == except else { return c }
		}
	}

	mutating func setChar(atCoordinates x: Int, _ y: Int, to c: Character) {
		data[y][x] = c
	}

	mutating func setChar(atIndex row: Int, _ column: Int, to c: Character) {
		data[row][column] = c
	}

	func getChar(atCoordinates x: Int, _ y: Int) -> Character {
		return data[y][x]
	}

	func getChar(atIndex row: Int, _ column: Int) -> Character {
		return data[row][column]
	}

	init(fromString s: String) {
		var r = [[Character]]()

		for line in s.split(separator: "\n").map({ String($0) }) {
			r += [Array(line)]
		}

		data = r
	}
}

