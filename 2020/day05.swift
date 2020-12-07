class Day05: PuzzleClass {
	struct BoardingPass: CustomStringConvertible {
		var seatId: Int
		var passId: String

		var seatRow: Int { seatId >> 3 }
		var seatColumn: Int { seatId & 7 }
		var description: String { "\(passId): row \(seatRow), column \(seatColumn), seat ID \(seatId)." }

		init(fromString s: String) {
			seatId = 0
			passId = s
			let chars = Array(String(s.reversed()))

			for i in 0..<chars.count {
				switch chars[i] {
				case "B", "R": seatId |= (1 << i)
				case "F", "L": break // already 0
				default: err("invalid boarding pass data: \(s)")
				}
			}
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let boardingPasses = input.lines.map { BoardingPass(fromString: $0) }
		boardingPasses.forEach { debug($0) }
		return boardingPasses.map { $0.seatId }.max()!
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let seats = input.lines
			.map { BoardingPass(fromString: $0).seatId }
			.sorted()

		debug(seats)

		for i in 1..<(seats.count - 1) {
			if seats[i + 1] != seats[i] + 1 {
				return seats[i] + 1
			}
		}

		err("no free seat :-(")
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "05-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "FBFBBFFRLR"), result: 357),
				PuzzleTest(PuzzleInput(fromString: "BFFFBBFRRR"), result: 567),
				PuzzleTest(PuzzleInput(fromString: "FFFBBBFRRR"), result: 119),
				PuzzleTest(PuzzleInput(fromString: "BBFFBBFRLL"), result: 820),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "05-input"),
			tests: []
		),
	]

	required init() {}
}

