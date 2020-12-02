class Day02 {
	struct Password: CustomStringConvertible {
		var digit1: Int
		var digit2: Int
		var char: Character
		var password: String

		var isValidPart1: Bool {
			let charCount = password.reduce(0, { $0 + ($1 == char ? 1 : 0) })
			return (charCount >= digit1 && charCount <= digit2)
		}

		var isValidPart2: Bool {
			var matchCount = 0
			matchCount += Array(password)[digit1 - 1] == char ? 1 : 0
			matchCount += Array(password)[digit2 - 1] == char ? 1 : 0
			return matchCount == 1
		}

		var description: String {
			return "(\(digit1),\(digit2)/\(char)) \(password) (p1: \(isValidPart1)) (p2: \(isValidPart2))"
		}
	}

	static func parsePw(passwordLines: [String]) -> [Password] {
		var pwList = [Password]()

		for password in passwordLines {
			let parts = password.split(separator: " ")

			let limits = parts[0].split(separator: "-").map { Int($0)! }

			let pw = Password(
				digit1: limits[0],
				digit2: limits[1],
				char: parts[1].first!,
				password: String(parts[2])
			)

			print(pw)
			pwList += [pw]
		}

		return pwList
	}

	static func part1(_ input: PuzzleInput) -> PuzzleResult {
		let pwList = parsePw(passwordLines: input.lines)
		return pwList.reduce(0, { $0 + ($1.isValidPart1 ? 1 : 0) })
	}

	static func part2(_ input: PuzzleInput) -> PuzzleResult {
		let pwList = parsePw(passwordLines: input.lines)
		return pwList.reduce(0, { $0 + ($1.isValidPart2 ? 1 : 0) })
	}
}

