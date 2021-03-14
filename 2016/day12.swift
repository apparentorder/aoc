class Day12: PuzzleClass {
	var registers: [String:Int] = [
		"a": 0,
		"b": 0,
		"c": 0,
		"d": 0,
	]

	func regOrValue(_ s: String) -> Int {
		if let i = Int(s) {
			return i
		}

		return registers[s]!
	}

	func run(_ program: [String]) {
		var instructionPointer = 0
		var instructionCounter = 0

		while instructionPointer < program.count {
			instructionCounter += 1

			if false {
				debug("-----")
				debug("instruction #\(instructionCounter): \(program[instructionPointer])")
				debug("registers: \(registers.sorted(by: { $1.key > $0.key }))")
			}

			var args = program[instructionPointer].components(separatedBy: " ")
			let instruction = args.removeFirst()

			switch instruction {
			case "cpy":
				registers[args[1]] = regOrValue(args[0])
				instructionPointer += 1

			case "inc":
				registers[args[0]]! += 1
				instructionPointer += 1

			case "dec":
				registers[args[0]]! -= 1
				instructionPointer += 1

			case "jnz":
				let jumpTestRegister = args[0]
				let jumpBy = Int(args[1])!
				let jumpDest = instructionPointer + jumpBy

				guard regOrValue(jumpTestRegister) != 0 else {
					// reg is zero, continue normally
					instructionPointer += 1
					break
				}

				guard jumpBy == -2 else {
					// not jumping by -2, so nothing we might optimize,
					// jump to destination normally
					instructionPointer = jumpDest
					break
				}

				// optimize "jnz -2" loops of simple inc/dec instructions
				// which are equivalent to "increate x by y, set y to 0"
				// (in theory, the same could be done for larger loops, but
				// this is enough already)
				// (note that this isn't *strictly* necessary, as otherwise the
				// program runs for about 5 seconds for part1 and a bit over two
				// minutes for part 2.

				var increaseRegister: String? = nil
				var decreaseRegister: String? = nil

				for prev in [program[jumpDest], program[jumpDest + 1]] {
					let prevParts = prev.components(separatedBy: " ")

					if prevParts[0] == "inc" {
						increaseRegister = prevParts[1]
					} else if prevParts[0] == "dec", prevParts[1] == jumpTestRegister {
						decreaseRegister = jumpTestRegister
					}
				}

				guard let inc = increaseRegister, let dec = decreaseRegister else {
					// not exactly the case we could optimize
					// jump to destination normally
					instructionPointer = jumpDest
					break
				}

				debug(
					"optimizing inc/dec/jnz loop: "
					+ "increasing register \(inc) by register \(dec) (\(registers[dec]!))"
				)

				registers[inc]! += registers[dec]!
				registers[dec] = 0

				// .. then continue with next instruction (as if "jnz" had
				// tested against a value of 0)

				instructionPointer += 1

			default:
				err("unknown instruction: \(program[instructionPointer])")
			}
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		run(input.lines)
		return registers["a"]!
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		registers["c"] = 1
		run(input.lines)
		return registers["a"]!
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "12-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "12-input-test"), result: 42),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "12-input"),
			tests: []
		),
	]

	required init() {}

}

