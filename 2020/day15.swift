import Foundation

class Day15: PuzzleClass {
	func numbers(_ input: PuzzleInput, turns: Int) -> PuzzleResult {
		var byNumber = [Int:Int]()
		var numberSpoken: Int = -1

		for (turn, number) in input.intArray.enumerated() {
			byNumber[number] = turn + 1
		}

		var lastNumber = input.intArray.last!
		for i in (byNumber.count + 1)...turns {
			if let n = byNumber[lastNumber], n < (i - 1) {
				numberSpoken = i - n - 1
				//debug("n=\(n) numberSpoken=\(numberSpoken)")
			} else {
				numberSpoken = 0
			}

			debug("turn \(i) last was \(lastNumber) spoken \(numberSpoken)")
			byNumber[lastNumber] = i - 1
			lastNumber = numberSpoken
		}

		return numberSpoken
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return numbers(input, turns: 2020)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return numbers(input, turns: 30_000_000)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromString: "12,1,16,3,11,0"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "0,3,6"), result: 436),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromString: "12,1,16,3,11,0"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "15-input-test-part2"), result: 208),
			]
		),
	]

	required init() {}
}

