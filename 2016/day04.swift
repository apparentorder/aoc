class Day04: PuzzleClass {
	struct Room {
		let name: String
		let sectorId: Int
		let checksum: String

		var decodedName: String {
			var decodedName = name

			for _ in 0..<sectorId {
				var nextDecodedName = ""
				for c in decodedName {
					guard c != "z" else {
						nextDecodedName += "a"
						continue
					}

					guard c != "-" && c != " " else {
						nextDecodedName += " "
						continue
					}

					nextDecodedName += String(UnicodeScalar(c.asciiValue! + 1))
				}

				decodedName = nextDecodedName
			}

			return decodedName
			// yes, this could be much faster.
		}

		init?(_ s: String) {
			// example input string: aaaaa-bbb-z-y-x-123[abxyz]

			var letterCounts = [Character:Int]()

			let split = s.components(separatedBy: "[")
			checksum = String(split[1].dropLast())

			let nameSplit = split[0].components(separatedBy: "-")
			sectorId = Int(nameSplit.last!)!
			name = nameSplit.dropLast().joined(separator: "-")

			for c in name where c != "-" {
				letterCounts[c] = (letterCounts[c] ?? 0) + 1
			}

			var computedChecksum = ""
			while computedChecksum.count < 5 {
				let highestCount = letterCounts.values.max()!
				let highestLetters = letterCounts.filter { $0.value == highestCount }.keys

				let nextLetter = highestLetters.sorted().first!
				letterCounts.removeValue(forKey: nextLetter)

				computedChecksum += String(nextLetter)
			}

			debug(
				"room \(name) sectorId \(sectorId) checksum "
				+ "given \(checksum) checksum computed \(computedChecksum) --> "
				+ "\(computedChecksum == checksum ? "valid" : "INVALID")"
			)

			guard computedChecksum == checksum else { return nil }
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		var rooms = [Room]()

		for line in input.lines {
			if let r = Room(line) {
				rooms += [r]
			}
		}

		return rooms.map { $0.sectorId }.reduce(0, +)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		var rooms = [Room]()

		for line in input.lines {
			if let r = Room(line) {
				rooms += [r]
			}
		}

		rooms.forEach { debug("\($0.decodedName) (\($0.name))") }

		// name found by manual inspection of decoded names (grep pole)
		return rooms.filter { $0.decodedName == "northpole object storage" }.first!.sectorId
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "04-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "04-input-test"), result: 1514),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "04-input"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "04-test1"), result: 241861950),
			]
		),
	]

	required init() {}

}

