import CryptoKit

// with all optimizations, still still takes an excessive amount of time
// (for part2 up to 40sec).
// there must be "a better solution" (i'm guessing it's related to an MD5
// prefix collision attack that I won't look up just to copy it)

class Day05: PuzzleClass {
	struct DoorCodeSequence: Sequence {
		let doorId: String

		func makeIterator() -> DoorCodeIterator {
			return DoorCodeIterator(doorId: doorId)
		}
	}

	struct DoorCodeIterator: IteratorProtocol {
		let doorId: String
		var index = 0

		let twoZeroBytes = Array(repeating: UInt8(0), count: 2)

		mutating func next() -> String? {
			// UNLIMITED SEQUENCE!
			while true {
				index += 1

				let message = doorId + String(index)
				let digest = Insecure.MD5.hash(data: message.data(using: .utf8)!)

				// we can easily skip hex values starting with "00 00" (i.e. two *bytes* of 0).
				guard digest.starts(with: twoZeroBytes) else { continue }

				// also note that we only need the first four bytes
				let hex = digest.prefix(4).map { String(format: "%02x", $0) }

				// still need to check if the fifth hex digit (third byte) also is zero.
				guard hex[2].first! == "0" else { continue }

				debug("\(message) -> \(hex.joined())")
				return hex.joined()
			}
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		var password = ""
		for hash in DoorCodeSequence(doorId: input.raw) {
			password += String(Array(hash)[5])
			debug("password: \(password)")

			guard password.count < 8 else { return password }
		}

		return "never returns"
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		var password = Array(repeating: Optional<Character>(nil), count: 8)

		for hash in DoorCodeSequence(doorId: input.raw) {
			let posStr = String(Array(hash)[5])

			guard let pos = Int(posStr), pos >= 0 && pos <= 7 else {
				debug("invalid pos \(posStr), skipping")
				continue
			}

			guard password[pos] == nil else {
				debug("pos \(pos) already known, skipping")
				continue
			}

			password[pos] = Array(hash)[6]
			debug("password: \(String(password.map { $0 ?? "_" }))")

			guard password.contains(nil) else { return String(password.map { $0! }) }
		}

		return "never returns"
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromString: "ffykfhsq"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "abc"), result: "18f47a30"),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromString: "ffykfhsq"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "abc"), result: "05ace8e3"),
			]
		),
	]

	required init() {}

}

