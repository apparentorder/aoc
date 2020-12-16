//
// N.B.: This is version is a bit more cleaned up, generalized and optimized. For the version
// used to solve at first, see git history.
//
class Day01: PuzzleClass {
	func findSum(_ sum: Int, inArray remaining: [Int], maxDepth: Int, having: [Int]) -> [Int] {
		let currentSum = having.reduce(0, +)

		guard having.count != maxDepth else {
			// max. depth reached
			if currentSum == sum { return having }
			return []
		}

		guard currentSum < sum else {
			// no point in checking further if we already overshot
			return []
		}

		guard remaining.count > 0 else { return [] }

		var a = remaining
		while a.count > 0 {
			let next = a.removeFirst()
			let r = findSum(sum, inArray: a, maxDepth: maxDepth, having: having + [next])

			if r.count > 0 { return r }
		}

		return []
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let entries = findSum(2020, inArray: input.intArray, maxDepth: 2, having: [])
		return entries.reduce(1, *)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let entries = findSum(2020, inArray: input.intArray, maxDepth: 3, having: [])
		return entries.reduce(1, *)
	}

	func part2nonRecursive(_ input: PuzzleInput) -> PuzzleResult {
		let a = input.intArray
		for (i, v) in a.enumerated() {
			for (j, v2) in a[i...].enumerated() {
				for v3 in a[j...] {
					if v+v2+v3 == 2020 { return v*v2*v3 }
				}
			}
		}

		err("no result")
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "01-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "01-test1"), result: 514579),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "01-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "01-test1"), result: 241861950),
			]
		),
		"p2nr": Puzzle(
			implementation: part2nonRecursive,
			input: PuzzleInput(fromFile: "01-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "01-test1"), result: 241861950),
			]
		),
	]

	required init() {}

}

