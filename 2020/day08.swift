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

	struct ExecutionState {
		var acc = 0 // accumulator
		var ptr = 0 // instruction pointer
		var instructionsSeen = [Int:Bool]()
	}

	func runProgramUntilLoop(_ instructions: [Instruction]) -> Int {
		var state = ExecutionState()

		while true {
			debug("exec: \(instructions[state.ptr])")
			guard state.instructionsSeen[state.ptr] == nil else {
				// we've been here before!
				return state.acc
			}

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

	func tryProgram(_ instructions: [Instruction]) -> Int? {
		var state = ExecutionState()

		while true {
			if state.ptr == instructions.count {
				// ptr is one entry beyond our instructions: win!
				return state.acc
			}

			guard state.ptr >= 0 && state.ptr < instructions.count else {
				// make sure we're not out of bounds
				debug("ptr out of bounds")
				return nil
			}

			guard state.instructionsSeen[state.ptr] == nil else {
				// we've been here before!
				debug("loop!")
				return nil
			}

			debug("exec: \(instructions[state.ptr]) @ \(state)")

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
		return runProgramUntilLoop(instructions)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let instructions = input.lines.map { parseInstruction($0) }

		for i in 0..<instructions.count {
			var tryInstructions = instructions
			guard tryInstructions[i].operation != .acc else { continue }

			// try flipping
			tryInstructions[i].operation = (tryInstructions[i].operation == .jmp) ? .nop : .jmp

			debug("Trying program:\n\(tryInstructions)")
			if let result = tryProgram(tryInstructions) {
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

