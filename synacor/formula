#!/usr/bin/env swift

import Foundation

enum Coin: Int {
	case Red = 2
	case Corroded = 3
	case Shiny = 5
	case Concave = 7
	case Blue = 9
}

let coins: [Coin] = [.Red, .Corroded, .Shiny, .Concave, .Blue]

func perm(having: [Coin], remaining: [Coin]) {
	if remaining.isEmpty {
		let x = having // lazy typing

		if (x[0].rawValue + x[1].rawValue * x[2].rawValue**2 + x[3].rawValue**3 - x[4].rawValue) == 399 {
			print("match!")
			print("\(having.map { $0.rawValue })")
			print("\(having)")
			exit(0)
		}
	}

	for coin in remaining {
		var h = having
		var r = remaining

		r.removeAll(where: { $0 == coin })
		h.append(coin)

		perm(having: h, remaining: r)
	}
}

perm(having: [], remaining: coins)

infix operator **: BitwiseShiftPrecedence
func ** (x: Int, y: Int) -> Int {
	var r = 1
	for _ in 0..<y { r *= x }
	return r
}

