class Day22: PuzzleClass {
	func parse(_ input: PuzzleInput) -> [[Int]] {
		var playerCards = [[Int]]()

		var player = 0
		playerCards += [[Int]()]

		for line in input.lines {
			guard !line.hasPrefix("Player 2") else {
				playerCards += [[Int]()]
				player += 1
				continue
			}

			guard let i = Int(line) else { continue }
			playerCards[player] += [i]
		}

		return playerCards
	}

	func playR(playerCards pc: [[Int]], depth: Int = 0) -> Int {
		var playerCards = pc
		var deckHistory = [[[Int]]]() // deckHistory[player][round] = [cards]
		deckHistory += [[[Int]]()] // player0
		deckHistory += [[[Int]]()] // player1
		var round = 0

		debug("NEW GAME:", indent: depth*4)
		debug("p1 deck: \(playerCards[0])", indent: depth*4)
		debug("p2 deck: \(playerCards[1])", indent: depth*4)

		while !playerCards[0].isEmpty && !playerCards[1].isEmpty {
			round += 1

			// Before either player deals a card, if there was a previous round in this
			// game that had exactly the same cards in the same order in the same
			// players' decks, the game instantly ends in a win for player 1.
			var looped = [false, false]
			//debug("deck history: \(deckHistory)")
			for dhPlayer in [0, 1] {
				for dhRound in deckHistory[dhPlayer] {
					if dhRound == playerCards[dhPlayer] {
						looped[dhPlayer] = true
						debug("LOOP for player \(dhPlayer): \(playerCards[dhPlayer])", indent: depth*4)
					}
				}
			}

			guard !looped[0] && !looped[1] else {
				debug("LOOP for BOTH players! Player[0] wins!", indent: depth*4)
				return 0
			}

			deckHistory[0] += [playerCards[0]]
			deckHistory[1] += [playerCards[1]]

			let drawnCards = [playerCards[0].removeFirst(), playerCards[1].removeFirst()]
			var winner: Int

			// If both players have at least as many cards remaining in their deck as
			// the value of the card they just drew, the winner of the round is
			// determined by playing a new game of Recursive Combat
			if playerCards[0].count >= drawnCards[0] && playerCards[1].count >= drawnCards[1] {
				var recursivePlayerCards = playerCards
				recursivePlayerCards[0].removeLast(recursivePlayerCards[0].count - drawnCards[0])
				recursivePlayerCards[1].removeLast(recursivePlayerCards[1].count - drawnCards[1])
				winner = playR(playerCards: recursivePlayerCards, depth: depth + 1)
			} else {
				winner = (drawnCards[0] > drawnCards[1]) ? 0 : 1
			}

			if winner == 0 {
				playerCards[0] += [drawnCards[0], drawnCards[1]]
			} else {
				playerCards[1] += [drawnCards[1], drawnCards[0]]
			}

			debug("p1 deck after round \(round): \(playerCards[0])", indent: depth*4)
			debug("p2 deck after round \(round): \(playerCards[1])", indent: depth*4)
			debug("")
		}

		debug("p1 deck after game: \(playerCards[0])", indent: depth*4)
		debug("p2 deck after game: \(playerCards[1])", indent: depth*4)
		debug("")

		guard depth == 0 else {
			// this is a sub-game, return winning player id
			return playerCards[0].isEmpty ? 1 : 0
		}

		// top-level game, return score
		let winningCards = playerCards[0].isEmpty ? playerCards[1] : playerCards[0]
		var score = 0
		for (i, card) in winningCards.reversed().enumerated() {
			score += card*(i+1)
		}

		return score
	}

	func play(playerCards pc: [[Int]]) -> Int {
		var playerCards = pc

		while !playerCards[0].isEmpty && !playerCards[1].isEmpty {
			let drawnCards = [playerCards[0].removeFirst(), playerCards[1].removeFirst()]

			if drawnCards[0] > drawnCards[1] {
				playerCards[0] += [drawnCards[0], drawnCards[1]]
			} else {
				playerCards[1] += [drawnCards[1], drawnCards[0]]
			}

			debug("p1 deck: \(playerCards[0])")
			debug("p2 deck: \(playerCards[1])")
			debug("")
		}

		debug("p1 deck: \(playerCards[0])")
		debug("p2 deck: \(playerCards[1])")

		let winningCards = playerCards[0].isEmpty ? playerCards[1] : playerCards[0]
		var score = 0
		for (i, card) in winningCards.reversed().enumerated() {
			score += card*(i+1)
		}
		return score
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		var playerCards = parse(input)
		debug("\(playerCards)")
		return play(playerCards: playerCards)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		var playerCards = parse(input)

		// loop detection test
		//playerCards = [[43, 19], [2, 29, 14]]
		//return playR(playerCards: playerCards)

		return playR(playerCards: playerCards)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "22-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "22-input-test"), result: 306),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "22-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "22-input-test"), result: 291),
			]
		),
	]

	required init() {}
}

