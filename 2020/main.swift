import Foundation

guard CommandLine.arguments.count == 2 else {
	var e = ""

	e += "USAGE: \(CommandLine.arguments[0]) <puzzleName>\n"
	e += "\n"

	e += "Available puzzleNames:\n"
	Puzzles.keys.sorted().forEach { e += "- \($0)\n" }
	e += "\n"

	err(e)
}

guard let puzzle = Puzzles[CommandLine.arguments[1]] else {
	err("invalid puzzleName")
}

// Run all tests first
for test in puzzle.tests {
	let result = puzzle.implementation(test.input)
	guard result == test.result else {
		err("TEST FAILED: Expected result \(test.result) but got \(result)")
	}
}

// Now with full input!
let result = puzzle.implementation(puzzle.input)
print("RESULT: \(result)")

