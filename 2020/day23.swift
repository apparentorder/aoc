class Day23: PuzzleClass {
	func play(_ input: PuzzleInput, moves: Int, fillCupsTo: Int? = nil) -> PuzzleResult {
		var startingCups = input.raw.map { Int(String($0))! }
		let maxDebug = startingCups.count

		let totalCups = fillCupsTo ?? startingCups.count
		startingCups.reserveCapacity(totalCups + 1)
		if totalCups > startingCups.count {
			startingCups += Array((startingCups.max()! + 1)...(totalCups))
		}

		var nextCup = Array(repeating: 0, count: totalCups + 2)

		func insertCup(_ newCup: Int, afterCup: Int) {
			let oldNext = nextCup[afterCup]
			nextCup[afterCup] = newCup
			nextCup[newCup] = oldNext
		}

		func cups(startingWith sc: Int, for max: Int? = nil) -> [Int] {
			var r = [sc]
			var i = sc
			while nextCup[i] != sc {
				guard max == nil || r.count < max! else { break }
				i = nextCup[i]
				r += [i]
			}
			return r
		}

		func removeCup(after ac: Int) -> Int {
			let toRemove = nextCup[ac]
			var newNext = nextCup[toRemove]
			nextCup[ac] = newNext
			return toRemove
		}
				
		// place starting cups, with the last element pointing to the first
		for (i, cup) in startingCups.enumerated() {
			nextCup[cup] = startingCups[(i + 1) % startingCups.count]
		}

		var currentCup = startingCups[0]

		for move in 1...moves {
			debug("-- move \(move) --")
			debug("cups: \(cups(startingWith: currentCup, for: maxDebug))")
			debug("current: \(currentCup)")

			let pickUp = (0..<3).map { _ in removeCup(after: currentCup) }
			debug("pick up: \(pickUp)")

			var destination = currentCup - 1
			while pickUp.contains(destination) || destination < 1 {
				destination -= 1
				if destination < 1 {
					destination = totalCups
				}
			}
			debug("destination: \(destination)")

			pickUp.reversed().forEach { insertCup($0, afterCup: destination) }

			currentCup = nextCup[currentCup]
		}

		if totalCups > 100 {
			let starCups = cups(startingWith: 1, for: 3)
			debug("final: \(starCups)")
			return starCups.dropFirst().reduce(1, *)
		} else {
			let final = cups(startingWith: 1)
			debug("final: \(cups(startingWith: 1))")
			return final.dropFirst().reduce("", { $0 + String($1) })
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return play(input, moves: 100)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return play(input, moves: 10_000_000, fillCupsTo: 1_000_000)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromString: "418976235"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "389125467"), result: 67384529),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromString: "418976235"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "389125467"), result: 149245887792),
			]
		),
	]

	required init() {}
}

