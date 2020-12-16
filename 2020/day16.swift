class Day16: PuzzleClass {
	var rules = [String:(min1: Int, max1: Int, min2: Int, max2: Int)]()
	var fieldIds = [String:Int]()
	var myTicket = [Int]()
	var otherTickets = [[Int]]()

	func parseTickets(_ inputLines: [String]) {
		var lines = inputLines
		while true {
			let line = lines.removeFirst()
			guard !line.isEmpty else { break }

			let lineComp = line.components(separatedBy: ": ")
			let rangeComp = lineComp[1].components(separatedBy: " or ")
			let rangeComp1 = rangeComp[0].components(separatedBy: "-")
			let rangeComp2 = rangeComp[1].components(separatedBy: "-")

			debug("\(line) l=\(lineComp), r=\(rangeComp1) r2=\(rangeComp2)")
			rules[lineComp[0]] =  (Int(rangeComp1[0])!, Int(rangeComp1[1])!, Int(rangeComp2[0])!, Int(rangeComp2[1])!)
		}

		debug("done; \(rules)")

		lines.removeFirst()
		myTicket = lines.removeFirst().components(separatedBy: ",").map { Int($0)! }

		lines.removeFirst(2)
		for line in lines {
			debug("OT: \(line)")
			otherTickets += [line.components(separatedBy: ",").map { Int($0)! }]
		}

		debug("my: \(myTicket)")
		debug("others: \(otherTickets)")
	}

	func invalidNumbersInTicket(_ ticket: [Int]) -> [Int] {
		var r = [Int]()

		for number in ticket {
			var isValid = false
			for (_, rule) in rules {
				if (number >= rule.min1 && number <= rule.max1) || (number >= rule.min2 && number <= rule.max2) {
					isValid = true
					break
				}
			}

			if !isValid {
				debug("ticket \(ticket) number \(number) is not valid")
				r += [number]
			}
		}

		return r
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		parseTickets(input.lines)
		var r = 0

		for ticket in otherTickets {
			let invalidNumbers = invalidNumbersInTicket(ticket)
			invalidNumbers.forEach { r += $0 }
		}

		return r
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		parseTickets(input.lines)

		otherTickets.removeAll { !invalidNumbersInTicket($0).isEmpty }
		otherTickets += [myTicket]

		var remainingRules = rules
		var remainingFieldIds = Array(0..<otherTickets[0].count)
		while true {
			guard !remainingFieldIds.isEmpty else { break }
			for fieldId in remainingFieldIds {
				var validRulesForField = remainingRules

				for ticket in otherTickets {
					for (ruleName, rule) in validRulesForField {
						let n = ticket[fieldId]
						if !((n >= rule.min1 && n <= rule.max1) || (n >= rule.min2 && n <= rule.max2)) {
							validRulesForField[ruleName] = nil
						}
					}
				}

				guard validRulesForField.count == 1 else {
					debug("multiple rules match for field \(fieldId): \(validRulesForField)")
					continue
				}

				debug("MATCH: field \(fieldId) is \(validRulesForField.keys.first!)")
				fieldIds[validRulesForField.keys.first!] = fieldId
				remainingFieldIds.removeAll { $0 == fieldId }
				remainingRules[validRulesForField.keys.first!] = nil
			}
		}

		return fieldIds
			.filter { $0.0.hasPrefix("departure") }
			.map { myTicket[$0.1] }
			.reduce(1, *)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "16-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "16-input-test"), result: 71),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "16-input"),
			tests: [
				// nb fixed test data to include departure rules
				PuzzleTest(PuzzleInput(fromFile: "16-input-test-part2"), result: 132),
			]
		),
	]

	required init() {}
}

