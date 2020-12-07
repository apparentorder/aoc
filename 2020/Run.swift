import Foundation

func runPuzzle(_ puzzleClassObject: PuzzleClass, _ puzzleName: String) {
	let puzzle = puzzleClassObject.puzzleConfig[puzzleName]!

	// Run all tests first
	for test in puzzle.tests {
		debug(">>> Test(\(test.result))")
		let testInstance = type(of: puzzleClassObject).init()

		let start = Date()
		let result = testInstance.puzzleConfig[puzzleName]!.implementation(test.input)
		let end = Date()

		guard result == test.result else {
			err("TEST FAILED: Expected result \(test.result) but got \(result)")
		}

		print(">>> Test(\(test.result)) time: \(elapsed(from: start, to: end))")
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

