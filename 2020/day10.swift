class Day10: PuzzleClass {
	func foo(_ intArray: [Int], isPart2: Bool) -> PuzzleResult {
		var adapters = intArray

		var diff1 = 0
		var diff2 = 0
		var diff3 = 0
		var last = 0
		//var totalOptions = 1

		while !adapters.isEmpty {
			debug("\(last) => \(adapters)")
			//var options = 0

			let containsPlus1 = adapters.contains(last + 1)
			let containsPlus2 = adapters.contains(last + 2)
			let containsPlus3 = adapters.contains(last + 3)

			if containsPlus1 {
				adapters.removeAll(where: { $0 == last + 1 })
				last += 1
				diff1 += 1
				continue
			}

			if containsPlus2 {
				adapters.removeAll(where: { $0 == last + 2 })
				last += 2
				diff2 += 1
				continue
			}

			if containsPlus3 {
				adapters.removeAll(where: { $0 == last + 3 })
				last += 3
				diff3 += 1
				continue
			}

			err("no matching adapter")
		}

		// "your device's built-in adapter is always 3 higher than the highest adapter"
		diff3 += 1

		//return isPart2 ? totalOptions : diff1 * diff3
		return isPart2 ? 0 : diff1 * diff3
	}

	func countPaths(lastUsed: Int, adaptersLeft: [Int], adaptersUsed: [Int]) -> Int {
		debug("countPaths with lastUsed \(lastUsed)")
		var paths = 0

		guard !adaptersLeft.isEmpty else {
			debug("valid path: \(adaptersUsed)")
			return 1
		}

		for a in adaptersLeft {
			//debug("\(a)?")
			if a >= lastUsed + 1 && a <= lastUsed + 3 {
				debug("\(a)!")
				paths += countPaths(
					lastUsed: a,
					adaptersLeft: adaptersLeft.filter { $0 != a },
					adaptersUsed: adaptersUsed + [a]
				)
			}
		}

		return paths
	}

	func meh(_ input: PuzzleInput) -> Int {
		let adapters = [0] + input.intArray.sorted()
		debug("\(adapters)")

		var block = [Int]()
		var blocks = [[Int]]()
		var paths = 1

		for a in adapters {
			if a != (block.max() ?? -1) + 1 {
				// new block
				blocks += [block]
				block = []
			}

			block += [a]
		}

		// flush last
		blocks += [block]

		for block in blocks {
			debug("block: \(block)")
			switch block.count {
			case 1: paths *= 1
			case 2: paths *= 1
			case 3: paths *= 2
			case 4: paths *= 4
			case 5: paths *= 7
			default: err("invalid block \(block)")
			}
		}

		return paths
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return foo(input.intArray, isPart2: false)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		//let a = input.intArray
		//return countPaths(lastUsed: 0, adaptersLeft: a, adaptersUsed: [])
		return meh(input)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "10-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "10-input-test1"), result: 7 * 5),
				PuzzleTest(PuzzleInput(fromFile: "10-input-test2"), result: 22 * 10),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "10-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "10-input-test1"), result: 8),
				PuzzleTest(PuzzleInput(fromFile: "10-input-test2"), result: 19208),
			]
		),
	]

	required init() {}
}

