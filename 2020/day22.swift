class Day22: PuzzleClass {
	var games = 0
	var rounds = 0

	func play(playerCards pc: [[Int]], recursiveCombat: Bool, depth: Int = 0) -> Int {
		var playerCards = pc
		let players = playerCards.enumerated().map { $0.0 }

		func debugDecks(_ extra: @autoclosure () -> String = "") {
			#if DEBUG
			let s = extra().isEmpty ? "" : " \(extra())"
			players.forEach {
				debug("player \($0) deck\(s): \(playerCards[$0])", indent: depth*4)
			}
			debug("")
			#endif
		}

		debug("NEW GAME:", indent: depth*4)
		debugDecks()

		var round = 0
		var deckHistory = players.map { _ in Set<[Int]>(minimumCapacity: 100) }

		while playerCards.allSatisfy({ !$0.isEmpty }) {
			round += 1
			rounds += 1

			// Before either player deals a card, if there was a previous round in this
			// game that had exactly the same cards in the same order in the same
			// players' decks, the game instantly ends in a win for player 1.
			for player in players {
				guard !deckHistory[player].contains(playerCards[player]) else {
					debug("LOOP for player \(player): \(playerCards[player])", indent: depth*4)
					debug("Player 0 wins!", indent: depth*4)
					return 0
				}
				deckHistory[player].insert(playerCards[player])
			}

			var winner: Int
			let drawnCards = players.map { playerCards[$0].removeFirst() }

			if !recursiveCombat || !players.allSatisfy({ playerCards[$0].count >= drawnCards[$0] }) {
				let winningCard = drawnCards.max()
				winner = players.filter { drawnCards[$0] == winningCard }.first!
			} else {
				// Part 2:
				// If both players have at least as many cards remaining in their deck as
				// the value of the card they just drew, the winner of the round is
				// determined by playing a new game of Recursive Combat
				// ...
				// the quantity of cards copied is equal to the number on the card they
				// drew to trigger the sub-game
				// 🧠
				let subGamePlayerCards = players.map {
					Array(playerCards[$0].dropLast(playerCards[$0].count - drawnCards[$0]))
				}
				winner = play(playerCards: subGamePlayerCards, recursiveCombat: true, depth: depth + 1)
			}

			// XXX this is the only place that's hard-coded to two players.
			// the rules are not clear how this would be handled for >2 players,
			// and simply going round-robin downwards by card value would mean
			// to re-write this function so it returns all drawn cards of a sub-game.
			// therefore, i'll leave it as it is for now.
			if winner == 0 {
				playerCards[0] += [drawnCards[0], drawnCards[1]]
			} else {
				playerCards[1] += [drawnCards[1], drawnCards[0]]
			}

			debugDecks("after round \(round)")
		}

		games += 1
		debugDecks("after game")

		// XXX for >2 players, we assume that only one player still
		// holds any cards (i.e. *all* other players dropped out first)
		// (not yet implemented)

		guard depth == 0 else {
			// this is a sub-game, return winning player id
			return players.filter { !playerCards[$0].isEmpty }.first!
		}

		debug("DONE after games=\(games) rounds=\(rounds)")

		// top-level game, return the score
		return playerCards
			.flatMap { $0 }
			.reversed()
			.enumerated()
			.reduce(0, { $0 + $1.1 * ($1.0 + 1) })
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let playerCards = parse(input)
		return play(playerCards: playerCards, recursiveCombat: false)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let playerCards = parse(input)
		return play(playerCards: playerCards, recursiveCombat: true)
	}

	func parse(_ input: PuzzleInput) -> [[Int]] {
		var playerCards = [[Int]]()

		for line in input.lines {
			guard !line.hasPrefix("Player") else {
				playerCards += [[Int]()]
				continue
			}

			guard let i = Int(line) else { continue }
			playerCards[playerCards.count - 1] += [i]
		}

		return playerCards
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
				PuzzleTest(PuzzleInput(fromFile: "22-input-test-loop"), result: 0),
			]
		),
	]

	required init() {}
}

