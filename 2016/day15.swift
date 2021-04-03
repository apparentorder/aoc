class Day15: PuzzleClass {
	typealias Disc = (currentPosition: Int, totalPositions: Int)

	struct SculptureState: CustomStringConvertible {
		var time: Int
		var capsulePosition: Int
		var discs = [Disc]()

		var capsuleRetrieved: Bool { capsulePosition >= discs.count }

		var description: String {
			var s = ""
			s += "time \(time)\n"
			for (i, disc) in discs.enumerated() {
				s += "disc #\(i) at position \(disc.currentPosition)/\(disc.totalPositions)"
				if i == capsulePosition {
					s += " <-- capsule"
				}
				s += "\n"
			}

			return s
		}

		mutating func forward(by seconds: Int) {
			time += seconds

			for (i, disc) in discs.enumerated() {
				discs[i].currentPosition = (disc.currentPosition + seconds) % disc.totalPositions
			}
		}

		mutating func tryTickWithCapsule() -> Bool {
			self.forward(by: 1)
			capsulePosition += 1

			return (capsuleRetrieved || discs[capsulePosition].currentPosition == 0)
		}
	}

	func parse(_ lines: [String]) -> SculptureState {
		var discs = [Disc]()

		for line in lines {
			let comp = line.components(separatedBy: " ")
			let discTotalPositions = Int(comp[3])!
			let discCurrentPosition = Int(comp[11].dropLast())! // drop "."

			// n.b. we don't track the identifier (Disc #) but assume that the discs in the input
			// are sorted, and therefore get disc[n] = "Disc #n+1" (counting from zero).
			guard Int(comp[1].dropFirst() /* drop "#" */)! == discs.count + 1 else {
				err("disc ids in input are not sorted")
			}

			discs += [Disc(currentPosition: discCurrentPosition, totalPositions: discTotalPositions)]
		}
		return SculptureState(
			time: 0,
			capsulePosition: -1, // it takes one tick to reach the first disc
			discs: discs
		)
	}

	func findButtonTime(state startingState: SculptureState) -> Int {
		// buttonTime has to be a multiple of all discs' totalPositions.
		// this could be calculated for all discs (least common multiple). but since
		// even a trivial brute force completes in <1sec (or ~12sec with debug), and the
		// naïve approach had already been coded anyway, we'll optimize for the first disc
		// only (completing in ~80ms, or ~1s with debug).

		let firstDisc = startingState.discs[0]
		var buttonTime = firstDisc.totalPositions - firstDisc.currentPosition - 1
		let buttonIncrement = firstDisc.totalPositions

		while true {
			debug("--------------------------------")
			debug("trying button at time = \(buttonTime)")
			var state = startingState
			state.forward(by: buttonTime)

			while true {
				let canContinue = state.tryTickWithCapsule()
				debug(state)

				guard canContinue else {
					// reached invalid configuration (capsule bounced) for this buttonTime
					debug("FAILED: invalid state reached")
					break
				}

				guard !state.capsuleRetrieved else {
					debug("SUCCESS! Capsule retrieved!")
					return buttonTime
				}
			}

			buttonTime += buttonIncrement
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return findButtonTime(state: parse(input.lines))
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		var state = parse(input.lines)
		state.discs += [Disc(currentPosition: 0, totalPositions: 11)]
		return findButtonTime(state: state)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "15-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "15-input-test"), result: 5),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "15-input"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "15-test1"), result: 241861950),
			]
		),
	]

	required init() {}

}

