typealias PuzzleResult = Int

struct Puzzle {
	var implementation: ((PuzzleInput) -> PuzzleResult)
	var input: PuzzleInput
	var tests: [PuzzleTest]
}

protocol PuzzleClass {
	var puzzleConfig: [String:Puzzle] { get }
	init()
}

var PuzzleClasses: [String:PuzzleClass] = [
	"d01": Day01(),
	"d02": Day02(),
	"d03": Day03(),
	"d04": Day04(),
	"d05": Day05(),
	"d06": Day06(),
	"d07": Day07(),
	"d08": Day08(),
	"d09": Day09(),
	"d10": Day10(),
	"d11": Day11(),
	"d12": Day12(),
	"d13": Day13(),
	"d14": Day14(),
	"d15": Day15(),
	"d16": Day16(),
	"d17": Day17(),
]

