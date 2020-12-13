class Day13: PuzzleClass {
	func part1(_ input: PuzzleInput) -> PuzzleResult {
		var tokens = input.tokens
		let time = Int(tokens.removeFirst())!
		let busIds = tokens.compactMap { Int($0) }

		var minWait = Int.max
		var minWaitBusId = 0

		for busId in busIds {
			let wait = busId - (time % busId)
			debug("busId \(busId) wait time \(wait)")

			if wait < minWait {
				minWait = wait
				minWaitBusId = busId
			}
		}

		return minWait * minWaitBusId
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		var tokens = input.tokens
		tokens.removeFirst() // discard the first item ('time' in part1)

		let busIdsByIndex = tokens
			.enumerated()
			.filter { $0.1 != "x" }
			.map { (index: $0.0, busId: Int($0.1)!) }
			.sorted { $0.busId > $1.busId }

		var step = busIdsByIndex.map({ $0.busId }).max()!

		var time = 0
		checkNextTime: while true {
			time += step

			step = 1
			for (index, busId) in busIdsByIndex {
				guard (time + index) % busId == 0 else { continue checkNextTime }
				debug("time = \(time) valid busId \(busId) for t=\(time + index)")
				step = max(step, step * busId)
			}
			debug("match at time \(time)")
			break
		}

		return time
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "13-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: ("939 7,13,x,x,59,x,31,19")), result: 295),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "13-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: ("foo 7,13,x,x,59,x,31,19")), result: 1068781),
				PuzzleTest(PuzzleInput(fromString: ("foo 17,x,13,19")), result: 3417),
				PuzzleTest(PuzzleInput(fromString: ("foo 67,7,59,61")), result: 754018),
				PuzzleTest(PuzzleInput(fromString: ("foo 67,x,7,59,61")), result: 779210),
				PuzzleTest(PuzzleInput(fromString: ("foo 67,7,x,59,61")), result: 1261476),
				PuzzleTest(PuzzleInput(fromString: ("foo 1789,37,47,1889")), result: 1202161486),
			]
		),
	]

	required init() {}
}

