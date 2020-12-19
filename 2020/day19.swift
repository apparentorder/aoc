class Day19: PuzzleClass {
	var resolvedRules = [Int:[String]](minimumCapacity: 500)
	var unresolvedRules = [Int:String](minimumCapacity: 500)

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		let rules = input.lineGroups[0]
		let messages = input.lineGroups[1]

		parseRules(rules)
		let validStringsForRule0 = Set(resolveRule(0))

		let validMessages = validStringsForRule0.intersection(messages)
		validMessages.forEach { debug("valid message: \($0)") }
		return validMessages.count
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		let rules = input.lineGroups[0]
		let messages = input.lineGroups[1]

		parseRules(rules)

		// rule 0 (see below) = "8 11"
		unresolvedRules[8] = "42 | 42 8"
		unresolvedRules[11] = "42 31 | 42 11 31"

		//
		// we will assume that rule 0 is always "8 11" -- this is true for
		// the actual input and for the part2 test input, but not for the
		// part1 test input!
		//
		// therefore, any valid string consists exclusively of 1+ occurances
		// of rule 42, followed by 1+ occurrances of rule 31,
		// i.e. must match ^(42)+(31)+$, so to speak.
		//
		// additionally, the rules dictate that there must be more
		// prefixes(rule42) than there are suffixes(rule31), because rule 11
		// always has an equal amount of both of those.
		//
		// also note that all valid strings per rule have the same length,
		// as they are all combinations of different lengths.
		// further, both rules 31 and 42 are of length (test=5, puzzle=8).
		//

		let validStringsRule31 = resolveRule(31)
		let validStringsRule42 = resolveRule(42)

		debug("rule 31: valid strings: \(validStringsRule31)")
		debug("rule 42: valid strings: \(validStringsRule42)")

		var validCount = 0
		for message in messages {
			var remainingMessage = message

			let suffixesMatched = trim(anyOf: validStringsRule31, from: &remainingMessage, fromStart: false)
			guard suffixesMatched > 0 else { continue }

			let prefixesMatched = trim(anyOf: validStringsRule42, from: &remainingMessage, fromStart: true)
			guard prefixesMatched > suffixesMatched else { continue }

			guard remainingMessage.isEmpty else { continue } // message must have no other parts in the middle

			validCount += 1
			debug("valid message: \(message)")
		}

		return validCount
	}

	func parseRules(_ input: [String]) {
		for line in input {
			let parts = line.components(separatedBy: ": ")
			let ruleId = Int(parts[0])!

			if !parts[1].hasPrefix("\"") {
				unresolvedRules[ruleId] = parts[1]
			} else {
				// final rule, i.e. already resolved
				resolvedRules[ruleId] = [parts[1].filter { $0 != "\"" }]
			}
		}
		debug("initially resolved rules: \(resolvedRules)")
	}

	func resolveRule(_ ruleId: Int, depth: Int = 0) -> [String] {
		if let validStrings = resolvedRules[ruleId] {
			return validStrings
		}

		var validStrings = [String]()

		debug("START resolving rule \(ruleId)", indent: 4*depth)
		let subRules = unresolvedRules[ruleId]!.components(separatedBy: " | ")
		for subRule in subRules {
			var validStringsForSubRule = [String]()

			let otherRuleIds = subRule.components(separatedBy: " ").map { Int($0)! }
			for otherRuleId in otherRuleIds {
				debug("... resolving rule \(ruleId), other rule \(otherRuleId)", indent: 4*(depth+1))
				let otherStrings = resolveRule(otherRuleId, depth: depth + 1)

				guard !validStringsForSubRule.isEmpty else {
					validStringsForSubRule = otherStrings
					continue
				}

				var newVSFSR = [String]()
				for os in otherStrings {
					for vsfr in validStringsForSubRule {
						newVSFSR += [vsfr + os]
					}
				}
				validStringsForSubRule = newVSFSR
			}

			validStrings += validStringsForSubRule
		}

		debug("END resolving rule \(ruleId) to valid strings \(validStrings)", indent: 4*depth)

		resolvedRules[ruleId] = validStrings
		return validStrings
	}

	func trim(anyOf matches: [String], from string: inout String, fromStart: Bool) -> Int {
		var matchCount = 0
		outer: while true {
			for match in matches {
				if fromStart && string.hasPrefix(match) {
					string.removeFirst(match.count)
					matchCount += 1
					continue outer
				} else if !fromStart && string.hasSuffix(match) {
					string.removeLast(match.count)
					matchCount += 1
					continue outer
				}
			}
			break
		}

		return matchCount
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "19-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "19-input-test"), result: 2),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "19-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "19-input-test-part2"), result: 12),
			]
		),
	]

	required init() {}
}

