class Day21: PuzzleClass {
	struct Food: Hashable {
		var ingredients: [String]
		var allergens: [String]
	}

	var allFoods = [Food]()

	func parse(_ input: PuzzleInput) {
		for line in input.lines {
			var parts = line.components(separatedBy: " (contains ")
			parts[1].removeLast()

			let ingredients = parts[0].components(separatedBy: " ")
			let allergens = parts[1].components(separatedBy: ", ")

			allFoods += [Food(ingredients: ingredients, allergens: allergens)]
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		parse(input)

		var allAllergens = Set(allFoods.flatMap { $0.allergens })
		var ingredientByAllergen = [String:String]() // part2

		while true {
			debug("NEXT ITERATION; allAllergens = \(allAllergens.sorted())")
			guard !allAllergens.isEmpty else { break }

			for findAllergen in allAllergens {
				var possibleMatches = Set<String>()

				for food in allFoods where food.allergens.contains(findAllergen) {
					if possibleMatches.isEmpty {
						possibleMatches.formUnion(food.ingredients)
						debug("for \(findAllergen): possible matches set to \(possibleMatches)")
					} else {
						debug("for \(findAllergen): possible matches \(possibleMatches) intersect \(food.ingredients)")
						possibleMatches.formIntersection(food.ingredients)
					}
				}

				guard possibleMatches.count != 1 else {
					let match = possibleMatches.first!
					debug("exact match: \(match) contains \(findAllergen)")

					allAllergens.remove(findAllergen)
					ingredientByAllergen[findAllergen] = match

					for i in 0..<allFoods.count {
						allFoods[i].ingredients.removeAll { $0 == match }
					}

					continue
				}
			}
		}

		let remainingIngredients = allFoods.flatMap { $0.ingredients }
		debug("remaining: \(remainingIngredients)")

		print("PART 2: \(ingredientByAllergen.sorted(by: { $0.key < $1.key }).map { $0.value }.joined(separator: ","))")

		return remainingIngredients.count
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return -2
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "21-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "21-input-test"), result: 5),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "21-input"),
			tests: [
				//PuzzleTest(PuzzleInput(fromFile: "21-input-test"), result: 273),
			]
		),
	]

	required init() {}
}

