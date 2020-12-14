class Day14: PuzzleClass {
	let maxInt36 = 68_719_476_735

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		var program = input.lines
		var memory = Array(repeating: 0, count: 100_000)
		var mask = [Character]()

		while !program.isEmpty {
			var foo = program.removeFirst()

			guard !foo.hasPrefix("mask") else {
				// done, next prefix
				foo.removeFirst("mask = ".count)
				mask = Array(foo)
				debug("mask = \(mask)")
				continue
			}

			let c = foo.components(separatedBy: " ")
			var addressString = c[0]
			var value = Int(c[2])!

			addressString.removeFirst("mem[".count)
			addressString.removeLast("]".count)
			let address = Int(addressString)!

			for i in 0..<36 {
				let bit = 35 - i
				switch mask[i] {
				case "X":
					break // no change
				case "0":
					debug("modifying \(value) i=\(i) bit=\(bit)")
					value &= (maxInt36 ^ (1<<bit))
					debug("now \(value)")
				case "1":
					debug("modifying \(value) i=\(i) bit=\(bit)")
					value |= (1 << bit)
					debug("now \(value)")
				default:
					err("invalid mask: \(mask)")
				}
			}

			debug("storing \(value) at \(address)")
			debug("")
			memory[address] = value
		}

		return memory.reduce(0, +)
	}

	func addressList(fromMask mask: [Character]) -> [Int] {
		var r = [Int]()

		guard let x = mask.firstIndex(of: "X") else {
			var n = 0
			for i in 0..<36 where mask[i] == "1" {
				let bit = 35 - i
				n |= (1 << bit)
			}

			return [n]
		}

		var newMask = mask
		newMask[x] = "0"
		r += addressList(fromMask: newMask)

		newMask[x] = "1"
		r += addressList(fromMask: newMask)

		return r
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		var program = input.lines
		var memory = [Int:Int]()
		var mask = [Character]()

		while !program.isEmpty {
			var foo = program.removeFirst()

			guard !foo.hasPrefix("mask") else {
				// done, next prefix
				foo.removeFirst("mask = ".count)
				mask = Array(foo)
				debug("mask = \(mask)")
				continue
			}

			let c = foo.components(separatedBy: " ")
			var addressString = c[0]
			let value = Int(c[2])!

			addressString.removeFirst("mem[".count)
			addressString.removeLast("]".count)
			var address = Int(addressString)!

			for i in 0..<36 {
				let bit = 35 - i
				switch mask[i] {
				case "X":
					break // no change yet (floating, handled below)
				case "0":
					break // no change at all
				case "1":
					debug("modifying \(address) i=\(i) bit=\(bit)")
					address |= (1 << bit)
					debug("now \(address)")
				default:
					err("invalid mask: \(mask)")
				}
			}

			var newMask = mask
			for i in 0..<36 where newMask[i] != "X" {
				let bit = 35 - i
				newMask[i] =  address & (1<<bit) > 0 ? "1" : "0"
			}

			let al = addressList(fromMask: newMask)
			al.forEach {
				debug("storing \(value) at address \($0)")
				memory[$0] = value
			}

			debug("")
		}

		return memory.values.reduce(0, +)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "14-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "14-input-test"), result: 165),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "14-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "14-input-test-part2"), result: 208),
			]
		),
	]

	required init() {}
}

