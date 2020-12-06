class Day06 {
	static func parseGroups (inputLines: [String]) -> [Int] {
		var answer = 0
		var r = [Int]()

		for line in inputLines {
			guard !line.isEmpty else {
				// next group
				debug("group answer \(answer)")
				r += [answer]
				answer = 0
				continue
			}

			for question in line {
				answer |= 1 << (question.asciiValue! - 97)
			}
		}

		// last group
		debug("group answer \(answer)")
		r += [answer]
			
		return r
	}

	static func parsev2(inputLines: [String]) -> PuzzleResult {
		var answers = [Character:Int]()
		var paxInGroup = 0
		var sum = 0

		for line in inputLines {
			guard !line.isEmpty else {
				debug("group answers \(answers) for \(paxInGroup) passengers")
				for (_, v) in answers {
					if v == paxInGroup {
						sum += 1
					}
				}
				answers = [Character:Int]()
				paxInGroup = 0
				continue
			}

			paxInGroup += 1
			for question in line {
				answers[question] = (answers[question] ?? 0) + 1
			}
		}

		debug("group answers \(answers) for \(paxInGroup) passengers")
		for (_, v) in answers {
			if v == paxInGroup {
				sum += 1
			}
		}

		return sum
	}

	static func part1(_ input: PuzzleInput) -> PuzzleResult {
		var sum = 0

		for answer in parseGroups(inputLines: input.lines) {
			debug("\(answer) ...")
			for i in 0..<26 {
				if answer & (1 << i) != 0 {
					debug("... bit \(i)")
					sum += 1
				}
			}
		}

		return sum
	}

	static func part2(_ input: PuzzleInput) -> PuzzleResult {
		return parsev2(inputLines: input.lines)
	}
}

