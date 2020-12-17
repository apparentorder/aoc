class Day17: PuzzleClass {
	var isPart2 = false

	var activeCubes = Set<Coordinates4D>()
	var nextActiveCubes = Set<Coordinates4D>()

	struct Coordinates4D: Hashable {
		var w: Int
		var x: Int
		var y: Int
		var z: Int
	}

	func cubes(cycles: Int) -> Int {
		debug("Before any cycles:")
		debugDimension()

		for cycle in 1...cycles {
			nextActiveCubes.removeAll()
			var cubesToCheck = Dictionary<Coordinates4D, Int>()

			for cube in activeCubes {
				for neighbor in allNeighbors(of: cube) {
					cubesToCheck[neighbor] = (cubesToCheck[neighbor] ?? 0) + 1
				}
			}

			for (cube, activeNeighborCount) in cubesToCheck {
				if activeCubes.contains(cube) {
					if (activeNeighborCount == 2 || activeNeighborCount == 3) {
						nextActiveCubes.insert(cube)
					}
				} else {
					if activeNeighborCount == 3 {
						nextActiveCubes.insert(cube)
					}
				}
			}

			activeCubes = nextActiveCubes

			debug("After cycle: \(cycle)")
			debug("capacity aC: \(activeCubes.capacity)")
			debugDimension()
		}

		return activeCubes.count
	}

	func allNeighbors(of loc: Coordinates4D) -> Set<Coordinates4D> {
		var r = Set<Coordinates4D>(minimumCapacity: 80)

		for w in [-1, 0, +1] {
			for x in [-1, 0, +1] {
				for y in [-1, 0, +1] {
					for z in [-1, 0, +1] where !(x == 0 && y == 0 && z == 0 && w == 0) && (w == 0 || isPart2) {
						r.insert(Coordinates4D(
							w: loc.w + w,
							x: loc.x + x,
							y: loc.y + y,
							z: loc.z + z
						))
					}
				}
			}
		}

		return r
	}

	func parse(_ input: PuzzleInput) {
		for (rowIndex, row) in input.lines.enumerated() {
			for (colIndex, char) in row.enumerated() where char == "#" {
				nextActiveCubes.insert(Coordinates4D(w: 0, x: colIndex, y: rowIndex, z: 0))
			}
		}

		activeCubes = nextActiveCubes
	}

	func debugDimension() {
		#if DEBUG
		let maxW = activeCubes.map { $0.w }.max()!
		let maxX = activeCubes.map { $0.x }.max()!
		let maxY = activeCubes.map { $0.y }.max()!
		let maxZ = activeCubes.map { $0.z }.max()!

		for w in -maxW...maxW {
			for z in -maxZ...maxZ {
				debug("z=\(z), w=\(w)")

				for y in -maxY...maxY {
					var s = ""
					for x in -maxX...maxX {
						let here = Coordinates4D(w: w, x: x, y: y, z: z)
						s += (x == 0 && y == 0) ? "0" : (activeCubes.contains(here) ? "#" : ".")
					}
					debug(s)
				}
				debug("")
			}
		}
		debug("------------------------------------------------------------------------")
		#endif
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		isPart2 = false
		parse(input)
		return cubes(cycles: 6)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		isPart2 = true
		parse(input)
		return cubes(cycles: 6)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "17-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "17-input-test"), result: 112),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "17-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "17-input-test"), result: 848),
			]
		),
	]

	required init() {}
}

