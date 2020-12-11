import Foundation

typealias Coordinates = (x: Int, y: Int)

func usage() -> Never {
	var e = ""

	e += "USAGE: aoc2020 [-debug] <puzzleClassName> <puzzleName>\n"
	e += "\n"

	e += "Available puzzleClassNames:\n"
	PuzzleClasses.keys.sorted().forEach { e += "- \($0)\n" }
	e += "(or 'all')\n"
	e += "\n"

	err(e)
}

func elapsed(from start: Date, to end: Date) -> String {
	return String(format: "%.3fms", end.timeIntervalSince(start) * 1000)
}

func printerr(_ s: String) {
	FileHandle.standardError.write(s.data(using: .utf8)!)
}

func err(_ errorMessage: String) -> Never {
	print("     .")
	print("    / \\")
	print("   / ! \\")
	print("  '-----'")
	print()

	var e = errorMessage

	// add \n if necessary
	if let lastChar = e.last {
		if lastChar != "\n" {
			e += "\n"
		}
	}

	printerr(e)
	exit(69)
}

