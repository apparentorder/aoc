#!/usr/bin/env swift -g

//
//  admittedly, this is the first puzzle where i had to resear^Wlook up the
//  solution on the internet. after 3+ days full-time exploration of different
//  ideas, i gave up.
//
//  even after finding this marvelous gem, it took some hours:
//  https://codeforces.com/blog/entry/72593
//

import Foundation

// real modulo function
// (Swift provides as % simply a remainder function, i.e.
// produces negative results)
infix operator %%
func %%(lhs: Int, rhs: Int) -> Int {
	let x = lhs % rhs
	return (x >= 0 ? x : x + rhs)
}

extension Int {
	var isPrime: Bool {
		guard self >= 1     else { return false }
		guard self > 3	    else { return true } // true for 2, 3
		var i = 2
		while i * i <= self {
			if self % i == 0 {
				return false
			}
			i += 1
		}
		return true
	}
}

func double_multiply_mod(_ _x: Int, _ _y: Int, modulus: Int) -> Int {
	var x = abs(_x)
	var y = abs(_y)

	var ret = 0
	while x >= 1 {
		if !x.isMultiple(of: 2) {
			ret = (ret + y) %% modulus
		}
		y = (y * 2) %% modulus

		x = x/2
	}

	if (_x < 0 && _y >= 0) || (_y < 0 && _x >= 0) {
		// exactly one arg. was negative, so return
		// negative number
		ret *= -1
	}

	return ret
}

// exponentiation, modulo m
func pow_mod(_ _x: Int, exponent: Int, modulus: Int) -> Int {
	var x = _x
	var n = exponent
	var y = 1

	if n == 0 { return 1 }

	while n > 1 {
		if n.isMultiple(of: 2) {
			x = double_multiply_mod(x, x, modulus: modulus)
			n /= 2
		} else {
			y = double_multiply_mod(y, x, modulus: modulus)
			x = double_multiply_mod(x, x, modulus: modulus)
			n = (n - 1) / 2
		}
	}

	return double_multiply_mod(y, x, modulus: modulus) %% modulus
}

struct ShuffleSequence {
	struct lcfCoefficients {
		var a: Int
		var b: Int
		var c: Int { return a }
		var d: Int { return b }
	}

	public let deck: CardDeck
	public var composedCoeff: lcfCoefficients

	init(fromFileName inputFile: String, forDeck deck: CardDeck) {
		let contents = try! String(contentsOfFile: inputFile, encoding: .utf8)
		let inputLines = contents.split(separator: "\n")
		var instructions = [lcfCoefficients]()

		self.deck = deck

		for s in inputLines {
			if s == "deal into new stack" {
				instructions += [lcfCoefficients(a: -1, b: -1)]
			} else if let range = s.range(of: "deal with increment ") {
				let incr = Int(s[range.upperBound...])!
				instructions += [lcfCoefficients(a: incr, b: 0)]
			} else if let range = s.range(of: "cut ") {
				let top = Int(s[range.upperBound...])!
				instructions += [lcfCoefficients(a: 1, b: -1 * top)]
			} else {
				fatalError("unknown instruction in input: \(s)")
			}
		}

		var coeff = instructions.removeFirst()
		for add in instructions {
			coeff.a = (coeff.a * add.c) %% deck.size
			coeff.b = (coeff.b * add.c + add.d) %% deck.size
		}

		composedCoeff = coeff
	}

	func shuffle(times: Int = 1, inverse: Bool = false) {
		let a = composedCoeff.a
		let b = composedCoeff.b
		let m = deck.size
		let x = deck.currentPosition

		if times == 1 && !m.isPrime {
			deck.currentPosition = (a * x + b) %% m
			return
		}

		precondition(m.isPrime, "shuffle() with a non-prime modulus (deck size)")

		let ak = pow_mod(a, exponent: times, modulus: m)

		let dividend = double_multiply_mod(b, (1 - ak), modulus: m)
		let divisor = (1 - a) %% m

		let modinverse = pow_mod(divisor, exponent: m - 2, modulus: m)
		let div_result = double_multiply_mod(dividend, modinverse, modulus: m)

		if inverse {
			let inv_dividend = (x - div_result)
			let inv_divisor = ak
			let inv_modinverse = pow_mod(inv_divisor, exponent: m - 2, modulus: m)
			let inv_div_result = double_multiply_mod(inv_dividend, inv_modinverse, modulus: m)
			deck.currentPosition = inv_div_result
		} else {
			deck.currentPosition = (ak * x + div_result) %% m
		}
	}
}

class CardDeck: CustomStringConvertible {
	public let size: Int
	public let startPosition: Int
	public var currentPosition: Int

	init(ofSize size: Int, traceStartPosition startPosition: Int) {
		self.size = size
		self.startPosition = startPosition
		self.currentPosition = startPosition
	}

	public var description: String {
		return "Card moved from \(startPosition) to \(currentPosition)"
	}
}

func runTests() {
	let allTests = [
		"example1":    [ "fname": "example1", "size": 10, "fromPosition": 1, "toPosition": 7, "times": 1 ],
		"example2":    [ "fname": "example2", "size": 10, "fromPosition": 1, "toPosition": 4, "times": 1 ],
		"example3":    [ "fname": "example3", "size": 10, "fromPosition": 1, "toPosition": 5, "times": 1 ],
		"example4":    [ "fname": "example4", "size": 10, "fromPosition": 1, "toPosition": 4, "times": 1 ],
		"input-1":     [ "fname": "input", "size": 10007, "fromPosition": 2019, "toPosition": 3749, "times": 1 ],
		"input-10006": [ "fname": "input", "size": 10007, "fromPosition": 2019, "toPosition": 2019, "times": 10006 ],
	]

	for (name, testdef) in allTests {
		let d = CardDeck(ofSize: testdef["size"] as! Int, traceStartPosition: testdef["fromPosition"] as! Int)
		let s = ShuffleSequence(fromFileName: testdef["fname"] as! String, forDeck: d)
		s.shuffle(times: testdef["times"] as! Int)
		precondition(d.currentPosition == testdef["toPosition"] as! Int, "\(name) returned \(d)")
		print("passed test \(name)")
	}
}

func runTestInverse() {
	let d = CardDeck(ofSize: 10007, traceStartPosition: 3749)
	let s = ShuffleSequence(fromFileName: "input", forDeck: d)

	s.shuffle(times: 1, inverse: true)
	let cardAt3749 = d.currentPosition
	print("testinverse: card at 3749:", cardAt3749)
}

func runPart1() {
	let d = CardDeck(ofSize: 10007, traceStartPosition: 2019)
	let s = ShuffleSequence(fromFileName: "input", forDeck: d)

	s.shuffle()
	let posOf2019 = d.currentPosition
	print("part1: pos of 2019 after 1 shuffle:", posOf2019)
}

func runPart2() {
	let d = CardDeck(ofSize: 119315717514047, traceStartPosition: 2020)
	let s = ShuffleSequence(fromFileName: "input", forDeck: d)

	s.shuffle(times: 101741582076661, inverse: true)
	let cardAt2020 = d.currentPosition
	print("part2: card at 2020 after 101741582076661 shuffles:", cardAt2020)
}

runTests()
runTestInverse()
runPart1()
runPart2()

