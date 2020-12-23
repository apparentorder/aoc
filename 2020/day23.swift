class Day23: PuzzleClass {
	//
	// we only need a way to map from any Cup Label to it's clockwise neighbor Cup Label.
	// at no point do we need to traverse the entire list in part2.
	//
	// also note that the whole list of cups will be a sequence from 1 to the total
	// amount of cups (with the first few cups in random order, as specified by the
	// input).
	//
	// hence we will use an array `nextCup` as a simple single-linked list to map any
	// Cup Label to its clockwise neighbor.
	//
	// this connection is circular, i.e. the last cup's neighbor will be the first cup.
	//
	func play(_ input: PuzzleInput, moves: Int, fillCupsTo: Int? = nil) -> PuzzleResult {
		// print a sequence of cups
		// mainly for debug output, and for part 1. too slow for part 2.
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

		var startingCups = input.raw.map { Int(String($0))! }
		let totalCups = fillCupsTo ?? startingCups.count
		var nextCup = Array(repeating: 0, count: totalCups + 1)

		// fill our starting array with an integer sequence to match the
		// required number of cups
		if totalCups > startingCups.count {
			startingCups += Array((startingCups.max()! + 1)...(totalCups))
		}

		// place starting cups, with the last cup pointing to the first cup
		for (i, cup) in startingCups.enumerated() {
			nextCup[cup] = startingCups[(i + 1) % startingCups.count]
		}

		var currentCup = startingCups[0]

		for move in 1...moves {
			debug("-- move \(move) --")
			debug("cups: \(cups(startingWith: currentCup, for: 9))")
			debug("current: \(currentCup)")

			// using cups() causes (total run time) *= 5 -- so let's handpick instead.
			//let pickUp = cups(startingWith: nextCup[currentCup], for: 3)
			let pickUp = [
				nextCup[currentCup],
				nextCup[nextCup[currentCup]],
				nextCup[nextCup[nextCup[currentCup]]],
			]

			debug("pick up: \(pickUp)")

			var destination = currentCup - 1
			while pickUp.contains(destination) || destination < 1 {
				destination -= 1
				if destination < 1 {
					destination = totalCups
				}
			}
			debug("destination: \(destination)")

			// attach our three picked up cups to their destination
			nextCup[currentCup] = nextCup[pickUp[2]]
			nextCup[pickUp[2]] = nextCup[destination]
			nextCup[destination] = pickUp[0]

			currentCup = nextCup[currentCup]
		}

		if totalCups >= 10 {
			let starCups = cups(startingWith: 1, for: 3)
			debug("final: \(starCups)")
			return starCups.dropFirst().reduce(1, *)
		} else {
			let final = cups(startingWith: 1)
			debug("final: \(final)")
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

