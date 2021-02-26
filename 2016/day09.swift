class Day09: PuzzleClass {
	//
	// approach:
	//
	// 1) parse the input string into a tree structure (using a simple recursive enum),
	//    storing strings (and for part 2: sub-trees) and their respective repeat counts
	// 2) walk through the tree and just sum up string lenghts * repeat counts
	//
	// a full decompress of the real puzzle input is possible -- it solves in about two minutes to
	// a string of ~10 GB (!). it's pretty clear this wasn't an intended approach. ;)
	// therefore, the decompress() function is here only as a proof of concept, but not used.
	//

	indirect enum Token: CustomStringConvertible {
		case token([Token], repeatCount: Int)
		case string(String, repeatCount: Int)

		var description: String {
			switch self {
				case let .token(_, r): return "<token>x\(r)"
				case let .string(s, r): return "\"\(s)\"x\(r)"
			}
		}
	}

	func decompress(_ tokens: [Token]) -> String {
		var s = ""
		for token in tokens {
			switch token {
			case let .string(string, r): s += String(repeating: string, count: r)
			case let .token(t, r): s += String(repeating: decompress(t), count: r)
			}
		}

		return s
	}

	func decompressedSize(_ tokens: [Token]) -> Int {
		var s = 0
		for token in tokens {
			switch token {
			case let .string(string, r): s += string.count * r
			case let .token(t, r): s += decompressedSize(t) * r
			}
		}

		return s
	}

	func parse(_ input: String, recursive: Bool) -> [Token] {
		// sequentially parse the input string.
		// for each marker found, we store the amount of characters given in the marker.
		// only if 'recursive' (part 2), we then recurse to parse the captured string further.

		enum parseState {
			case parsingVerbatim
			case parsingMarker
			case parsingRepeatBuffer
		}

		var tokens = [Token]()
		var marker = ""
		var buffer = ""
		var repeatBuffer = ""
		var repeatCount = -1
		var repeatLength = -1
		var state = parseState.parsingVerbatim

		for char in input {
			guard !char.isWhitespace else { continue }

			switch state {
			case .parsingVerbatim:
				guard char != "(" else {
					if !buffer.isEmpty {
						tokens += [Token.string(buffer, repeatCount: 1)]
					}

					state = .parsingMarker
					marker = ""
					continue
				}

				buffer += [char]

			case .parsingRepeatBuffer:
				repeatLength -= 1
				repeatBuffer += [char]

				guard repeatLength > 0 else {
					if recursive {
						//repeatBuffer = decompress(repeatBuffer, recursive: true)
						tokens += [Token.token(parse(repeatBuffer, recursive: true), repeatCount: repeatCount)]
					} else {
						tokens += [Token.string(repeatBuffer, repeatCount: repeatCount)]
					}

					state = .parsingVerbatim
					buffer = ""

					continue
				}

			case .parsingMarker:
				guard char != ")" else {
					let parts = marker.components(separatedBy: "x")
					repeatLength = Int(parts[0])!
					repeatCount = Int(parts[1])!

					state = .parsingRepeatBuffer
					repeatBuffer = ""

					continue
				}

				marker += [char]
			}
		}

		guard state == .parsingVerbatim else { err("invalid parse state \(state) after input") }

		// flush remaining buffer, if any
		if !buffer.isEmpty {
			tokens += [Token.string(buffer, repeatCount: 1)]
		}

		debug("\(input) -> \(tokens)")
		return tokens
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let tokens = parse(input.raw, recursive: false)
		return decompressedSize(tokens)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let tokens = parse(input.raw, recursive: true)
		return decompressedSize(tokens)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "09-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "ADVENT"), result: 6),
				PuzzleTest(PuzzleInput(fromString: "A(1x5)BC"), result: 7),
				PuzzleTest(PuzzleInput(fromString: "(3x3)XYZ"), result: 9),
				PuzzleTest(PuzzleInput(fromString: "A(2x2)BCD(2x2)EFG"), result: 11),
				PuzzleTest(PuzzleInput(fromString: "(6x1)(1x3)A"), result: 6),
				PuzzleTest(PuzzleInput(fromString: "X(8x2)(3x3)ABCY"), result: 18),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "09-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "(3x3)XYZ"), result: 9),
				PuzzleTest(PuzzleInput(fromString: "X(8x2)(3x3)ABCY"), result: 20),
				PuzzleTest(PuzzleInput(fromString: "(27x12)(20x12)(13x14)(7x10)(1x12)A"), result: 241920),
				PuzzleTest(PuzzleInput(fromString: "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"), result: 445),
			]
		),
	]

	required init() {}

}

