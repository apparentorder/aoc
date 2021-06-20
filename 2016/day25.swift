class Day25: PuzzleClass {
	var registers = [String:Int]()

	// annotated input code:
	//
	// setup part:
	// cpy a d
	// cpy 14 c
	// o cpy 182 b
	// | o inc d
	// | | dec b
	// | ` jnz b -2
	// | dec c
	// ` jnz c -5
	// ... basically this is just "input value + 182*14"
	// 
	// o cpy d a <-- "while true" starts here. we can ignore that since we want a single sequence only.
	// | o jnz 0 0
	// | | cpy a b
	// | | cpy 0 a
	// | | o cpy 2 c
	// | | | o jnz b 2
	// | | | | jnz 1 6
	// | | | | dec b
	// | | | | dec c
	// | | | ` jnz c -4
	// | | | inc a
	// | | ` jnz 1 -7
	// | | cpy 2 b
	// | | o jnz c 2
	// | | | jnz 1 4
	// | | | dec b
	// | | | dec c
	// | | ` jnz 1 -4
	// | | jnz 0 0
	// | | out b
	// | ` jnz a -19
	// ` jnz 1 -21
	//
	// the literal translation of this is shown in run_orig() for reference; what this actually does
	// is easier to observe in run(). the output signal is simply the (increased) input value in binary --
	// so an input of 182 gives a starting value of 182 + 182*14 = 2,730, which is [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
	// in binary.
	//

	func run() -> [Int] {
		var output = [Int]()

		registers["a"]! += 182 * 14

		while regOrValue("a") != 0 {
			registers["b"] = regOrValue("a")
			registers["a"] = regOrValue("b") / 2
			registers["c"] = regOrValue("b") % 2

			output += [registers["c"]! % 2] // "out b"
		}

		return output
	}

	func run_orig() -> [Int] {
		var output = [Int]()

		registers["d"] = regOrValue("a")
		registers["c"] = 14

		registers["d"]! += 182 * 14
		registers["b"] = 0
		registers["c"] = 0

		registers["a"] = regOrValue("d")

		repeat {
			registers["b"] = regOrValue("a")
			registers["a"] = 0

			outer: while true {
				registers["c"] = 2

				repeat {
					if regOrValue("b") == 0 {
						break outer
					}

					registers["b"]! -= 1
					registers["c"]! -= 1
				} while regOrValue("c") != 0

				registers["a"]! += 1
			}

			registers["b"] = 2

			while regOrValue("c") != 0 {
				registers["b"]! -= 1
				registers["c"]! -= 1
			}

			output += [registers["b"]!]
		} while regOrValue("a") != 0

		return output
	}

	func regOrValue(_ s: String) -> Int {
		if let i = Int(s) {
			return i
		}

		return registers[s]!
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		_ = input // ignore

		outer: for i in 0...Int.max {
			debug("Trying register A = \(i)...")
			registers = ["a": i, "b": 0, "c": 0, "d": 0]

			let output = run()
			debug("... \(output)")

			guard output[0] == 0 else {
				// expected clock signal has to start with 0
				continue
			}

			for i in 1..<output.count {
				guard output[i] != output[i - 1] else {
					// not an alternating signal
					continue outer
				}
			}

			return i
		}

		err("TILT")
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return "happy new year!"
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "25-input"),
			tests: []
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "25-input"),
			tests: []
		),
	]

	required init() {}

}

