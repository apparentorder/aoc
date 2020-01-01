#!/usr/bin/env swift -O

import Foundation

class CardDeck: CustomStringConvertible {
	public var cards: [Int]

	init(ofSize deckSize: Int = 10007) {
		cards = [Int](0 ..< deckSize)
		for i in 0 ..< deckSize {
			cards[i] = i
		}
	}

	public var description: String {
		return cards.map { String($0) }.joined(separator: " ")
	}

	public func dealNew() {
		var newCards = [Int](0 ..< cards.count)

		for (i, v) in cards.enumerated() {
			newCards[cards.count - i - 1] = v
		}

		cards = newCards
	}

	public func cut(topN topN_in: Int) {
		var newCards = [Int](0 ..< cards.count)
		var topN = topN_in

		if topN < 0 {
			topN = cards.count + topN
		}

		for i in 0 ..< cards.count {
			newCards[i] = cards[(i + topN) % cards.count]
		}

		cards = newCards
	}

	public func deal(withIncrement: Int? = nil) {
		var newCards = [Int](0 ..< cards.count)

		for (i, v) in cards.enumerated() {
			// deal new: just reverse it
			var pos = cards.count - 1 - i

			if let incr = withIncrement {
				// deal with increment:
				// fill every incr'th position
				pos = (incr * i) % cards.count
			}

			newCards[pos] = v
		}

		cards = newCards
	}

	func runInstructions(fromFileName inputFile: String) {
		let contents = try! String(contentsOfFile: inputFile, encoding: .utf8)
		let inputLines = contents.split(separator: "\n")

		for s in inputLines {
			if s == "deal into new stack" {
				self.deal()
				//print("self.deal()")
			} else if let range = s.range(of: "deal with increment ") {
				let incr = Int(s[range.upperBound...])!
				self.deal(withIncrement: incr)
				//print("self.deal(withIncrement: \(incr))")
			} else if let range = s.range(of: "cut ") {
				let top = Int(s[range.upperBound...])!
				self.cut(topN: top)
				//print("self.cut(topN: \(top))")
			} else {
				fatalError("unknown instruction in input: \(s)")
			}
		}
	}
}

func runTests() {
	let dnew = CardDeck(ofSize: 10)
	dnew.deal()
	assert(dnew.description == "9 8 7 6 5 4 3 2 1 0", "dealNew failed, result \(dnew)")

	let dtop3 = CardDeck(ofSize: 10)
	dtop3.cut(topN: 3)
	assert(dtop3.description == "3 4 5 6 7 8 9 0 1 2", "cut top 3 failed, result \(dtop3)")

	let dtopminus4 = CardDeck(ofSize: 10)
	dtopminus4.cut(topN: -4)
	assert(dtopminus4.description == "6 7 8 9 0 1 2 3 4 5", "cut top -4 failed, result \(dtopminus4)")

	let dinc3 = CardDeck(ofSize: 10)
	dinc3.deal(withIncrement: 3)
	assert(dinc3.description == "0 7 4 1 8 5 2 9 6 3", "deal with increment 3 failed, result \(dinc3)")

	let dex1 = CardDeck(ofSize: 10)
	dex1.runInstructions(fromFileName: "example1")
	assert(dex1.description == "0 3 6 9 2 5 8 1 4 7", "example1 returned \(dex1)")

	let dex2 = CardDeck(ofSize: 10)
	dex2.runInstructions(fromFileName: "example2")
	assert(dex2.description == "3 0 7 4 1 8 5 2 9 6", "example2 returned \(dex2)")

	let dex3 = CardDeck(ofSize: 10)
	dex3.runInstructions(fromFileName: "example3")
	assert(dex3.description == "6 3 0 7 4 1 8 5 2 9", "example3 returned \(dex3)")

	let dex4 = CardDeck(ofSize: 10)
	dex4.runInstructions(fromFileName: "example4")
	assert(dex4.description == "9 2 5 8 1 4 7 0 3 6", "example4 returned \(dex4)")
}

runTests()

let part1 = CardDeck()
part1.runInstructions(fromFileName: "input")
print("position of card 2019:", part1.cards.firstIndex(of: 2019)!)

