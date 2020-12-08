import Foundation

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
	return String(format: "%.4fs", end.timeIntervalSince(start))
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

//
// A word about performance:
//
// Swift will *always* evaluate a string constant. This means that the
// performance of debug("foo \(bar)") will mirror the complexity of
// describing `bar`. If this is a comlex and/or nested structure, the
// performance will be abysmal, especially when used e.g. in a
// high-iteration loop.
//
// This is true even if the debug() function body were completely empty
// and is optimized away by the -O flag. In other words: This performance
// impact will affect execution without debug output just as well.
//
// Try using debug() in a way that passes arguments instead of describing
// them in those cases, e.g. debug("foo", bar).
//
func debug(_ args: Any...) {
	guard debugEnabled else { return }
	let s = args.map { String(describing: $0) }
	print(s.joined(separator: " "))
}

