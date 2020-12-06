
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
			d += String(row)
			d += "\n"
		}
		return d
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

