class Day06 {
	typealias AnswersByQuestion = Dictionary<Character, Int>
	struct GroupAnswers {
		var pax = 0
		var answers = AnswersByQuestion()

		var sumPart1: Int { answers.keys.count }
		var sumPart2: Int { answers.filter { $0.1 == pax }.count }
	}

	static func parsev2(_ input: [[String]]) -> [GroupAnswers] {
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

	static func part1(_ input: PuzzleInput) -> PuzzleResult {
		return parsev2(input.lineGroups)
			.map { $0.sumPart1 }
			.reduce(0, +)
	}

	static func part2(_ input: PuzzleInput) -> PuzzleResult {
		return parsev2(input.lineGroups)
			.map { $0.sumPart2 }
			.reduce(0, +)
	}
}

