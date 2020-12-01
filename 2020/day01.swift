//
// N.B.: This is version is a bit more cleaned up, generalized and optimized. For the version
// used to solve at first, see git history.
//
class Day01 {
	static func findSum(_ sum: Int, inArray remaining: [Int], maxDepth: Int, having: [Int]) -> [Int] {
		let currentSum = having.reduce(0, { $0 + $1 })

		guard having.count != maxDepth else {
			// max. depth reached
			if currentSum == 2020 { return having }
			return []
		}

		guard currentSum < sum else {
			// no point in checking further if we already overshot
			return []
		}

		guard remaining.count > 0 else { return [] }

		var a = remaining
		while a.count > 0 {
			let next = a.removeFirst()
			let r = findSum(sum, inArray: a, maxDepth: maxDepth, having: having + [next])

			if r.count > 0 { return r }
		}

		return []
	}

	static func part1(_ input: PuzzleInput) -> PuzzleResult {
		let entries = findSum(2020, inArray: input.intArray, maxDepth: 2, having: [])
		return entries.reduce(1, { $0 * $1 })
	}

	static func part2(_ input: PuzzleInput) -> PuzzleResult {
		let entries = findSum(2020, inArray: input.intArray, maxDepth: 3, having: [])
		return entries.reduce(1, { $0 * $1 })
	}
}

