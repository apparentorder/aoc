from tools.aoc import AOCDay
from typing import Any

def parse(input):
	grid = []

	for line in input:
		grid += [[]]
		for c in list(line):
			grid[len(grid) - 1] += [int(c)]

	print(grid)
	return grid

def is_visible(grid, this_tree, other_trees):
	#print("this %s others %s" % (this_tree, other_trees))
	return len(other_trees) == 0 or max(other_trees) < this_tree

def visibility(grid, this_tree, other_trees):
	# returns (bool: visible from the edge?), (count of visible other trees)
	print("this %s others %s" % (this_tree, other_trees))

	count = 0

	if len(other_trees) == 0:
		return True, count

	for other_tree in other_trees:
		count +=1
		if other_tree >= this_tree:
			return False, count

	return True, count

def visicount(grid):
	count = len(grid)*4 - 4
	print("edge count %s" % (count))

	for y in range(1, len(grid) - 1):
		for x in range(1, len(grid[y]) - 1):
			sides = {
				"trees_top": [grid[_y][x] for _y in range(0, y)],
				"trees_left": [grid[y][_x] for _x in range(0, x)],
				"trees_right": [grid[y][_x] for _x in range(x+1, len(grid[y]))],
				"trees_bottom": [grid[_y][x] for _y in range(y+1, len(grid))],
			}

			tree_visible = False
			for key, trees in sides.items():
				result = is_visible(grid, grid[y][x], trees)
				#print("(%s,%s) visible through %s: %s" % (x,y, key, result))
				tree_visible = tree_visible or result

			if tree_visible:
				count += 1

	return count

def score(grid):
	scores = []

	for y in range(1, len(grid) - 1):
		for x in range(1, len(grid[y]) - 1):
			sides = {
				"trees_top": [grid[_y][x] for _y in reversed(range(0, y))],
				"trees_left": [grid[y][_x] for _x in reversed(range(0, x))],
				"trees_right": [grid[y][_x] for _x in range(x+1, len(grid[y]))],
				"trees_bottom": [grid[_y][x] for _y in range(y+1, len(grid))],
			}

			tree_score = 1
			for key, trees in sides.items():
				result = visibility(grid, grid[y][x], trees)[1]
				tree_score *= result
				print("%s from (%s,%s): %s" % (key, x,y, result))

			print("(%s,%s) score %s" % (x,y, tree_score))
			scores += [tree_score]

	return max(scores)

class Day(AOCDay):
	inputs = [
		[
			(21, '08-test')
			,(1854, '08')
		],
		[
			(8, '08-test')
			,(None, '08')
		]
	]

	def part1(self) -> Any:
		grid = parse(self.getInput())
		return visicount(grid)

	def part2(self) -> Any:
		grid = parse(self.getInput())
		return score(grid)

