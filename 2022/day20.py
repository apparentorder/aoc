from tools.aoc import AOCDay
from typing import Any
import json
import re

def parse(input, multiply = 1):
	return [int(line)*multiply for line in input]

def mix(nums, times = 1):
	# nums are not unique, so we maintain a second list with the
	# original list indexes. this list is mixed exactly like the
	# nums list, so we can look up the original order using nums_index.index().

	nums_index = list(range(len(nums)))

	for _ in range(times):
		for index_value in range(len(nums)):
			index_old = nums_index.index(index_value)

			value = nums[index_old]

			del nums_index[index_old]
			del nums[index_old]

			# note: we need to mod around the length of the list
			# *without* the original value, or else things will be
			# fucked once the value would move moved "over" its original
			# position. this is why the test input usually works but
			# the actual input does not.
			index_new = (index_old + value) % len(nums)

			nums.insert(index_new, value)
			nums_index.insert(index_new, index_value)

			#print(f" after move of {value}: {nums}")

	return nums

class Day(AOCDay):
	inputs = [
		[
			(3, '20-test')
			,(10763, '20-penny')
			,(13967, '20')
		],
		[
			(1_623_178_306, '20-test')
			,(4_979_911_042_808, '20-penny')
			,(1_790_365_671_518, '20')
		]
	]

	def part1(self) -> Any:
		nums = parse(self.getInput())
		mix(nums)
		x1 = nums[(nums.index(0) + 1000) % len(nums)]
		x2 = nums[(nums.index(0) + 2000) % len(nums)]
		x3 = nums[(nums.index(0) + 3000) % len(nums)]

		#print(f"x1000 = {x1}, x2000 = {x2}, x3000 = {x3}")
		# make sure the test returns exactly the three specified values
		assert(len(nums) > 10 or [x1,x2,x3] == [4, -3, 2])

		return sum([x1, x2, x3])

	def part2(self) -> Any:
		nums = parse(self.getInput(), multiply = 811589153)
		mix(nums, times = 10)

		x1 = nums[(nums.index(0) + 1000) % len(nums)]
		x2 = nums[(nums.index(0) + 2000) % len(nums)]
		x3 = nums[(nums.index(0) + 3000) % len(nums)]
		#print(f"x1000 = {x1}, x2000 = {x2}, x3000 = {x3}")
		# make sure the test returns exactly the three specified values
		assert(len(nums) > 10 or [x1,x2,x3] == [811589153,2434767459,-1623178306])

		return sum([x1, x2, x3])

