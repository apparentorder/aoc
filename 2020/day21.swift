class Day21: PuzzleClass {
	struct Food: Hashable {
		var ingredients: [String]
		var allergens: [String]
	}

	var allFoods = [Food]()
	var dangerousIngredients = [String:String]()

	func filterAllergens() {
		var allAllergens = Set(allFoods.flatMap { $0.allergens })

		while !allAllergens.isEmpty {
			debug("NEXT ITERATION; allAllergens = \(allAllergens.sorted())")

			for allergen in allAllergens {
				var ingredientsWithAllergen = Set<String>()

				for food in allFoods where food.allergens.contains(allergen) {
					let ingredients = Set(food.ingredients).subtracting(dangerousIngredients.values)

					ingredientsWithAllergen = (ingredientsWithAllergen.isEmpty) ?
						ingredients : ingredientsWithAllergen.intersection(ingredients)

					debug("for \(allergen): remaining possible matches: \(ingredientsWithAllergen)")

					guard ingredientsWithAllergen.count != 1 else {
						let ingredient = ingredientsWithAllergen.first!
						debug("exact match: \(ingredient) contains \(allergen)")

						allAllergens.remove(allergen)
						dangerousIngredients[allergen] = ingredient

						break
					}
				}
			}
		}
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		parse(input)
		filterAllergens()

		let remainingIngredients = allFoods.flatMap { $0.ingredients }.filter { !dangerousIngredients.values.contains($0) }
		debug("remaining: \(remainingIngredients)")
		return remainingIngredients.count
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		parse(input)
		filterAllergens()
		return dangerousIngredients.sorted(by: { $0.key < $1.key }).map { $0.value }.joined(separator: ",")
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

