// The Rudolf Engine, named for the booze-nosed reindeer that's powering our party sleigh.

class RudolfEngine {
	var program = [Instruction]()
	var execState = ExecutionState()
	var programState: ProgramState
	var breakpoint: Breakpoint? = nil
	var error: Error? = nil

	var acc: Int { execState.acc }
	var errorString: String { error == nil ? "(none)" : error!.rawValue }

        enum Instruction {
                case nop(Int)
                case acc(Int)
                case jmp(Int)

		init(_ s: String) {
			let c = s.components(separatedBy: " ")
			let op = c[0]

			switch op {
			case "nop": self = .nop(Int(c[1])!)
			case "acc": self = .acc(Int(c[1])!)
			case "jmp": self = .jmp(Int(c[1])!)
			default: err("invalid operation: \(s)")
			}
		}

		func exec(_ state: inout ExecutionState) {
			switch self {
			case .nop:
				break
			case let .acc(i):
				state.acc += i
			case let .jmp(i):
				state.ptr += i
				return // don't implicitly increment ptr
			}

			state.ptr += 1
		}

		var isJmpOrNop: Bool {
			// helper for d08 p2
			if case .nop(_) = self { return true }
			if case .jmp(_) = self { return true }
			return false
		}
	}

	enum Error: String {
		case invalidState = "invalid state"
		case outOfBounds = "out of bounds"
		case outOfBoundsAfterLastInstruction = "out of bounds; exactly after last instruction"
	}

	enum ProgramState {
		case initialized
		case running
		case stopped
		case failed
	}

        struct ExecutionState: CustomStringConvertible {
                var acc = 0 // accumulator
                var ptr = 0 // instruction pointer
		var instructionsUsed: Set<Int> = []
                var description: String { "(ptr=\(ptr) acc=\(acc))" }
        }

	enum Breakpoint {
		case loopDetected // d08 p1
	}

        func run() {
		guard programState != .failed else {
			error = .invalidState
			return
		}

		programState = .running

                while true {
                        guard execState.ptr >= 0 && execState.ptr < program.count else {
				// special case: exactly one instruction after the
				// end is a required check for d08 p2
				if execState.ptr == program.count {
					programState = .failed
					error = .outOfBoundsAfterLastInstruction
					return
				}

                                programState = .failed
				error = .outOfBounds
				return
                        }

			if let b = breakpoint, b == .loopDetected {
				guard !execState.instructionsUsed.contains(execState.ptr) else {
					programState = .stopped
					return
				}

				execState.instructionsUsed.insert(execState.ptr)
			}

                        debug("exec \(program[execState.ptr]) @ \(execState)")
			program[execState.ptr].exec(&execState)
                }
        }

	func flipJmpNop(atIndex i: Int) {
		switch program[i] {
		case let .nop(v): program[i] = .jmp(v)
		case let .jmp(v): program[i] = .nop(v)
		default: err("flipJmpNop() for unrelated instruction \(program[i])")
		}
	}

	init(fromStrings lines: [String]) {
		program = lines.map { Instruction($0) }
		programState = .initialized
	}

	init(cloneFrom original: RudolfEngine) {
		program = original.program
		breakpoint = original.breakpoint
		programState = .initialized
	}
}

