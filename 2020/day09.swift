class Day09: PuzzleClass {
	func part1rolling(_ input: PuzzleInput) -> Int {
		let buffer = input.intArray
		let preambleCount = buffer.count < 25 ? 5 : 25 // hack: preamble of test is 5 instead of 25

		for i in preambleCount..<buffer.count {
			let num = buffer[i]

			var isValid = false
			outer: for a in (i - preambleCount)..<i {
				guard buffer[a] < num else { continue }
				for b in (i - preambleCount)..<i {
					if buffer[a] + buffer[b] == num {
						isValid = true
						break outer
					}
				}
			}

			guard isValid else { return num }
		}

		err("nothing found?")
	}

	func part2rolling(_ input: PuzzleInput) -> Int {
		let buffer = input.intArray
		let invalidNum = part1rolling(input)
		var sum = 0

		var start = 0

		debug("wanted: \(invalidNum)")
		for end in 0..<buffer.count {
			sum += buffer[end]

			while sum > invalidNum {
				sum -= buffer[start]
				start += 1
			}

			if sum == invalidNum {
				let rolling = buffer[start...end]
				return rolling.min()! + rolling.max()!
			}
		}

		err("nope")
	}

	// -----

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
		let invalidNum = part1(input) as! Int

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
		"p1rolling": Puzzle(
			implementation: part1rolling,
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
		"p2rolling": Puzzle(
			implementation: part2rolling,
			input: PuzzleInput(fromFile: "09-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "09-input-test"), result: 62),
			]
		),
	]

	required init() {}
}

