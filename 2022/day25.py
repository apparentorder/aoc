from tools.aoc import AOCDay
from tools.grid import Grid
from tools.coordinate import Coordinate
from typing import Any
import json
import re

def desnafu(line):
	n = 0
	snafu = list(line)

	for i in reversed(range(len(snafu))):
		pos = len(snafu) - 1 - i
		if snafu[pos].isnumeric():
			d = int(snafu[pos])
		elif snafu[pos] == "-":
			d = -1
		else:
			d = -2

		n += d*(5**i)

	return n

def snafu(n):
	s = ""
	number = n

	i = 1
	add_next = False
	while number > 0 or add_next:
		remainder = number%(5**i)
		number -= remainder
		digit = remainder//(5**(i-1))

		if add_next:
			digit = (digit + 1) % 5
			add_next = (digit == 0) # additional add_next when wrapped around

		if digit == 3:
			c = "="
			add_next = True
		elif digit == 4:
			c = "-"
			add_next = True
		else:
			c = str(digit)

		i += 1
		s = c + s

	return s

class Day(AOCDay):
	inputs = [
		[
			("2=-1=0", '25-test')
			,("2=--00--0220-0-21==1", '25')
		],
		[
			(None, '25-test')
			,(None, '25')
		]
	]

	def part1(self) -> Any:
		supply_sum = sum([desnafu(line) for line in self.getInput()])
		return snafu(supply_sum)

	def part2(self) -> Any:
		return None

