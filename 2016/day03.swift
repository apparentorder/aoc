class Day03: PuzzleClass {
	func countValidTriangles(_ intlist: [Int], isPart2: Bool) -> Int {
		var r = 0

		for i in 0..<intlist.count/3 {
			let base = isPart2 ? 3*3*(i/3) + (i%3): i*3
			let skew = isPart2 ? 3 : 1
			let side1 = intlist[base + skew*0]
			let side2 = intlist[base + skew*1]
			let side3 = intlist[base + skew*2]

			if (
				side1 + side2 > side3 &&
				side1 + side3 > side2 &&
				side2 + side3 > side1
			) {
				r += 1
			}
		}

		return r
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return countValidTriangles(input.intArray, isPart2: false)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return countValidTriangles(input.intArray, isPart2: true)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "03-input"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "03-test1"), result: 514579),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "03-input"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "03-test1"), result: 241861950),
			]
		),
	]

	required init() {}

}

