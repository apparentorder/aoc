class Day23: PuzzleClass {
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

	func run(_ initialProgram: [String]) {
		var instructionPointer = 0
		var instructionCounter = 0
		var program = initialProgram

		func tryOptimizedJump(by jumpBy: Int, to jumpDest: Int, testing jumpTestRegister: String) -> Bool {
			let increaseRegister: String
			let increaseBy: Int

			switch jumpBy {
			case -2: // generic inc/dec loop optimization, works for any pair of registers
				let prev2 = program[instructionPointer - 2]
				let prev1 = program[instructionPointer - 1]
				let decreaseRegister: String

				if prev1.hasPrefix("inc") && prev2.hasPrefix("dec") {
					increaseRegister = String(prev1.last!)
					decreaseRegister = String(prev2.last!)
				} else if prev1.hasPrefix("dec") && prev2.hasPrefix("inc") {
					decreaseRegister = String(prev1.last!)
					increaseRegister = String(prev2.last!)
				} else {
					return false
				}

				guard decreaseRegister == jumpTestRegister else { return false }

				increaseBy = registers[decreaseRegister]!

				registers[decreaseRegister] = 0

			case -5:
				// special case: the most problematic double loop, exactly as observed in the puzzle output.
				// there is another double loop starting with "cpy 90 d", but it doesn't have any meaningful
				// impact on run time.
				guard program[instructionPointer - 5] == "cpy b c" else { return false }
				guard program[instructionPointer - 4] == "inc a" else { return false }
				guard program[instructionPointer - 3] == "dec c" else { return false }
				guard program[instructionPointer - 2] == "jnz c -2" else { return false }
				guard program[instructionPointer - 1] == "dec d" else { return false }

				increaseRegister = "a"
				increaseBy = registers["b"]! * registers["d"]!

				// n.b. register 'b' is not modified by the loop
				registers["c"] = 0
				registers["d"] = 0

			default:
				return false
			}

			debug("optimizing \(abs(jumpBy))-step loop: increasing register \(increaseRegister) by \(increaseBy)")

			registers[increaseRegister]! += increaseBy

			return true
		}

		while instructionPointer < program.count {
			instructionCounter += 1

			if false {
				debug("-----")
				debug("registers before: \(registers.sorted(by: { $1.key > $0.key }))")
				debug("instruction #\(instructionCounter)@\(instructionPointer): \(program[instructionPointer])")
			}

			var args = program[instructionPointer].components(separatedBy: " ")
			let instruction = args.removeFirst()

			switch instruction {
			case "cpy":
				// If toggling produces an invalid instruction (like cpy 1 2) [...] skip it
				if registers.keys.contains(args[1]) {
					registers[args[1]] = regOrValue(args[0])
				}

				instructionPointer += 1

			case "inc":
				registers[args[0]]! += 1
				instructionPointer += 1

			case "dec":
				registers[args[0]]! -= 1
				instructionPointer += 1

			case "tgl":
				let targetOffset = regOrValue(args[0])
				guard 0..<(program.count) ~= (instructionPointer + targetOffset) else {
					debug("toggle for invalid targetOffset \(targetOffset) -- skipping")
					instructionPointer += 1
					break
				}
				let targetInstruction = program[instructionPointer + targetOffset]

				var newInstruction = ""
				switch targetInstruction.prefix(3) {
					case "inc": newInstruction = "dec"
					case "dec": newInstruction = "inc"
					case "jnz": newInstruction = "cpy"
					case "cpy": newInstruction = "jnz"
					case "tgl": newInstruction = "inc"
					default: err("invalid target instruction in toggle")
				}

				// re-attach argument(s)
				newInstruction += targetInstruction.dropFirst(3)

				program[instructionPointer + targetOffset] = newInstruction
				debug("toggle: old=[\(targetInstruction)] new=[\(newInstruction)]")

				debug("program is now:")
				debug(program)

				instructionPointer += 1

			case "jnz":
				let jumpTestRegister = args[0]
				let jumpBy = regOrValue(args[1])
				let jumpDest = instructionPointer + jumpBy

				guard regOrValue(jumpTestRegister) != 0 else {
					// reg is zero, continue normally
					instructionPointer += 1
					break
				}

				guard jumpBy < 0 else {
					// not jumping backwards, so nothing we might optimize,
					// therefore jump to destination normally
					instructionPointer = jumpDest
					break
				}

				if tryOptimizedJump(by: jumpBy, to: jumpDest, testing: jumpTestRegister) {
					// loop optimized away -- continue normally as if the destination was zero
					instructionPointer += 1
				} else {
					// cannot optimize, so jump as per program's instruction
					instructionPointer = jumpDest
				}

			default:
				err("unknown instruction: \(program[instructionPointer])")
			}
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		// "The rest of the electronics seem to place the keypad entry (the number of eggs, 7)
		// in register a, run the code, and then send the value left in register a to the safe.
		registers["a"] = 7

		run(input.lines)
		return registers["a"]!
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		registers["a"] = 12
		run(input.lines)
		return registers["a"]!
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "23-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "23-input-test"), result: 3),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "23-input"),
			tests: []
		),
	]

	required init() {}

}

