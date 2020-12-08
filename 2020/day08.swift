class Day08: PuzzleClass {
	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let handheld = RudolfEngine(fromStrings: input.lines)
		handheld.breakpoint = .loopDetected

		handheld.run()
		guard handheld.programState == .stopped else { err("unexpected state: \(handheld.programState)") }

		return handheld.acc
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let unmodifiedHandheld = RudolfEngine(fromStrings: input.lines)
		unmodifiedHandheld.breakpoint = .loopDetected

		// yes, trying brute force.
		for i in 0..<(unmodifiedHandheld.program.count) where unmodifiedHandheld.program[i].isJmpOrNop {
			let clone = RudolfEngine(cloneFrom: unmodifiedHandheld)
			clone.flipJmpNop(atIndex: i)
			clone.run()

			switch clone.programState {
			case .failed:
				if clone.error == .outOfBoundsAfterLastInstruction {
					debug("part2 match at program[\(i)]")
					return clone.acc
				}

				err("unexpected error from clone handheld: \(clone.errorString)")

			case .stopped:
				// loop detected, try next
				continue

			default:
				err("unexpected state \(clone.programState) after tinkering")
			}
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

