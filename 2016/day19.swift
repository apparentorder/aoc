class Day19: PuzzleClass {
	struct CircleElf {
		var previousElfNumber: Int
		var nextElfNumber: Int
	}

	func elephantWinnerP1(of elfCount: Int) -> Int {
		var left = 1
		var n = 0

		var previousCountIsOdd = (elfCount % 2 == 1)
		var seats = elfCount

		while seats > 1 {
			n += 1

			seats = elfCount / (1<<n)

			debug("at n=\(n) step=\(1<<n) left=\(left) seats=\(seats)")

			if previousCountIsOdd {
				// move left end
				left += (1<<n)
			}

			debug("after n=\(n) step=\(1<<n) left=\(left)")

			previousCountIsOdd = (seats % 2 == 1)
		}

		return left
	}

	func elephantWinnerP2(of elfCount: Int, stealFromAcross: Bool = false) -> Int {
		var circle = elfCircle(elfCount)
		//debug(circle)

		var currentElf = 1
		var acrossElf = 1 + elfCount/2
		while circle.count > 1 {
			debug("current elf: \(currentElf), across \(acrossElf)")

			// find victim (next for p1; across for p2)
			let victimElfNumber = stealFromAcross ? acrossElf : circle[currentElf]!.nextElfNumber
			debug("stealing from: \(victimElfNumber)")

			acrossElf = circle[victimElfNumber]!.nextElfNumber

			// fixup the victim's neighbors' pointers
			let victimPreviousElfNumber = circle[victimElfNumber]!.previousElfNumber
			let newNextElfNumber = circle[victimElfNumber]!.nextElfNumber
			circle[victimPreviousElfNumber]!.nextElfNumber = newNextElfNumber
			circle[newNextElfNumber]!.previousElfNumber = victimPreviousElfNumber
			circle.removeValue(forKey: victimElfNumber)

			// next player is always to the left
			let nextPlayerNumber = circle[currentElf]!.nextElfNumber
			debug("next player: \(nextPlayerNumber)")
			currentElf = nextPlayerNumber

			// the across player *may* move to the left a second time, if the
			// circle previously had an uneven amount of seats
			if stealFromAcross, circle.count % 2 == 0 {
				acrossElf = circle[acrossElf]!.nextElfNumber
			}

			debug("")
		}

		return circle.keys.first!
	}

	func elfCircle(_ count: Int) -> [Int:CircleElf] {
		var r = [Int:CircleElf]()
		r.reserveCapacity(count)

		for elfNumber in 1...count {
			r[elfNumber] = CircleElf(previousElfNumber: elfNumber - 1, nextElfNumber: elfNumber + 1)
		}

		r[1]!.previousElfNumber = count
		r[count]!.nextElfNumber = 1

		return r
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return elephantWinnerP1(of: Int(input.raw)!)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return elephantWinnerP2(of: Int(input.raw)!, stealFromAcross: true)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromString: "3017957"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "5"), result: 3),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromString: "3017957"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "5"), result: 2),
			]
		),
	]

	required init() {}

}

