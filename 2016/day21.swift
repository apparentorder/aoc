class Day21: PuzzleClass {
	//
	// assumption: no letter appears twice.
	//

	struct Password: CustomStringConvertible {
		var password: [Character]
		var description: String { String(password) }

		func letterIndex(_ c: Character) -> Int {
			return self.password.firstIndex(of: c)!
		}

		func letterIndex(_ s: String) -> Int {
			return letterIndex(Character(s))
		}

		mutating func swap(_ posX: Int, _ posY: Int) {
			let swapLetter = password[posY]
			password[posY] = password[posX]
			password[posX] = swapLetter
		}

		mutating func rotate(by count: Int, to direction: String) {
			var new = password

			let offset: Int
			if direction == "left" {
				offset = count
			} else /* right */ {
				offset = password.count - (count % password.count)
			}

			for i in 0..<password.count {
				new[i] = password[(i + offset) % password.count]
			}

			password = new
		}

		func rotationsForLetter(_ s: String) -> Int {
			return self.rotationsForLetter(Character(s))
		}

		func rotationsForLetter(_ c: Character) -> Int {
			// "[rotate] one time, plus a number of times equal to that index"
			// "[rotate] one additional time if the index was at least 4"
			let i = self.letterIndex(c)
			return 1 + i + (i >= 4 ? 1 : 0)
		}

		mutating func reverse(from posX: Int, to posY: Int) {
			var new = password

			for i in 0..<password.count {
				new[i] = password[i]
				if posX...posY ~= i {
					new[i] = password[posY - (i - posX)]
				} else {
					new[i] = password[i]
				}
			}

			password = new
		}

		mutating func move(from posX: Int, to posY: Int) {
			let c = password.remove(at: posX)
			password.insert(c, at: posY)
		}

		init(_ s: String) {
			self.password = Array(s)
		}
	}

	func scramble(_ startingWith: String, instructions: [String], reverse: Bool = false) -> String {
		var password = Password(startingWith)

		debug("password: \(password)")

		for instruction in (reverse ? instructions.reversed() : instructions) {
			let parts = instruction.components(separatedBy: " ")

			switch parts[0] {
			case "swap":
				let x: Int
				let y: Int
				if parts[1] == "letter" {
					x = password.letterIndex(parts[2])
					y = password.letterIndex(parts[5])
				} else {
					x = Int(parts[2])!
					y = Int(parts[5])!
				}

				password.swap(x, y)

			case "rotate":
				let direction: String
				let count: Int

				if parts[1] != "based" {
					count = Int(parts[2])!

					if reverse {
						direction = (parts[1] == "left") ? "right" : "left"
					} else {
						direction = parts[1]
					}
				} else /* based on position of letter X */ {
					if !reverse {
						count = password.rotationsForLetter(parts[6])
						direction = "right"
					} else {
						// brute force: rotate left, then see if we could rotate based
						// on the given letter and end up with the current password
						var r: Int? = nil
						for tryRotations in (1...(password.password.count + 1)).reversed() {
							var tryPassword = password

							tryPassword.rotate(by: tryRotations, to: "left")

							guard tryPassword.rotationsForLetter(parts[6]) == tryRotations else {
								continue
							}

							guard r == nil else {
								// n.b.: multiple valid inputs are possible,
								// but in my case only showed up in the test data,
								// NOT using the real puzzle input. *shrug*
								// also note that reversing the part 1 test data
								// was my idea and not recommended by the puzzle
								// input, so it might be that the actual input was
								// actually designed to avoid this issue. still meh.
								debug(
									"NOTE: multiple reverse rotations "
									+ "of password \(password) for letter "
									+ "\(parts[6]); using the highest "
									+ "rotation count"
								)
								continue
							}

							r = tryRotations
						}

						count = r!
						direction = "left"
					}
				}

				password.rotate(by: count, to: direction)

			case "reverse":
				password.reverse(from: Int(parts[2])!, to: Int(parts[4])!)

			case "move":
				let x = Int(parts[2])!
				let y = Int(parts[5])!

				if reverse {
					password.move(from: y, to: x)
				} else {
					password.move(from: x, to: y)
				}

			default:
				err("invalid instruction: \(instruction)")
			}

			debug("after instruction '\(instruction)': \(password)")
		}

		return password.description
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let passwordString = (input.lines.count < 20) ? /* test mode */ "abcde" : /* actual */ "abcdefgh"
		return scramble(passwordString, instructions: input.lines)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let passwordString = (input.lines.count < 20) ? /* test mode */ "decab" : /* actual */ "fbgdceah"
		return scramble(passwordString, instructions: input.lines, reverse: true)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "21-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "21-input-test"), result: "decab"),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "21-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "21-input-test"), result: "abcde")
			]
		),
	]

	required init() {}

}

