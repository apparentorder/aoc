import CryptoKit

class Day17: PuzzleClass {
	let hexAlphabet = Array("0123456789abcdef")
	var salt = ""

	struct Direction: CustomStringConvertible {
		let heading: Heading
		let char: String
		var description: String { char }
	}

	struct Path {
		var pathString = ""
		var position = Coordinates(0,0)
	}

	let allDirections = [
		// note: order matters, allDirections[n] corresponds to the n'th char of the hash.
		Direction(heading: .north, char: "U"),
		Direction(heading: .south, char: "D"),
		Direction(heading: .west,  char: "L"),
		Direction(heading: .east,  char: "R"),
	]

	func md5HashString(_ message: String) -> [Character] {
		let digest = Insecure.MD5.hash(data: message.data(using: .utf8)!)
		var r = Array(repeating: Character("_"), count: 32)

		var i = 0
		for d in digest {
			r[i*2] = hexAlphabet[Int(d / 0x10)]
			r[i*2+1] = hexAlphabet[Int(d % 0x10)]
			i += 1
		}

		return r
	}

	func candidateDirections(after path: String, atPosition position: Coordinates) -> [Direction] {
		let doors = md5HashString(salt + path).prefix(4)
		var r = [Direction]()
		let doorOpenCharacters: [Character] = ["b", "c", "d", "e", "f"]

		for i in 0..<4 {
			guard doorOpenCharacters.contains(doors[i]) else { continue /* door closed */ }
			let candidateDirection = allDirections[i]

			r.append(candidateDirection)
		}

		return r
	}

	//func findShortestPath(to: Coordinates) -> String {
	func findPaths(to: Coordinates, shortestOnly: Bool = false) -> [Path] {
		var r = [Path]()

		var paths = [
			Path(), // start with empty path
		]

		var nextPaths = [Path]()

		while true {
			guard !paths.isEmpty else {
				break
			}

			for path in paths {
				guard path.position != Coordinates(3,3) else {
					// gotcha!
					//return path.pathString
					r += [path]
					guard !shortestOnly else { return r }
					continue
				}

				let candidates = candidateDirections(after: path.pathString, atPosition: path.position)
				//debug("candidates for \(salt + path.pathString): \(candidates)")

				for candidate in candidates {
					let newPos = Coordinates(
						path.position.x + candidate.heading.rawValue.x,
						path.position.y + candidate.heading.rawValue.y
					)
					guard 0...3 ~= newPos.x else { continue }
					guard 0...3 ~= newPos.y else { continue }

					nextPaths.append(Path(
						pathString: path.pathString + candidate.char,
						position: newPos
					))
				}
			}

			paths = nextPaths
			nextPaths.removeAll(keepingCapacity: true)
		}

		return r
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		salt = input.raw
		let shortestPath = findPaths(to: Coordinates(3,3), shortestOnly: true)
		return shortestPath.first!.pathString
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		salt = input.raw
		let paths = findPaths(to: Coordinates(3,3))
		return paths.map { $0.pathString.count }.sorted(by: >).first!
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromString: "hhhxzeay"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "ihgpwlah"), result: "DDRRRD"),
				PuzzleTest(PuzzleInput(fromString: "kglvqrro"), result: "DDUDRLRRUDRD"),
				PuzzleTest(PuzzleInput(fromString: "ulqzkmiv"), result: "DRURDRUDDLLDLUURRDULRLDUUDDDRR"),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromString: "hhhxzeay"),
			tests: [
				PuzzleTest(PuzzleInput(fromString: "ihgpwlah"), result: 370),
				PuzzleTest(PuzzleInput(fromString: "kglvqrro"), result: 492),
				PuzzleTest(PuzzleInput(fromString: "ulqzkmiv"), result: 830),
			]
		),
	]

	required init() {}

}

