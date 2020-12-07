class Day07 {
	static var allBags = [Bag]()

	struct ContainedBag {
		var name: String
		var count: Int
	}

	struct Bag {
		var name: String
		var contained: [ContainedBag]

		init(fromString s: String) {
			contained = []

			var components = s.components(separatedBy: " ")
			name = "\(components[0]) \(components[1])"

			components.removeFirst(4) // drop bag color + "bags contain(s)"

			guard !components[0].hasPrefix("no") else {
				// contains no bags
				return
			}

			while components.count > 0 {
				let cb = ContainedBag(
					name: "\(components[1]) \(components[2])",
					count: Int(components[0])!
				)

				contained += [cb]

				components.removeFirst(4)
			}
		}

		init(name: String, contained: [ContainedBag]) {
			self.name = name
			self.contained = contained
		}

		static func byName(_ s: String) -> Bag {
			let bags = allBags.filter { $0.name == s }
			guard !bags.isEmpty else { err("Bag.byName: no match for \(s)") }
			return bags[0]
		}

		var bagCount: Int {
			var bagCount = 1

			for cb in contained {
				debug("count: \(self) --> container \(cb)")
				bagCount += cb.count * Bag.byName(cb.name).bagCount
			}

			return bagCount
		}

		func canContain(_ name: String) -> Bool {
			debug("canContain? for bag \(self)")
			// check direct matches
			if !contained.filter({ $0.name == name }).isEmpty { return true }

			debug("canContain? for bag \(self) - no direct matches, trying indirect")
			// check indirect matches
			return contained.map({ Bag.byName($0.name) }).contains { $0.canContain(name) }
		}
	}

	static func part1(_ input: PuzzleInput) -> PuzzleResult {
		allBags = input.lines.map { Bag(fromString: $0) }
		allBags.forEach { debug("container \($0.name) containing \($0.contained)") }

		allBags.filter({ $0.canContain("shiny gold") }).forEach { debug("\($0)") }
		return allBags.filter({ $0.canContain("shiny gold") }).count
	}

	static func part2(_ input: PuzzleInput) -> PuzzleResult {
		allBags = input.lines.map { Bag(fromString: $0) }
		let shiny = Bag.byName("shiny gold")
		return shiny.bagCount - 1 // not counting the shiny itself
	}
}

