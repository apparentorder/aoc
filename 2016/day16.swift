import Foundation // log2

class Day16: PuzzleClass {
	//
	// key realizations:
	//
	// the checksum is effectively an XOR, so it can be computed "rolling". no need to
	// match pairs.
	//
	// further, the sequence is always <input>0<input-reversed-mirrored>, therefore the
	// XOR checksum of one such sequence is always 1 (because the input length is odd).
	//
	// the input perpetually repeats itself, alternating between the original input and
	// the flipped input, each time separated by a '0' (or a flipped '0').
	//
	// in effect, we only need to figure out the separating bits, as the perpetually
	// repeating input sequence's checksum never changes.
	//
	// much of this works because the input length is odd and the expected length
	// (bits to be checksummed) is a multiple of the input's length.
	//
	// with some better math insights, this could probably be cut down much further.
	// (i bet there's a formula to tell how many separating '1's there are)
	//
	// this runs in ~3s / ~0.7s and does not require growing memory.
	//

	func valueAtPosition(_ position: Int, forInitialState input: [UInt8]) -> UInt8 {
		let n = (position + 1) / (input.count + 1)
		let mod = (position + 1) % (input.count + 1)

		debug("vap pos \(position) n \(n) mod \(mod)")

		guard mod == 0 else {
			// if position isn't a multiple of the input length, we can simply
			// return the relative position in the input, as it perpetually repeats
			// unmodified (but may need to be flipped and inversed)
			return n % 2 == 0 ? (input[mod - 1]) : (input[input.count - mod] ^ 1)
		}

		let _log = log2(Double(n))
		let intExponent: Int? = (n > 0 && floor(_log) == _log) ? Int(_log) : nil
		debug("vap at mirror start, _log \(_log)")

		// strategy:
		// a) if position is cleanly input.count*2^n, we know the value is 0, as
		//    such a position always marks the middle of the sequence:
		//    <input>0<input-reversed-mirrored>
		// b) otherwise return the inversed "mirror position", e.g. the mirror
		//    position of input.count+1 is (not input.count-1) --
		//    this naturally recurses until a) is true

		if intExponent != nil, n > 0 {
			// we're at a mirror start position
			return 0
		}

		let mirrorStart = (input.count + 1) * Int(pow(2, floor(_log)))
		let mirrorPosition = mirrorStart - (position - mirrorStart) - 2
		debug("mirror for pos \(position): \(mirrorPosition)")

		return valueAtPosition(mirrorPosition, forInitialState: input) ^ 1
	}

	func checksum(state initialState: [UInt8], length: Int) -> [UInt8] {
		var r = [UInt8]()

		// we need to produce a checksum that is the same length as the
		// initial state -- in other words, each bit of the checksum is
		// calculated from bitsPerChecksumBlock of the Dragon Sequence
		let bitsPerChecksumBlock = length / initialState.count

		for checksumBlock in 0..<initialState.count {
			let leftEnd = bitsPerChecksumBlock * checksumBlock
			let rightEnd = (bitsPerChecksumBlock * (checksumBlock + 1)) - 1

			var checksum: UInt8 = 1

			debug("cks for block \(checksumBlock) left \(leftEnd) right \(rightEnd)")

			var pos = leftEnd
			while pos <= rightEnd {
				let n   = pos / (initialState.count + 1)
				let mod = pos % (initialState.count + 1)

				if mod == 0 && (rightEnd - pos > initialState.count) {
					// as the initialState's length is odd, its checksum
					// will alterways flip between 0 and 1 for each block
					checksum ^= UInt8(n % 2) ^ 1
					pos += initialState.count
				} else {
					checksum ^= valueAtPosition(pos, forInitialState: initialState)
					pos += 1
				}
			}

			r += [checksum]
		}

		debug(r)
		return r
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let comp = input.raw.components(separatedBy: " ")
		debug("input: \(input.raw)")

		let initialState = comp[0].map { UInt8(String($0))! }
		let length = Int(comp[1])!

		return checksum(state: initialState, length: length)
			.reduce(into: "") { $0 += String($1) }
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let comp = input.raw.components(separatedBy: " ")
		debug("input: \(input.raw)")

		let initialState = comp[0].map { UInt8(String($0))! }
		let length = Int(comp[1])!

		return checksum(state: initialState, length: length)
			.reduce(into: "") { $0 += String($1) }
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
			tests: [
				PuzzleTest(PuzzleInput(fromString: "10000 320"), result: "01100"),
			]
		),
	]

	required init() {}

}

