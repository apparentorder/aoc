#!/usr/bin/env swift

import Foundation

let inputFile = "aoc14in"

let contents = try String(contentsOfFile: inputFile, encoding: .utf8)
let inputLines = contents.split(separator: "\n")

struct Reaction {
	var input: [ChemicalIngredient]
	var output: ChemicalIngredient
}

struct ChemicalIngredient {
	var chemical: String
	var amount: Int
}

var allReactions = [Reaction]()

// ----------------------------------------------------------------------

// parse input

for s in inputLines {
	var line = String(s)
	line = line.replacingOccurrences(of: " => ", with: ">")
	line = line.replacingOccurrences(of: ", ", with: ",")
	let lineParts = s.split(separator: ">")
	let inputIngredientParts = lineParts[0].split(separator: ",")
	let outputIngredientString = lineParts[1]

	let outputIngredientStringParts = outputIngredientString.split(separator: " ")
	let output = ChemicalIngredient(
		chemical: String(outputIngredientStringParts[1]),
		amount: Int(outputIngredientStringParts[0])!)

	var r = Reaction(input: [], output: output)

	for iip in inputIngredientParts {
		let iiStringParts = iip.split(separator: " ")
		let ii = ChemicalIngredient(
			chemical: String(iiStringParts[1]),
			amount: Int(iiStringParts[0])!)
		r.input += [ii]
	}

	allReactions += [r]
}

// ----------------------------------------------------------------------

let debug = false
var warehouse = [String:Int]()
var ore_per_unit = [String:Double]()
ore_per_unit["ORE"] = 1

func findR(_ name: String) -> Reaction? {
	for r in allReactions {
		if r.output.chemical == name {
			return r
		}
	}
	return nil
}

func debug(_ s: String) {
	if debug {
		print(s)
	}
}

func setPrice(_ r: Reaction) {
	var price: Double = 0

	if ore_per_unit[r.output.chemical] != nil {
		// already known
		return
	}

	//print("sp r=\(r)")

	for input in r.input {
		if let opu = ore_per_unit[input.chemical] {
			price += opu * Double(input.amount) / Double(r.output.amount)
		} else {
			print("BUG: setPrice() with unknown input. should not happen.")
			exit(1)
		}
	}

	//ore_per_unit[output.chemical] = Double(input.amount) / Double(output.amount) * ore_per_unit[input.chemical]!
	ore_per_unit[r.output.chemical] = price
	print("price(\(r.output.chemical)(1)) = (\(ore_per_unit[r.output.chemical]!))")
}

func runReaction(_ r: Reaction, depth: Int = 0) -> Int {
	var oreCount = 0
	let indent = String(repeating: " ", count: depth * 3)

	debug("\(indent)producing \(r.output.chemical)(\(r.output.amount))")

	for ingredient in r.input {
		if ingredient.chemical == "ORE" {
			debug("\(indent)>>> used \(ingredient.amount) ORE")
			setPrice(r)
			return ingredient.amount
		}

		debug("\(indent)... NEED \(ingredient.chemical)(\(ingredient.amount))")
		var have = warehouse[ingredient.chemical] ?? 0
		debug("\(indent)... warehouse has \(have)")

		while have < ingredient.amount {
			let nextR = findR(ingredient.chemical)!
			debug("\(indent)... run reaction for " +
				"\(nextR.output.chemical)(\(nextR.output.amount))")
			oreCount += runReaction(nextR, depth: depth + 1)

			have += nextR.output.amount
			debug("\(indent)... now have \(have) of \(nextR.output.chemical)")
		}

		warehouse[ingredient.chemical] = have - ingredient.amount
	}
	setPrice(r)

	return oreCount
}

var root = findR("FUEL")!

let ore_count = runReaction(root)

print()
for (k, v) in warehouse {
	print("leftover: \(k)(\(v))")
}

print()

print("ORE per (first!) FUEL:      \(ore_count)")
print("FUEL per ORE:               \(ore_per_unit["FUEL"]!)")
print("FUEL per 1000000000000 ORE: \(Int(trunc(1000000000000 / ore_per_unit["FUEL"]!)))")
print()
print("// NOTE // Apparently due to some floating point blurring, this number may")
print("           be higher than the actual result. Try one (1) less than given here!")

