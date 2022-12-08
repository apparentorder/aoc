from tools.aoc import AOCDay
from typing import Any

def parse(input):
	return [list(map(int, line)) for line in input]

def visibility(grid, this_tree, other_trees) -> (bool, int):
	# returns (bool: visible from the edge?), (count of visible other trees)

	#print("this %s others %s" % (this_tree, other_trees))
	count = 0

	for other_tree in other_trees:
		count +=1
		if other_tree >= this_tree:
			return False, count

	return True, count

def treehouse(grid) -> (int, int):
	# returns (part1: count of trees visible from edge), (part2: max scenic score)

	count = len(grid)*4 - 4
	scores = []

	for y in range(1, len(grid) - 1):
		for x in range(1, len(grid[y]) - 1):
			sides = {
				"trees_top":    [grid[_y][x] for _y in reversed(range(0, y))],
				"trees_left":   [grid[y][_x] for _x in reversed(range(0, x))],
				"trees_right":  [grid[y][_x] for _x in range(x+1, len(grid[y]))],
				"trees_bottom": [grid[_y][x] for _y in range(y+1, len(grid))],
			}

			tree_score = 1
			tree_visible = False
			for key, trees in sides.items():
				result = visibility(grid, grid[y][x], trees)
				tree_visible = tree_visible or result[0]
				tree_score *= result[1]

			count += 1 if tree_visible else 0
			scores += [tree_score]

	return count, max(scores)

class Day(AOCDay):
	inputs = [
		[
			(21, '08-test')
			,(1854, '08')
		],
		[
			(8, '08-test')
			,(527340, '08')
		]
	]

	def part1(self) -> Any:
		grid = parse(self.getInput())
		return treehouse(grid)[0]

	def part2(self) -> Any:
		grid = parse(self.getInput())
		return treehouse(grid)[1]

