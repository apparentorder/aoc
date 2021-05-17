class Day20: PuzzleClass {
	struct Rule {
		let startAddress: Int
		let endAddress: Int
	}

	func allowed(rules: [Rule], returnFirst: Bool) -> Int {
		var address = 0
		var matchCount = 0

		outer: while address <= (1<<32) {
			debug("address \(address)")

			for rule in rules {
				guard !((rule.startAddress...rule.endAddress) ~= address) else {
					address = rule.endAddress + 1
					continue outer
				}
			}

			// if control reaches here, we're not blacklisted.

			// either return the address (for part1)
			guard !returnFirst else {
				return address
			}

			// ... or count the addresses until the next blacklist range starts (or we hit the end)
			if let nextStart = rules.map { $0.startAddress }.filter({ $0 >= address }).min() {
				matchCount += (nextStart - address)
				address = nextStart
			} else {
				matchCount += ((1<<32) - address)
				address = 1<<33 // anything >2^32
			}
		}

		return matchCount
	}

	func parseRules(_ lines: [String]) -> [Rule] {
		var r = [Rule]()
		r.reserveCapacity(lines.count)

		for line in lines {
			let parts = line.components(separatedBy: "-")
			let from = Int(parts[0])!
			let to = Int(parts[1])!

			r += [Rule(startAddress: from, endAddress: to)]
		}

		return r
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return allowed(rules: parseRules(input.lines), returnFirst: true)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return allowed(rules: parseRules(input.lines), returnFirst: false)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "20-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "20-input-test"), result: 3),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "20-input"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "20-test1"), result: 241861950),
			]
		),
	]

	required init() {}

}

