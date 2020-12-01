class Day01 {

	static func findSum(_ sum: Int, ofExpenses expenses: [Int], withCount: Int) -> [Int] {
		for e1 in expenses {
			for e2 in expenses {
				if withCount == 3 {
					for e3 in expenses {
						if e1 + e2 + e3 == 2020 {
							print("MATCH: \(e1) + \(e2) + \(e3)")
							return [e1, e2, e3]
						}
					}
				} else {
					if e1 + e2 == 2020 {
						print("MATCH: \(e1) + \(e2)")
						return [e1, e2]
					}
				}
			}
		}

		err("no match found")
	}

	static func part1(_ input: PuzzleInput) -> PuzzleResult {
		let entries = findSum(2020, ofExpenses: input.intArray, withCount: 2)
		return entries[0] * entries[1]
	}

	static func part2(_ input: PuzzleInput) -> PuzzleResult {
		let entries = findSum(2020, ofExpenses: input.intArray, withCount: 3)
		return entries[0] * entries[1] * entries[2]
	}
}

