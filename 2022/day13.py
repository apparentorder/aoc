from functools import cmp_to_key
from tools.aoc import AOCDay
from typing import Any
import json

ORDER_RIGHT = 1
ORDER_WRONG = -1
ORDER_UNKNOWN = 0

def parse(input):
	return [json.loads(line) for line in input if line != ""]

def right_order(packets):
	sum_right_index = 0

	for i in range(len(packets) // 2):
		#print(f">>> Compare {left} vs {right}")
		if packet_pair_order(packets[i*2], packets[i*2+1]) == ORDER_RIGHT:
			#print("... right order!")
			sum_right_index += i + 1

	return sum_right_index

def packet_pair_order(left, right, depth = 0):
	# If both values are integers, the lower integer should come first.
	if type(left) is int and type(right) is int:
		#print(f"compare {left} vs {right}")

		# If the left integer is lower than the right integer, the inputs are in the right order.
		if left < right:
			return ORDER_RIGHT
		# If the left integer is higher than the right integer, the inputs are not in the right order.
		elif left > right:
			return ORDER_WRONG

		# Otherwise, the inputs are the same integer; continue checking the next part of the input.
		return ORDER_UNKNOWN

	# If exactly one value is an integer,
	# convert the integer to a list which contains that integer as its only value
	if type(left) is int:
		left = [left]
	elif type(right) is int:
		right = [right]

	# if control reaches here, both values are lists
	#assert(type(left) is list and type(right) is list)

	for i in range(min([len(left), len(right)])):
		po = packet_pair_order(left[i], right[i])
		if po != ORDER_UNKNOWN:
			return po

	# If the lists are the same length and no comparison makes a decision about the order,
	# continue checking the next part of the input.
	if len(left) == len(right):
		return ORDER_UNKNOWN

	# if control reaches here, no value decided the outcome before one list was empty

	# If the left list runs out of items first, the inputs are in the right order.
	if len(left) < len(right):
		return ORDER_RIGHT
	else:
		# If the right list runs out of items first, the inputs are not in the right order
		return ORDER_WRONG

class Day(AOCDay):
	inputs = [
		[
			(13, '13-test')
			,(6428, '13-penny')
			,(5806, '13')
		],
		[
			(140, '13-test')
			,(22464, '13-penny')
			,(23600, '13')
		]
	]

	def part1(self) -> Any:
		packets = parse(self.getInput())
		return right_order(packets)

	def part2(self) -> Any:
		packets = parse(self.getInput())

		div1 = [[2]]
		div2 = [[6]]
		packets.extend([div1, div2])

		packets.sort(key = cmp_to_key(packet_pair_order), reverse = True)
		#print(packets)

		r  = packets.index(div1) + 1
		r *= packets.index(div2) + 1
		return r

