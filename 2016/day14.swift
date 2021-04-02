import CryptoKit

//
// seriously disappointed by
// a) the measly performance of md5 here
// b) that there indeed isn't any way to optimize this (according to the solutions thread)
//
// runs ~10min with debug output,
// runs ~2min  with compile optimizations.
//

class Day14: PuzzleClass {
	static let hexAlphabet = Array("0123456789abcdef".unicodeScalars)

	struct Hash: Hashable {
		let index: Int
		let hash: String
		var firstTripletCharacter: Character? = nil
		var quintupletCharacters = Set<Character>()

		static func md5HashString(_ message: String, count: Int = 1) -> String {
			// original p1 implementation was using .map { String(format: "%02x", $0) }
			// faster digest-to-string from
			// https://stackoverflow.com/questions/39075043/how-to-convert-data-to-hex-string-in-swift
			// still pretty slow though.

			let digest = Insecure.MD5.hash(data: message.data(using: .utf8)!)
			return String(digest.reduce(into: "".unicodeScalars) { result, value in
				result.append(hexAlphabet[Int(value / 0x10)])
				result.append(hexAlphabet[Int(value % 0x10)])
			})
		}

		init(_ s: String, index: Int, stretchCount: Int = 0) {
			self.index = index
			var message = "\(s)\(index)"

			for _ in 0..<(stretchCount + 1) {
				message = Hash.md5HashString(message)

			}

			hash = message
			let hashChars = Array(hash)

			for i in 0..<(hashChars.count - 2) {
				guard !(
					(hashChars[i] == hashChars[i+1]) &&
					(hashChars[i] == hashChars[i+2])
				) else {
					firstTripletCharacter = hashChars[i]
					break
				}
			}

			guard firstTripletCharacter != nil else {
				// can't have a match of five if we didn't find a match of three
				return
			}

			for i in 0..<(hash.count - 4) {
				if (
					(hashChars[i] == hashChars[i+1]) &&
					(hashChars[i] == hashChars[i+2]) &&
					(hashChars[i] == hashChars[i+3]) &&
					(hashChars[i] == hashChars[i+4])
				) {
					quintupletCharacters.insert(hashChars[i])
				}
			}
		}
	}

	func generateKeys(salt: String, count generateKeysCount: Int, stretchCount: Int = 0) -> Set<Hash> {
		var keys = Set<Hash>()
		var hashes = [Hash]()

		var index = -1
		while true {
			index += 1

			let hash = Hash(salt, index: index, stretchCount: stretchCount)

			// if a hash doesn't have a three-of-a-kind sequence, we don't
			// even need to add it to the list of previously seen hashes
			guard hash.firstTripletCharacter != nil else { continue }

			//debug("\(salt)\(index) => \(hash)")

			// check previously seen hashes for a triplet that matches
			// any of the quintupletCharacters this hash might have
			for qtChar in hash.quintupletCharacters {
				for prevHash in hashes {
					guard let prevHashTripletChar = prevHash.firstTripletCharacter else { continue }
					guard prevHashTripletChar == qtChar else { continue }
					guard hash.index - prevHash.index <= 1_000 else { continue }

					keys.insert(prevHash)
					print("FOUND KEY: \(prevHash)")

					guard keys.count < generateKeysCount else {
						return keys
					}
				}
			}

			hashes += [hash]

			// potential optimization: clear out seen hashes we won't be needing anymore
			//hashes.removeAll { hash.index - $0.index > 1_000 }
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return generateKeys(salt: input.raw, count: 64).map { $0.index }.max()!
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return generateKeys(salt: input.raw, count: 64, stretchCount: 2016).map { $0.index }.max()!
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromString: "jlmsuwbz"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "abc"), result: 22728),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromString: "jlmsuwbz"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "abc"), result: 22551),
			]
		),
	]

	required init() {}

}

