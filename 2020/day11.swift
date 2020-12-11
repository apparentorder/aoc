class Day11: PuzzleClass {
	func countOccupiedSeats(map: Matrix, from: (x: Int, y: Int), maxIterations: Int?) -> Int {
		var surroundingSeatsOccupied = 0

		for moveX in [-1, 0, +1] {
			for moveY in [-1, 0, +1] {
				let surroundingSeat = map.findAnyCharacter(
					of: ["#", "L"],
					inDirection: (moveX, moveY),
					fromCoordinates: (from.x, from.y),
					maxIterations: maxIterations
				)

				if let c = surroundingSeat, c == "#" {
					surroundingSeatsOccupied += 1
				}
			}
		}

		return surroundingSeatsOccupied
	}

	func gameOfSeats(_ input: PuzzleInput, isPart2: Bool) -> PuzzleResult {
		var changes = 0
		var map = input.matrix
		let maxPeople = isPart2 ? 5 : 4

		repeat {
			changes = 0
			var mapNext = map
			for x in 0..<map.columns {
				for y in 0..<map.rows {
					debug("AT \(x),\(y)")

					let surroundingSeatsOccupied = countOccupiedSeats(
						map: map,
						from: (x, y),
						maxIterations: isPart2 ? nil : 1
					)

					let c = map.getChar(atCoordinates: x, y)
					if c == "#" && surroundingSeatsOccupied >= maxPeople {
						mapNext.setChar(atCoordinates: x, y, to: "L")
						changes += 1
					} else if c == "L" && surroundingSeatsOccupied == 0 {
						mapNext.setChar(atCoordinates: x, y, to: "#")
						changes += 1
					}
				}
			}

			map = mapNext

			debug("------------------------------------------------------------------------")
			debug(map)
		} while changes > 0

		return map.data.reduce(0, { $0 + $1.filter({ $0 == "#" }).count })
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return gameOfSeats(input, isPart2: false)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return gameOfSeats(input, isPart2: true)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "11-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "11-input-test"), result: 37),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "11-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "11-input-test"), result: 26),
			]
		),
	]

	required init() {}
}

