class Day16: PuzzleClass {
	typealias Constraints = (min1: Int, max1: Int, min2: Int, max2: Int)

	var allRules = [String:Constraints]()
	var myTicket = [Int]()
	var otherTickets = [[Int]]()

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		parseTickets(input)

		return otherTickets
			.flatMap { invalidFields(inTicket: $0) }
			.reduce(0, +)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		parseTickets(input)

		otherTickets.removeAll { !invalidFields(inTicket: $0).isEmpty }
		otherTickets += [myTicket]

		let numberOfFields = myTicket.count
		var fieldIds = [Int:String]()
		var remainingRules = allRules

		while fieldIds.count < numberOfFields {
			var anyChanges = false

			fieldIdLoop: for fieldId in 0..<numberOfFields where fieldIds[fieldId] == nil {
				var candidateRuleForField: String? = nil

				ruleLoop: for (ruleName, c) in remainingRules {
					for ticket in otherTickets {
						guard isValidField(ticket[fieldId], forConstraints: c) else {
							continue ruleLoop
						}
					}

					guard candidateRuleForField == nil else {
						debug("at least(!) two rules match for field \(fieldId): \(candidateRuleForField!), \(ruleName)")
						continue fieldIdLoop
					}

					candidateRuleForField = ruleName
				}

				guard let matchingRuleForField = candidateRuleForField else {
					err("no rules match for field \(fieldId)")
				}

				debug("MATCH: field \(fieldId) is \(matchingRuleForField)")
				fieldIds[fieldId] = matchingRuleForField
				remainingRules.removeValue(forKey: matchingRuleForField)
				anyChanges = true
			}

			guard anyChanges else { err("i'm stuck") }
		}

		// print final ticket
		debug("")
		fieldIds.sorted(by: { $0.1 < $1.1 }).forEach {
			debug("\($0.1): \(myTicket[$0.0])")
		}

		return fieldIds
			.filter { $0.1.hasPrefix("departure") }
			.map { myTicket[$0.0] }
			.reduce(1, *)
	}

	func isValidField(_ n: Int, forConstraints c: Constraints) -> Bool {
		return ((n >= c.min1 && n <= c.max1) || (n >= c.min2 && n <= c.max2))
	}

	func isValidField(_ n: Int) -> Bool {
		for (_, c) in allRules {
			if isValidField(n, forConstraints: c) {
				return true
			}
		}

		return false
	}

	func invalidFields(inTicket ticket: [Int]) -> [Int] {
		return ticket.filter { !isValidField($0) }
	}

	func parseTickets(_ input: PuzzleInput) {
		var lines = input.lines

		while true {
			let line = lines.removeFirst()
			guard !line.isEmpty else { break }

			let lineComp = line.components(separatedBy: ": ")
			let rangeComp = lineComp[1].components(separatedBy: " or ")
			let rangeComp1 = rangeComp[0].components(separatedBy: "-")
			let rangeComp2 = rangeComp[1].components(separatedBy: "-")

			allRules[lineComp[0]] =  Constraints(
				min1: Int(rangeComp1[0])!,
				max1: Int(rangeComp1[1])!,
				min2: Int(rangeComp2[0])!,
				max2: Int(rangeComp2[1])!
			)
		}

		lines.removeFirst() // "your ticket:"
		myTicket = lines.removeFirst().components(separatedBy: ",").map { Int($0)! }

		lines.removeFirst(2) // \n, "nearby tickets:"
		for line in lines {
			otherTickets += [line.components(separatedBy: ",").map { Int($0)! }]
		}
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
				// N.B.: We have manually added "departure" to the "class" and "row" fields
				// so this test produces a comparable result for part 2.
				PuzzleTest(PuzzleInput(fromFile: "16-input-test-part2"), result: 132),
			]
		),
	]

	required init() {}
}

