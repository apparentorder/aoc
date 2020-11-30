import Foundation

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

