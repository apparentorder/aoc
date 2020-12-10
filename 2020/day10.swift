class Day10: PuzzleClass {
	//
	// Solving this puzzle relies on the assumption that input numbers are
	// in groups. Each group is at most five elements and the gap between
	// each group is exactly two numbers.
	//
	// Therefore, the number of different paths *per group* is easily calculated,
	// and the individual groups' path counts just need to be multiplied.
	//

	func adapterGroups(_ input: PuzzleInput) -> [[Int]] {
		let adapters = [0] + input.intArray.sorted()
		debug("\(adapters)")

		var group = [Int]()
		var groups = [[Int]]()
		var prev = -1

		for a in adapters {
			if a != prev + 1 {
				// new group
				groups += [group]
				group = []
			}

			group += [a]
			prev = a
		}

		// flush last
		groups += [group]

		groups.forEach { debug("group: \($0)") }

		return groups
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let groups = adapterGroups(input)
		let diff3 = groups.count
		let diff1 = groups.reduce(0, { $0 + $1.count - 1 })
		return diff1 * diff3
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let groups = adapterGroups(input)
		var paths = 1

		for group in groups {
			debug("group: \(group)")
			switch group.count {
			case 1: paths *= 1
			case 2: paths *= 1
			case 3: paths *= 2
			case 4: paths *= 4
			case 5: paths *= 7
			default: err("invalid group \(group)")
			}
		}

		return paths
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

