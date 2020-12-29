import Foundation

var debugEnabled = false

CommandLine.arguments.removeFirst() // remove executable name
guard CommandLine.arguments.count > 0 else { usage() }
if CommandLine.arguments[0] == "-debug" {
	debugEnabled = true
	CommandLine.arguments.removeFirst()
}

guard CommandLine.arguments.count <= 2 else { usage() }
guard CommandLine.arguments.count > 0 else { usage() }
let puzzleClassName = CommandLine.arguments.removeFirst()
if puzzleClassName == "all" {
	for (pcKey, pc) in PuzzleClasses.sorted(by: { $1.0 > $0.0 }) {
		for puzzleKey in pc.puzzleConfig.keys.sorted() {
			print("------------------------------------------------------------------------")
			print(">>> Running \(pcKey) \(puzzleKey)")
			print("------------------------------------------------------------------------")
			runPuzzle(pc, puzzleKey)
		}
	}
	exit(0)
}

guard let puzzleClassObject = PuzzleClasses[puzzleClassName] else { err("unknown puzzleClass \(puzzleClassName)") }

if CommandLine.arguments.count == 0 {
	for puzzleKey in puzzleClassObject.puzzleConfig.keys.sorted() {
		print("------------------------------------------------------------------------")
		print(">>> Running \(puzzleClassName) \(puzzleKey)")
		print("------------------------------------------------------------------------")
		runPuzzle(puzzleClassObject, puzzleKey)
	}
	exit(0)
}

let puzzleName = CommandLine.arguments.removeFirst()

// if control reaches here, we have just one class and just one puzzle to run

guard puzzleClassObject.puzzleConfig.keys.contains(puzzleName) else {
	err("class \(puzzleClassName) has no puzzle named \(puzzleName)")
}

runPuzzle(puzzleClassObject, puzzleName)

