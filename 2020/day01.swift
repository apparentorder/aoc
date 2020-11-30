class Day01 {
	struct WeightCalc {
		let weight: Int
		let isPart2: Bool

		var fuel: Int {
			if !isPart2 {
				return Int(weight / 3) - 2
			}

			var x = weight
			var r = 0

			while true {
				let this = Int(x / 3) - 2

				guard this > 0 else { break }
				r += this
				x  = this
			}

			return r
		}
	}

	static func calcFuel(weights: [Int], isPart2: Bool) -> PuzzleResult {
		var totalFuel = 0

		for weight in weights {
			let wc = WeightCalc(weight: weight, isPart2: isPart2)
			totalFuel += wc.fuel
		}

		return totalFuel
	}

	static func part1(_ input: PuzzleInput) -> PuzzleResult {
		return calcFuel(weights: input.intArray, isPart2: false)
	}

	static func part2(_ input: PuzzleInput) -> PuzzleResult {
		return calcFuel(weights: input.intArray, isPart2: true)
	}
}

