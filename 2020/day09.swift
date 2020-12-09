class Day09: PuzzleClass {
	func part1(_ input: PuzzleInput) -> PuzzleResult {
		var buffer = input.intArray
		let preambleCount = buffer.count < 25 ? 5 : 25 // hack: preamble of test is 5 instead of 25

		var preamble = buffer[0..<preambleCount]
		buffer.removeFirst(preambleCount)

		while let num = buffer.first {
			var isValid = false
			outer: for a in preamble {
				guard a < num else { continue }
				for b in preamble {
					if a + b == num {
						isValid = true
						break outer
					}
				}
			}

			guard isValid else { return num }

			buffer.removeFirst()
			preamble.removeFirst()
			preamble.append(num)
		}

		err("nothing found?")
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let buffer = input.intArray
		let invalidNum = part1(input)

		for (i, a) in buffer.enumerated() {
			var nums = [a]
			var sum = 0
			for b in buffer[(i+1)...] {
				guard sum < invalidNum else { break }
				nums += [b]
				sum += b
				if sum == invalidNum {
					return nums.min()! + nums.max()!
				}
			}
		}

		err("nothing found?")
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "09-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "09-input-test"), result: 127),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "09-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "09-input-test"), result: 62),
			]
		),
	]

	required init() {}
}

