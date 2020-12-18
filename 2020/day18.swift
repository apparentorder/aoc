class Day18: PuzzleClass {
	var isPart2 = false

	func calc(_ expression: [String]) -> Int {
		var e = expression

		debug("calc \(expression)")

		if isPart2 {
			// additions first
			for i in (0..<e.count).reversed() where e[i] == "+" {
				let n = Int(e[i-1])! + Int(e[i+1])!
				e.remove(at: i-1)
				e.remove(at: i-1)
				e[i-1] = String(n)
			}
		}

		var r = Int(e[0])!

		var i = 1
		while i < e.count {
			let op = e[i]
			let n = Int(e[i+1])!
			i += 2

			if op == "+" {
				r += n
			} else { // "*"
				r *= n
			}
		}

		return r
	}

	func eval(_ s: String) -> Int {
		var tokens = String(s.flatMap { (c: Character) -> String in
			if c == "(" { return "( " }
			if c == ")" { return " )" }
			return String(c)
		}).components(separatedBy: " ")

		while let parenClose = tokens.firstIndex(of: ")") {
			let parenOpen = tokens[0..<parenClose].lastIndex(of: "(")!
			let subExpression = tokens[parenOpen+1 ..< parenClose].map { String($0) }
			debug("sub-expression: \(subExpression)")

			let n = calc(subExpression)
			tokens.replaceSubrange(parenOpen ... parenClose, with: [String(n)])
		}

		debug("eval(\(s)) => \(calc(tokens))")
		return calc(tokens)
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		isPart2 = false
		return input.lines
			.map { eval($0) }
			.reduce(0, +)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		isPart2 = true
		return input.lines
			.map { eval($0) }
			.reduce(0, +)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "18-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "1 + 2 * 3 + 4 * 5 + 6"), result: 71),
				PuzzleTest(PuzzleInput(fromString: "1 + (2 * 3) + (4 * (5 + 6))"), result: 51),
				PuzzleTest(PuzzleInput(fromString: "2 * 3 + (4 * 5)"), result: 26),
				PuzzleTest(PuzzleInput(fromString: "5 + (8 * 3 + 9 + 3 * 4 * 3)"), result: 437),
				PuzzleTest(PuzzleInput(fromString: "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"), result: 12240),
				PuzzleTest(PuzzleInput(fromString: "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"), result: 13632),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "18-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "1 + 2 * 3 + 4 * 5 + 6"), result: 231),
				PuzzleTest(PuzzleInput(fromString: "1 + (2 * 3) + (4 * (5 + 6))"), result: 51),
				PuzzleTest(PuzzleInput(fromString: "2 * 3 + (4 * 5)"), result: 46),
				PuzzleTest(PuzzleInput(fromString: "5 + (8 * 3 + 9 + 3 * 4 * 3)"), result: 1445),
				PuzzleTest(PuzzleInput(fromString: "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"), result: 669060),
				PuzzleTest(PuzzleInput(fromString: "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"), result: 23340),
			]
		),
	]

	required init() {}
}

