from tools.aoc import AOCDay
from typing import Any, NamedTuple

class TileCoord(NamedTuple):
	x: int
	y: int

class Day(AOCDay):
	def part1(self) -> Any:
		tile_list = self.parse_input()

		return max(
			(abs(t1.x - t2.x) + 1) *
			(abs(t1.y - t2.y) + 1)
			for i1, t1 in enumerate(tile_list)
			for t2 in tile_list[i1+1:]
		)

	def part2(self) -> Any:
		"""
		strategy:
		- create a list of lines which define the loop of red and green tiles by
		  walking the input list
		- start with the top-left tile, as we know outside and inside for this tile
		- for every red tile, mark every *diagonally* adjacent which points to the
		  outside (aka, neither red nor green tile) [see picture, "@" marks outside]
		- for each candidate rectangle (for each red tile pair), check that:
		  * no "outside" marker is *in* this rectangle (markers touching the border
		    are ok) -- this makes sure the rectangle is inside the loop
		  * no loop line runs through this rectangle (again, touching the border is ok)

                     @     @
                      #XXX#
                @    @X   X
                 #XXXX#   X
                 X        X
                 #XXXXXX# X
                @      @X X
                        #X#
                       @   @
		"""
		tile_list = self.parse_input()
		outside_list = []
		loop_line_list = []

		# walk the line 🎶
		for i in range(len(tile_list) + 1):
			tile = tile_list[i % len(tile_list)]
			next_tile = tile_list[(i + 1) % len(tile_list)]
			loop_line_list += [(
				(min(tile.x, next_tile.x), max(tile.x, next_tile.x)),
				(min(tile.y, next_tile.y), max(tile.y, next_tile.y)),
			)]

		# start with the top-left tile, and mark the position to the top-left of it as outside
		i = min(range(len(tile_list)), key = lambda ti: (tile_list[ti].x, tile_list[ti].y))
		current = top_left = tile_list[i]
		outside_list += [TileCoord(current.x - 1, current.y - 1)]

		# walk the line again (this could be combined with the first walk)
		while True:
			i = (i + 1) % len(tile_list)
			i_next = (i + 1) % len(tile_list)
			current = tile_list[i]
			next = tile_list[i_next]
			outside_prev = outside_list[-1]

			if current == top_left:
				break

			# using the previous outside marker as orientation, find and mark
			# this tile's outside position
			if current.x == next.x:
				# next move is vertical
				if next.y >= outside_prev.y:
					outside_list += [TileCoord(current.x + 1, outside_prev.y)]
				elif next.y <= outside_prev.y:
					outside_list += [TileCoord(current.x - 1, outside_prev.y)]
			else:
				# next move is horizontal
				if next.x >= outside_prev.x:
					outside_list += [TileCoord(outside_prev.x, current.y - 1)]
				elif next.x <= outside_prev.x:
					outside_list += [TileCoord(outside_prev.x, current.y + 1)]

		def check_rect(t1: TileCoord, t2: TileCoord):
			xmin = min(t1.x, t2.x)
			xmax = max(t1.x, t2.x)
			ymin = min(t1.y, t2.y)
			ymax = max(t1.y, t2.y)

			for outside in outside_list:
				if xmin < outside.x < xmax and ymin < outside.y < ymax:
					return False

			for ((x_start, x_end), (y_start, y_end)) in loop_line_list:
				if (
					x_start < xmax and x_end > xmin and
					y_start < ymax and y_end > ymin
				): return False

			return True

		return max(
			(abs(t1.x - t2.x) + 1) *
			(abs(t1.y - t2.y) + 1)
			for i1, t1 in enumerate(tile_list)
			for t2 in tile_list[i1+1:]
			if check_rect(t1, t2)
		)

	def parse_input(self) -> list[TileCoord]:
		return [
			TileCoord(*tuple(map(int, line.split(","))))
			for line in self.getInput()
		]

	inputs = [
		[
			(50, "input9-test"),
			# (997, "input9-penny"),
			(4745816424, "input9"),
		],
		[
			(24, "input9-test"),
			# (5978, "input9-penny"),
			(1351617690, "input9"),
		]
	]

if __name__ == '__main__':
	day = Day(2025, 9)
	day.run(verbose=True)
