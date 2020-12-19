class Day19: PuzzleClass {
	var resolvedRules = [Int:[String]](minimumCapacity: 500)
	var unresolvedRules = [Int:String](minimumCapacity: 500)

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
		//validStrings.reserveCapacity(10_0000)

		debug("START resolving rule \(ruleId)", indent: 4*depth)
		let subRules = unresolvedRules[ruleId]!.components(separatedBy: " | ")
		for subRule in subRules {
			var validStringsForSubRule = [String]()
			//validStrings.reserveCapacity(10_0000)

			let otherRuleIds = subRule.components(separatedBy: " ").map { Int($0)! }
			for otherRuleId in otherRuleIds {
				debug("... resolving rule \(ruleId), other rule \(otherRuleId)", indent: 4*(depth+1))
				let otherStrings = resolveRule(otherRuleId, depth: depth + 1)

				var newVSFSR = [String]()
				//newVSFSR.reserveCapacity(10_0000)

				for os in otherStrings {
					if validStringsForSubRule.isEmpty {
						newVSFSR += [os]
					} else {
						for vsfr in validStringsForSubRule {
							newVSFSR += [vsfr + os]
						}
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

		debug("xxx 31: \(validStringsRule31)")
		debug("xxx 42: \(validStringsRule42)")

		debug("xxx 31: min \(validStringsRule31.map { $0.count }.min()!)")
		debug("xxx 31: max \(validStringsRule31.map { $0.count }.max()!)")
		debug("xxx 42: min \(validStringsRule42.map { $0.count }.min()!)")
		debug("xxx 42: max \(validStringsRule42.map { $0.count }.max()!)")

		debug("xxx intersect 31, 42: \(Set(validStringsRule31).intersection(validStringsRule42))")

		var validCount = 0
		for message in messages {
			var remainingMessage = message
			var prefixesMatched = [String]()
			var suffixesMatched = [String]()

			// remove any matching suffix
			while true {
				var suffixMatched = false
				validStringsRule31.forEach {
					if remainingMessage.hasSuffix($0) {
						suffixesMatched.insert($0, at: 0)
						remainingMessage.removeLast($0.count)
						suffixMatched = true
						return
					}
				}
				guard suffixMatched else { break }
			}

			// bail out if no suffixes matched
			guard remainingMessage.count != message.count else {
				continue
			}

			// bail out if no potential prefixes are left
			guard !remainingMessage.isEmpty else { continue }

			// remove any matching prefix
			while true {
				var prefixMatched = false
				validStringsRule42.forEach {
					if remainingMessage.hasPrefix($0) {
						prefixesMatched += [$0]
						remainingMessage.removeFirst($0.count)
						prefixMatched = true
						return
					}
				}
				guard prefixMatched else { break }
			}

			// message must be empty now, as we were looking for ^(42)+(31)+$
			guard remainingMessage.isEmpty else { continue }

			// need more prefixes than suffixes
			guard prefixesMatched.count > suffixesMatched.count else { continue }

			validCount += 1
			debug("valid message: \(message) => \(prefixesMatched) ... \(suffixesMatched)")
		}

		return validCount
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

