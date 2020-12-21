class Day21: PuzzleClass {
	struct Food: Hashable {
		var ingredients: [String]
		var allergens: [String]
	}

	var allFoods = [Food]()
	var allergenIngredient = [String:String]()

	func filterAllergens() {
		var allAllergens = Set(allFoods.flatMap { $0.allergens })

		while !allAllergens.isEmpty {
			debug("NEXT ITERATION; allAllergens = \(allAllergens.sorted())")

			for allergen in allAllergens {
				var ingredients = Set<String>()

				for food in allFoods where food.allergens.contains(allergen) {
					ingredients = (ingredients.isEmpty) ?
						Set(food.ingredients) :
						ingredients.intersection(food.ingredients)

					debug("for \(allergen): remaining possible matches: \(ingredients)")

					guard ingredients.count != 1 else {
						let match = ingredients.first!
						debug("exact match: \(match) contains \(allergen)")

						allAllergens.remove(allergen)
						allergenIngredient[allergen] = match

						for i in 0..<allFoods.count {
							allFoods[i].ingredients.removeAll { $0 == match }
						}

						break
					}
				}
			}
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		parse(input)
		filterAllergens()
		let remainingIngredients = allFoods.flatMap { $0.ingredients }
		debug("remaining: \(remainingIngredients)")
		return remainingIngredients.count
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		parse(input)
		filterAllergens()
		return allergenIngredient.sorted(by: { $0.key < $1.key }).map { $0.value }.joined(separator: ",")
	}

	func parse(_ input: PuzzleInput) {
		for line in input.lines {
			var parts = line.components(separatedBy: " (contains ")
			parts[1].removeLast()

			let ingredients = parts[0].components(separatedBy: " ")
			let allergens = parts[1].components(separatedBy: ", ")

			allFoods += [Food(ingredients: ingredients, allergens: allergens)]
		}
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
				PuzzleTest(PuzzleInput(fromFile: "21-input-test"), result: "mxmxvkd,sqjhc,fvjkl"),
			]
		),
	]

	required init() {}
}

