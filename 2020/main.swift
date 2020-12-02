import Foundation

var debugEnabled = false
var puzzleNameArg: String?

for arg in CommandLine.arguments[1...] {
	if arg == "-debug" {
		debugEnabled = true
		continue
	}

	guard puzzleNameArg == nil else { usage() }
	puzzleNameArg = arg
}

guard let puzzleName = puzzleNameArg else { usage() }

guard let puzzle = Puzzles[puzzleName] else {
	err("invalid puzzleName")
}

// Run all tests first
for test in puzzle.tests {
	debug(">>> Test(\(test.result))")
	let start = Date()
	let result = puzzle.implementation(test.input)
	let end = Date()

	guard result == test.result else {
		err("TEST FAILED: Expected result \(test.result) but got \(result)")
	}

	print(">>> Test(\(test.result)) time: \(elapsed(from: start, to: end))")
	print()
}

debug(">>> Start puzzle")
let start = Date()
let result = puzzle.implementation(puzzle.input)
let end = Date()

print(">>> RESULT: \(result)")
print("    Time:   \(elapsed(from: start, to: end))")

