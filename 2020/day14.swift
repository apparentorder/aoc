import Foundation

class Day14: PuzzleClass {
	struct Mask {
		// keep track of which 0/1/X are at which position (i.e. which bits they represent)
		var bits0 = [Int]()
		var bits1 = [Int]()
		var bitsX = [Int]()

		init(_ s: String) {
			let chars = Array(s).reversed()
			for (i, c) in chars.enumerated() {
				switch c {
				case "0": bits0 += [i]
				case "1": bits1 += [i]
				case "X": bitsX += [i]
				default: err("invalid mask \(s)")
				}
			}
		}
	}

	func parseAndRun(_ program: [String], isPart2: Bool) -> PuzzleResult {
		var mask = Mask("")
		var writes = 0
		var memory = [Int:Int]() // [MemoryAddress:Value]
		let junkChars = CharacterSet(charactersIn: " =[]")

		for instruction in program {
			let components = instruction
				.components(separatedBy: junkChars)
				.filter { !$0.isEmpty }

			guard components[0] != "mask" else {
				mask = Mask(components[1])
				debug("mask = \(mask)")
				continue
			}

			var address = Int(components[1])!
			var value = Int(components[2])!
			var allAddresses: [Int]

			if !isPart2 {
				applyMask(mask, toNumber: &value, ignoringZero: false)
				allAddresses = [address]
			} else {
				applyMask(mask, toNumber: &address, ignoringZero: true)
				allAddresses = floatingAddresses(fromNumber: address, usingMask: mask)
			}

			for a in allAddresses {
				debug("write value \(value) to address \(a)")
				writes += 1
				memory[a] = value
			}
		}

		debug("writes: \(writes)")
		return memory.values.reduce(0, +)
	}

	func floatingAddresses(fromNumber number: Int, usingMask mask: Mask, xIndex: Int = 0) -> [Int] {
		var r = [Int]()
		var n = number

		guard xIndex < mask.bitsX.count else { return [n] }

		let bit = mask.bitsX[xIndex]
		clearBit(bit, inNumber: &n)
		r += floatingAddresses(fromNumber: n, usingMask: mask, xIndex: xIndex + 1)

		setBit(bit, inNumber: &n)
		r += floatingAddresses(fromNumber: n, usingMask: mask, xIndex: xIndex + 1)

		return r
	}

	func applyMask(_ mask: Mask, toNumber number: inout Int, ignoringZero: Bool) {
		mask.bits1.forEach { setBit($0, inNumber: &number) }

		// part1: mask value of 0: force bit to zero
		// part2: mask value of 0: ignore zero
		if !ignoringZero {
			mask.bits0.forEach { clearBit($0, inNumber: &number) }
		}
	}

	func clearBit(_ bit: Int, inNumber n: inout Int) {
		n &= (((1 << 36) - 1) ^ (1 << bit))
	}

	func setBit(_ bit: Int, inNumber n: inout Int) {
		n |= (1 << bit)
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return parseAndRun(input.lines, isPart2: false)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return parseAndRun(input.lines, isPart2: true)
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

