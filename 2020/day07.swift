import Foundation

class Day07 {
	typealias BagName = String
	typealias ContainedBagsRequired = Dictionary<BagName, Int>

	// part1: for each BagName: a list of BagNames that are possible containers for it
	static var allRulesInverse = Dictionary<BagName, Array<BagName>>() // part1

	// part2: direct translation of the input text rules:
	// for each BagName: the list and amount of required containers
	static var allRules = Dictionary<BagName, ContainedBagsRequired>() // part2

	static var countCache = ContainedBagsRequired()

	// N.B.: globals might be contaminated from tests -- clear before use!

	static func /* part1 */ possibleBags(forBag bagName: BagName) -> [BagName] {
		var bagsSeen = [BagName:Bool]() // lazy: dummy dict instead of Set()
		var bagNameQueue = [bagName]

		repeat {
			let bag = bagNameQueue.removeFirst()
			guard bagsSeen[bag] == nil else { continue } // already seen
			bagsSeen[bag] = true

			guard let containedBags = allRulesInverse[bag] else { continue } // dead end
			bagNameQueue += containedBags
		} while !bagNameQueue.isEmpty

		return Array(bagsSeen.keys)
	}

	static func /* part2 */ countRequiredBags(forBag bagName: String) -> Int {
		countCache.removeAll()

		var bagCount = 1

		for (containedBagName, containedBagCount) in allRules[bagName]! {
			let containedBagTotalCount: Int

			if let c = countCache[containedBagName] {
				containedBagTotalCount = c
			} else {
				containedBagTotalCount = countRequiredBags(forBag: containedBagName)
				countCache[containedBagName] = containedBagTotalCount
			}

			bagCount += containedBagCount * containedBagTotalCount
		}

		return bagCount
	}

	static func parseRules(_ inputLines: [String]) {
		let start = Date()

		allRules.removeAll()
		allRulesInverse.removeAll()

		for rule in inputLines {
			debug("PARSE: LINE: \(rule)")
			var components = rule.components(separatedBy: " ")

			let name = "\(components[0]) \(components[1])"
			allRules[name] = ContainedBagsRequired()

			components.removeFirst(4) // drop bag color + "bags contain(s)"
			guard components[0] != "no" else {
				// "contains no bags"
				continue
			}

			while !components.isEmpty {
				let cbName = "\(components[1]) \(components[2])"
				allRules[name]![cbName] = Int(components[0])!
				allRulesInverse[cbName] = (allRulesInverse[cbName] ?? []) + [name]

				debug("PARSE: \(name) -> \(cbName) x\(Int(components[0])!)")
				components.removeFirst(4)
			}
		}

		print(">>> rule parse time: " + elapsed(from: start, to: Date()))
	}

	static func part1(_ input: PuzzleInput) -> PuzzleResult {
		parseRules(input.lines)
		return possibleBags(forBag: "shiny gold").count - 1 // not counting the shiny bag itself
	}

	static func part2(_ input: PuzzleInput) -> PuzzleResult {
		parseRules(input.lines)
		return countRequiredBags(forBag: "shiny gold") - 1 // not counting the shiny bag itself
	}
}

