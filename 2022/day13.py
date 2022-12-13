from functools import cmp_to_key
from tools.aoc import AOCDay
from typing import Any

ORDER_RIGHT = 1
ORDER_WRONG = -1
ORDER_UNKNOWN = 0

def parse(input, group_in_pairs: bool):
	pairs = []

	while len(input) > 0:
		s1 = input.pop(0)
		if s1 == "": continue
		pairs += [[eval(s1), eval(input.pop(0))]]

	if group_in_pairs:
		return pairs
	else:
		packets = [p[0] for p in pairs]
		packets += [p[1] for p in pairs]
		return packets

def right_order(pair_list):
	sum_right_index = 0

	# the first value is called left and the second value is called right
	for index, (left, right) in enumerate(pair_list):
		#print(f">>> Compare {left} vs {right}")
		if packet_pair_order(left, right) == ORDER_RIGHT:
			#print("... right order!")
			sum_right_index += index + 1

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
		return packet_pair_order(left, right)
	elif type(right) is int:
		right = [right]
		return packet_pair_order(left, right)

	# if control reaches here, both values are lists
	assert(type(left) is list and type(right) is list)

	# we're gonna pop() 'em, so make copies.
	left = left.copy()
	right = right.copy()

	while True:
		# If the left list runs out of items first, the inputs are in the right order.
		if 0 == len(left) < len(right):
			return ORDER_RIGHT

		# If the right list runs out of items first, the inputs are not in the right order
		if 0 == len(right) < len(left):
			return ORDER_WRONG

		# If the lists are the same length and no comparison makes a decision about the order,
		# continue checking the next part of the input.
		if 0 == len(left) == len(right):
			return ORDER_UNKNOWN

		po = packet_pair_order(left.pop(0), right.pop(0))
		if po != ORDER_UNKNOWN:
			return po

class Day(AOCDay):
	inputs = [
		[
			(13, '13-test')
			,(5806, '13')
		],
		[
			(140, '13-test')
			,(23600, '13')
		]
	]

	def part1(self) -> Any:
		pairs = parse(self.getInput(), True)
		return right_order(pairs)

	def part2(self) -> Any:
		packets = parse(self.getInput(), False)

		div1 = [[2]]
		div2 = [[6]]

		packets += [div1]
		packets += [div2]

		packets = sorted(packets, key = cmp_to_key(packet_pair_order), reverse = True)
		#print(packets)

		r  = packets.index(div1) + 1
		r *= packets.index(div2) + 1
		return r

