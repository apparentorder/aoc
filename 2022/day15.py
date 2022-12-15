from tools.aoc import AOCDay
from typing import Any
import re

class Coordinate:
	def __init__(self, x, y):
		self.x = int(x) if type(x) is str else x
		self.y = int(y) if type(y) is str else y

def parse(input): # returns sensors, beacons, distances
	sensors = []
	beacons = []
	distances = []

	line_re = re.compile("Sensor at x=(\d+), y=(\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
	for line in input:
		# n.b.: assumption: all sensor coords are >= 0
		m = line_re.match(line)
		assert(m)

		sensor = Coordinate(m.group(1), m.group(2))
		beacon = Coordinate(m.group(3), m.group(4))
		mhd = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)

		sensors += [sensor]
		beacons += [beacon]
		distances += [mhd]

	return sensors, beacons, distances

def get_covered_areas_by_row(y, sensors, distances, limit = None):
	areas = []

	for i, sensor in enumerate(sensors):
		if sensor.y - distances[i] > y or sensor.y + distances[i] < y:
			continue

		distance_y = abs(sensor.y - y)
		coverage_start = sensor.x - distances[i] + distance_y
		coverage_end = sensor.x + distances[i] - distance_y
		areas += [[coverage_start, coverage_end]]

	#print(f"cov areas {areas}")

	has_merged = True
	while has_merged:
		def try_merge():
			for i in range(len(areas)):
				for ii in range(len(areas)):
					if i == ii: continue
					if areas[i][0] < areas[ii][0] <= areas[i][1] or areas[i][0] <= areas[ii][1] < areas[i][1]:
						areas[i][0] = min(areas[i][0], areas[ii][0])
						areas[i][1] = max(areas[i][1], areas[ii][1])
						del areas[ii]
						return True

			return False

		has_merged = try_merge()

	if limit:
		for i, a in enumerate(areas):
			areas[i][1] = min(a[1], limit)

	#print(f"merged areas: {areas}")
	return areas

class Day(AOCDay):
	inputs = [
		[
			(26, '15-test')
			,(5_394_423, '15')
		],
		[
			(56_000_011, '15-test')
			,(11_840_879_211_051, '15')
		]
	]

	def part1(self) -> Any:
		input = self.getInput()
		target_y = 10 if len(input) == 14 else 2_000_000

		sensors, beacons, distances = parse(input)

		areas = get_covered_areas_by_row(target_y, sensors, distances)
		count = sum(ca[1] - ca[0] + 1 for ca in areas)
		count -= len(set([pos.x for pos in sensors + beacons if pos.y == target_y]))

		return count

	def part2(self) -> Any:
		input = self.getInput()
		limit = 20 if len(input) == 14 else 4_000_000

		sensors, beacons, distances = parse(input)

		for target_y in range(limit + 1):
			areas = get_covered_areas_by_row(target_y, sensors, distances, limit)
			if len(areas) > 1:
				split = areas[0][1] if areas[0][1] != limit else areas[1][1]
				return (split + 1) * 4_000_000 + target_y

		return ""

