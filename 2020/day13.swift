class Day13: PuzzleClass {
	func part1(_ input: PuzzleInput) -> PuzzleResult {
		var tokens = input.tokens
		var min = Int(tokens.removeFirst())!

		for t in tokens {
			guard let i = Int(t) else { continue }
			var time = 0
			while time < min {
				time += i
				guard time <= min else {
					debug("\(i), \(time) - \(min) = \(time - min)")
					break
				}
			}
		}

		return 1
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		var tokens = input.tokens
		tokens.removeFirst()

		var maxid = 0
		var maxpos = 0
		for (i, t) in tokens.enumerated() {
			guard let id = Int(t) else { continue }
			if id > maxid {
				maxid = id
				maxpos = i
			}
		}

		var buses: [Int?] = tokens.map { Int($0) }

		debug("max \(maxid) at index \(maxpos)")
		var t = 0

		var step = maxid
		outer: while true {
			t += step

			var valid = false

			step = 1
			for (i, busidOpt) in buses.enumerated() {
				debug("t = \(t) check busid \(busidOpt) for t=\(t+i-maxpos)")
				guard let busid = busidOpt else { continue }
				guard (t + i - maxpos) % busid == 0 else { continue outer }
				step *= busid
			}
			debug("match at time \(t - maxpos)")
			return t - maxpos
		}

		return t
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "13-input"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "13-input-test"), result: 25),
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

