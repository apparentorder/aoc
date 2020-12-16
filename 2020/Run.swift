import Foundation

func runPuzzle(_ puzzleClassObject: PuzzleClass, _ puzzleName: String) {
	let puzzle = puzzleClassObject.puzzleConfig[puzzleName]!

	// Run all tests first
	for test in puzzle.tests {
		let resultString = test.result == nil ? "(nil)" : String(test.result!)
		debug(">>> Test(\(resultString))")

		let testInstance = type(of: puzzleClassObject).init()

		let start = Date()
		let result = testInstance.puzzleConfig[puzzleName]!.implementation(test.input)
		let end = Date()

		if let expected = test.result {
			guard expected == result else {
				err("TEST FAILED: Expected result \(expected) but got \(result)")
			}
		} else {
			debug("(result ignored!)")
		}

		print(">>> Test(\(resultString)) time: \(elapsed(from: start, to: end))")
		print()
	}

	debug(">>> Start puzzle")
	let puzzleInstance = type(of: puzzleClassObject).init()
	let start = Date()
	let result = puzzleInstance.puzzleConfig[puzzleName]!.implementation(puzzle.input)
	let end = Date()

	print(">>> RESULT: \(result)")
	print("    Time:   \(elapsed(from: start, to: end))")
}

