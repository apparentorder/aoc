class Day08: PuzzleClass {
	enum InstructionOperation: String {
		case nop = "nop"
		case acc = "acc"
		case jmp = "jmp"
	}

	struct Instruction: CustomStringConvertible {
		var operation: InstructionOperation
		var argument: Int
		var description: String { "\(operation) \(argument)" }
	}

	struct ExecutionState: CustomStringConvertible {
		var acc = 0 // accumulator
		var ptr = 0 // instruction pointer
		var instructionsSeen = [Int:Bool]()
		var description: String { "(ptr=\(ptr) acc=\(acc))" }
	}

	func runProgram(_ instructions: [Instruction], isPart2: Bool) -> Int? {
		var state = ExecutionState()

		while true {
			if state.ptr == instructions.count {
				// ptr is one entry beyond our instructions: win!
				return isPart2 ? state.acc : nil
			}

			guard state.ptr >= 0 && state.ptr < instructions.count else {
				debug("ptr out of bounds")
				return nil
			}

			guard state.instructionsSeen[state.ptr] == nil else {
				debug("loop!")
				return isPart2 ? nil : state.acc
			}

			debug("exec", instructions[state.ptr], "@", state)

			state.instructionsSeen[state.ptr] = true
			switch instructions[state.ptr].operation {
			case .nop:
				break
			case .acc:
				state.acc += instructions[state.ptr].argument
			case .jmp:
				state.ptr += instructions[state.ptr].argument
				continue // avoid ptr increment
			}

			state.ptr += 1
		}
	}

	func parseInstruction(_ s: String) -> Instruction {
		let c = s.components(separatedBy: " ")
		return Instruction(
			operation: InstructionOperation(rawValue: c[0])!,
			argument: Int(c[1])!
		)
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let instructions = input.lines.map { parseInstruction($0) }
		return runProgram(instructions, isPart2: false)!
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let instructions = input.lines.map { parseInstruction($0) }

		// yes, trying brute force.
		for i in 0..<instructions.count where instructions[i].operation != .acc {
			var tryInstructions = instructions

			// try flipping
			tryInstructions[i].operation = (tryInstructions[i].operation == .jmp) ? .nop : .jmp

			debug("Trying program", tryInstructions)
			if let result = runProgram(tryInstructions, isPart2: true) {
				debug("part2 match, instruction", i, "of", instructions.count, ":", tryInstructions[i])
				return result
			}
			debug()
		}

		err("brute force ended, no result?")
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "08-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "08-input-test"), result: 5),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "08-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "08-input-test"), result: 8),
			]
		),
	]

	required init() {}
}

