class Day07: PuzzleClass {
	struct IPv7 {
		let address: String

		struct Sequence {
			let sequence: String
			let isHypernet: Bool

			var containsAbba: Bool {
				let t = Array(sequence)

				for i in 0..<(t.count - 3) {
					if t[i+3] == t[i] && t[i+1] == t[i+2] && t[i] != t[i+1] {
						return true
					}
				}

				return false
			}

			var abaSequences: [String] {
				let t = Array(sequence)
				var r = [String]()

				for i in 0..<(t.count - 2) {
					if t[i+2] == t[i] && t[i] != t[i+1] {
						r += [String(t[i...i+2])]
					}
				}

				return r
			}

		}

		var supportsTLS: Bool {
			// supports TLS when *any* supernet sequence has an ABBA...
			guard (
				self.supernetSequences
				.contains(where: { $0.containsAbba })
			) else { return false }

			// ... but *none* of the hypernet sequences have an ABBA.
			guard (
				self.hypernetSequences
				.allSatisfy { !$0.containsAbba }
			) else { return false }

			return true
		}

		var supportsSSL: Bool {
			for seq in self.supernetSequences.flatMap({ $0.abaSequences }).map(Array.init) {
				let bab = String([seq[1], seq[0], seq[1]])
				if self.hypernetSequences.contains(where: { $0.sequence.contains(bab) }) {
					return true
				}
			}

			return false
		}

		var hypernetSequences: [Sequence] { self.sequences.filter { $0.isHypernet } }

		var supernetSequences: [Sequence] { self.sequences.filter { !$0.isHypernet } }

		var sequences: [Sequence] {
			var r = [Sequence]()
			var isHyper = false
			var a = address

			while !a.isEmpty {
				guard !isHyper else {
					let parts = a.components(separatedBy: "]")
					r += [Sequence(sequence: parts[0], isHypernet: true)]
					a.removeFirst(parts[0].count + 1)
					isHyper = false
					continue
				}

				let parts = a.components(separatedBy: "[")

				r += [Sequence(sequence: parts[0], isHypernet: false)]
				a.removeFirst(parts[0].count)

				if parts.count > 1 {
					a.removeFirst() // "["
					isHyper = true
				}
			}

			return r
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return input.lines.map { IPv7(address: $0) }.filter { $0.supportsTLS }.count
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return input.lines.map { IPv7(address: $0) }.filter { $0.supportsSSL }.count
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "07-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "07-input-test"), result: 2),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "07-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "07-input-test-part2"), result: 3),
			]
		),
	]

	required init() {}

}

