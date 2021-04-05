class Day16: PuzzleClass {
	//
	// simple/wasteful approach, p2 runs in ~24s / ~3s
	//
	struct DragonData: CustomStringConvertible {
		let input: [UInt8]
		let data: [UInt8]

		var description: String {
			var s = ""

			for i in 0..<data.count {

				if i % ((input.count + 1) * 2) == 0 {
					s += "\n"
				}
				if i % (input.count + 1) == input.count {
					s += "_" + String(data[i]) + "_"
				} else {
					s += String(data[i])
				}
			}

			//let s = data.reduce("", { $0 + String($1) })
			return "\(s) [cksum \(checksum)]"
		}

		var checksum: String {
			var r = data
			var rNext = [UInt8]()
			rNext.reserveCapacity(data.count)

			repeat {
				rNext.removeAll(keepingCapacity: true)
				for pairStart in stride(from: 0, to: r.count, by: 2) {
					let isSame = (r[pairStart] == r[pairStart + 1])
					rNext += isSame ? [1] : [0]
				}

				r = rNext
			} while r.count % 2 != 1

			return r.reduce("", { $0 + String($1) })
		}

		init(initialState: [UInt8], length: Int) {
			guard length % 2 == 0 else {
				err("uneven lengths are not supported")
			}

			self.input = initialState

			var a = initialState
			a.reserveCapacity(length)

			while a.count < length {
				a += [0] + a.reversed().map { ($0 & 1) ^ 1 }
			}

			self.data = Array(a.prefix(length))
		}

		init(initialState: String, length: Int) {
			self.init(initialState: initialState.map { UInt8(String($0))! }, length: length)
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let comp = input.raw.components(separatedBy: " ")
		let dd = DragonData(initialState: comp[0], length: Int(comp[1])!)
		debug(dd)
		return dd.checksum
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let comp = input.raw.components(separatedBy: " ")
		let dd = DragonData(initialState: comp[0], length: Int(comp[1])!)
		return dd.checksum
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromString: "10001001100000001 272"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "10000 20"), result: "01100"),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromString: "10001001100000001 35651584"),
			tests: []
		),
	]

	required init() {}

}

