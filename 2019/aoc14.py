#!/usr/bin/env python

import math
from decimal import *

infile = "aoc14in"

class Reaction:
	def __init__(self, input, output):
		self.input = []
		self.output = output

class ChemicalIngredient:
	def __init__(self, chemical, amount):
		self.chemical = chemical
		self.amount = amount

allReactions = []

getcontext().prec = 50

# -----
# parse input

f = open(infile)
for s in f:
	lineParts = s.split(" => ")
	inputIngredientParts = lineParts[0].split(", ")
	outputIngredientString = lineParts[1]

	outputIngredientStringParts = outputIngredientString.split()
	output = ChemicalIngredient(
		chemical = outputIngredientStringParts[1],
                amount = int(outputIngredientStringParts[0]))

	r = Reaction(input = [], output = output)

	for iip in inputIngredientParts:
		iiStringParts = iip.split()
		ii = ChemicalIngredient(
			chemical = iiStringParts[1],
			amount = int(iiStringParts[0]))
		r.input += [ii]

	allReactions += [r]

# -------

debug_enabled = False
warehouse = {}
ore_per_unit = {}
ore_per_unit["ORE"] = 1

def findR(name):
	for r in allReactions:
		if r.output.chemical == name:
			return r

	return None

def debug(s):
	if debug_enabled:
		print(s)

def setPrice(r):
	price = Decimal(0)

	if r.output.chemical in ore_per_unit.keys():
		return #already known

	for input in r.input:
		price += Decimal(ore_per_unit[input.chemical]) * Decimal(input.amount) / Decimal(r.output.amount)

	ore_per_unit[r.output.chemical] = Decimal(price)
	print("price %s(1) = %s" % (r.output.chemical, ore_per_unit[r.output.chemical]))

def runReaction(r, depth = 0):
	oreCount = 0
	indent = " " * depth * 3

	for ingredient in r.input:
		if ingredient.chemical == "ORE":
			setPrice(r)
			return ingredient.amount

		have = warehouse.get(ingredient.chemical, 0)

		while have < ingredient.amount:
			nextR = findR(ingredient.chemical)
			oreCount += runReaction(nextR, depth + 1)
			have += nextR.output.amount

		warehouse[ingredient.chemical] = have - ingredient.amount

	setPrice(r)

	return oreCount

root = findR("FUEL")
ore_count = runReaction(root)

print("")
for k in warehouse:
	print("leftover: %s(%d)" % (k, warehouse[k]))

print("")

print("ORE per (first!) FUEL:      %d" % ore_count)
print("FUEL per ORE:               %s" % ore_per_unit["FUEL"])
print("FUEL per 1000000000000 ORE: %s" % (Decimal(1000000000000) / ore_per_unit["FUEL"]))

