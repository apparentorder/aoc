from tools.aoc import AOCDay
from typing import Any

def tailposn(input, knot_count):
	knots = [[0,0] for _ in range(knot_count)]
	tailpos = []

	for line in input:
		dir, count = line.split()
		count = int(count)

		#print(line)
		for _ in range(count):
			match dir:
				case "U":
					knots[0][0] -= 1
				case "D":
					knots[0][0] += 1
				case "L":
					knots[0][1] -= 1
				case "R":
					knots[0][1] += 1
				case _:
					raise Exception("invalid direction %s" % (dir))

			for knot in range(1, knot_count):
				delta_x = knots[knot][1] - knots[knot - 1][1]
				delta_y = knots[knot][0] - knots[knot - 1][0]

				# if     abs(delta)==2, use //2 to move just one step, preserving direction (delta's sign)
				# if not abs(delta)==2, then delta will always be in [-1, 0, +1].
				if abs(delta_x) == 2 and abs(delta_y) == 2:
					knots[knot][1] -= delta_x//2
					knots[knot][0] -= delta_y//2
				elif abs(delta_x) == 2:
					knots[knot][1] -= delta_x//2
					knots[knot][0] -= delta_y
				elif abs(delta_y) == 2:
					knots[knot][1] -= delta_x
					knots[knot][0] -= delta_y//2

			tailpos.append(list(knots[knot_count - 1]))
			#print("new pos %s" % (knots))

	return len(set(str(e) for e in tailpos))

class Day(AOCDay):
	inputs = [
		[
			(13, '09-test')
			,(6212, '09')
		],
		[
			(1, '09-test')
			,(36, '09-test-p2')
			,(2522, '09')
		]
	]

	def part1(self) -> Any:
		return tailposn(self.getInput(), 2)

	def part2(self) -> Any:
		return tailposn(self.getInput(), 10)

