class Day10: PuzzleClass {
	struct Bot {
		var chips: [Int] = []
		var lowTargetBot: Int? = nil
		var highTargetBot: Int? = nil
	}

	var bots = [Int:Bot]()
	var part1Bot: Int? = nil

	enum PassChipError: Error {
		case targetBotFull
	}

	func createBot(_ n: Int) {
		guard bots[n] == nil else { return }
		bots[n] = Bot()
	}

	func passChip(_ value: Int, toBot: Int, fromBot: Int? = nil) throws {
		guard bots[toBot]!.chips.count < 2 else {
			throw PassChipError.targetBotFull
		}

		if let fb = fromBot {
			// n.b. we don't check if fromBot actually has this.
			bots[fb]!.chips.removeAll { $0 == value }
		}

		bots[toBot]!.chips += [value]

		let fbString = fromBot != nil ? "\(fromBot!)" : "(input bin)"
		debug("passed value \(value) from \(fbString) to \(toBot)")
	}

	func parse(_ input: [String]) {
		for line in input {
			if line.hasPrefix("value") {
				// value 5 goes to bot 2
				let parts = line.components(separatedBy: " ")
				let botId = Int(parts[5])!
				let value = Int(parts[1])!

				createBot(botId)
				try! passChip(value, toBot: botId)
			} else if line.contains("gives low to ") {
				// bot 1 gives low to output 1 and high to bot 0
				// ^0  1 2     3   4  5      6 7   8    9  10  11
				let parts = line.components(separatedBy: " ")
				let botId = Int(parts[1])!

				createBot(botId)

				// non-bot targets are outputs. we cheat and assign those values of 10_000 + output id.
				let ltBot = parts[5].hasPrefix("output") ?
					Int(parts[6])! + 10_000 : 
					Int(parts[6])!

				let htBot = parts[10].hasPrefix("output") ?
					Int(parts[11])! + 10_000 : 
					Int(parts[11])!

				createBot(ltBot)
				createBot(htBot)

				bots[botId]!.lowTargetBot = ltBot
				bots[botId]!.highTargetBot = htBot
			} else {
				err("invalid input: \(line)")
			}
		}

		for (id, bot) in bots.sorted(by: { $0.0 < $1.0 }) {
			debug("\(id) => \(bot)")
		}
	}

	func run(findBotComparing botComparingValues: [Int]) {
		while true {
			let botIdsWithTwoChips = bots.filter { $0.value.chips.count == 2 }.map { $0.key }
			guard !botIdsWithTwoChips.isEmpty else {
				debug("no more bots with two chips, game ends.")
				return
			}

			debug("next round: bots with two chips: \(botIdsWithTwoChips)")

			for fromBot in botIdsWithTwoChips {
				let low = bots[fromBot]!.chips.min()!
				let high = bots[fromBot]!.chips.max()!

				if botComparingValues.contains(low) && botComparingValues.contains(high) {
					debug("bot \(fromBot) has both \(low) and \(high)!")
					part1Bot = fromBot
				}

				if let lowTargetBot = bots[fromBot]!.lowTargetBot {
					try! passChip(low, toBot: lowTargetBot, fromBot: fromBot)
				}

				if let highTargetBot = bots[fromBot]!.highTargetBot {
					try! passChip(high, toBot: highTargetBot, fromBot: fromBot)
				}
			}
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		// from puzzle description:
		// "what is the number of the bot that is responsible for
		//  comparing value-61 microchips with value-17 microchips?"
		var botComparingValues = [61, 17]
		if input.lines.count < 10 {
			// apparently we're a test run
			botComparingValues = [2, 5]
		}

		parse(input.lines)
		run(findBotComparing: botComparingValues)

		guard let solution = part1Bot else { err("game ended but comparing bot was not found") }
		return solution
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		_ = part1(input)

		// phrasing is very weak with this puzzle.
		// by experimentation: every known output contains exactly one value at the end of the game.

		bots.filter { $0.key >= 10_000 }.forEach {
			debug("output \($0.key - 10_000) contains \($0.value.chips)")
		}

		return bots
			.filter { 10_000...10_002 ~= $0.key }
			.map { $0.value.chips[0] }
			.reduce(1, *)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "10-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "10-input-test"), result: 2),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "10-input"),
			tests: []
		),
	]

	required init() {}

}

