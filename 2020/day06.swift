class Day06: PuzzleClass {
	typealias AnswersByQuestion = Dictionary<Character, Int>
	struct GroupAnswers {
		var pax = 0
		var answers = AnswersByQuestion()

		var sumPart1: Int { answers.keys.count }
		var sumPart2: Int { answers.filter { $0.1 == pax }.count }
	}

	func parsev2(_ input: [[String]]) -> [GroupAnswers] {
		var r = [GroupAnswers]()

		for lineGroup in input {
			var ga = GroupAnswers()

			for line in lineGroup {
				ga.pax += 1

				for question in line {
					ga.answers[question] = (ga.answers[question] ?? 0) + 1
				}
			}

			r += [ga]
		}

		return r
	}

	func part1(_ input: PuzzleInput) -> PuzzleResult {
		return parsev2(input.lineGroups)
			.map { $0.sumPart1 }
			.reduce(0, +)
	}

	func part2(_ input: PuzzleInput) -> PuzzleResult {
		return parsev2(input.lineGroups)
			.map { $0.sumPart2 }
			.reduce(0, +)
	}

	// -------------------------------------------------------------

	lazy var puzzleConfig = [
		"p1": Puzzle(
			implementation: part1,
			input: PuzzleInput(fromFile: "06-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "06-input-test"), result: 11),
			]
		),
		"p2": Puzzle(
			implementation: part2,
			input: PuzzleInput(fromFile: "06-input"),
			tests: [
				PuzzleTest(PuzzleInput(fromFile: "06-input-test"), result: 6),
			]
		),
	]

	required init() {}
}

