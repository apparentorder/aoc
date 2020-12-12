import Foundation

class Day11: PuzzleClass {
	func gameOfSeats(_ input: PuzzleInput, isPart2: Bool) -> PuzzleResult {
		var changes = 0
		var map = input.matrix
		let maxPeople = isPart2 ? 5 : 4
		var lock = os_unfair_lock_s()

		repeat {
			changes = 0
			var mapNext = map
			DispatchQueue.concurrentPerform(iterations: map.columns) { x in
				DispatchQueue.concurrentPerform(iterations: map.rows) { y in
					debug("AT \(x),\(y)")

					let c = map.getChar(atCoordinates: x, y)
					guard c == "L" || c == "#" else { return }

					let surroundingSeatsOccupied = self.countOccupiedSeats(
						map: map,
						from: (x, y),
						maxIterations: isPart2 ? nil : 1
					)
					debug("surroundingSeatsOccupied: \(surroundingSeatsOccupied)")

					if c == "#" && surroundingSeatsOccupied >= maxPeople {
						os_unfair_lock_lock(&lock)
						mapNext.data[y][x] = "L"
						changes += 1
						os_unfair_lock_unlock(&lock)
					} else if c == "L" && surroundingSeatsOccupied == 0 {
						os_unfair_lock_lock(&lock)
						mapNext.data[y][x] = "#"
						changes += 1
						os_unfair_lock_unlock(&lock)
					}
				}
			}

			map = mapNext

			debug("------------------------------------------------------------------------")
			debug(map)
		} while changes > 0

		return map.data.reduce(0, { $0 + $1.filter({ $0 == "#" }).count })
	}

	func countOccupiedSeats(map: Matrix, from: (x: Int, y: Int), maxIterations: Int?) -> Int {
		var surroundingSeatsOccupied = 0

		for moveX in [-1, 0, +1] {
			for moveY in [-1, 0, +1] {
				let surroundingSeat = map.findFirstCharacter(
					except: ".",
					inDirection: (moveX, moveY),
					fromCoordinates: from,
					maxIterations: maxIterations
				)

				if let c = surroundingSeat, c == "#" {
					surroundingSeatsOccupied += 1
				}
			}
		}

		return surroundingSeatsOccupied
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

