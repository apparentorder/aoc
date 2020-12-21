class Day21: PuzzleClass {
	struct Food: Hashable {
		var ingredients: Set<String>
		var allergens: Set<String>
	}

	var allFoods = [Food]()
	var dangerousIngredients = [String:String]()

	func filterAllergens() {
		var remainingAllergens = Set(allFoods.flatMap { $0.allergens })

		while !remainingAllergens.isEmpty {
			debug("NEXT ITERATION; remainingAllergens = \(remainingAllergens.sorted())")
			var allergenIngredients = [String:Set<String>]()

			for food in allFoods {
				let ingredients = Set(food.ingredients).subtracting(dangerousIngredients.values)

				food.allergens.subtracting(dangerousIngredients.keys).forEach {
					allergenIngredients[$0] =
						(allergenIngredients[$0] ?? Set(ingredients)).intersection(ingredients)
				}
			}

			for (allergen, ingredients) in allergenIngredients
			where ingredients.count == 1 && dangerousIngredients[allergen] == nil {
				debug("exact match: \(ingredients.first!) contains \(allergen)")
				remainingAllergens.remove(allergen)
				dangerousIngredients[allergen] = ingredients.first!
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

			let ingredients = Set(parts[0].components(separatedBy: " "))
			let allergens = Set(parts[1].components(separatedBy: ", "))

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

