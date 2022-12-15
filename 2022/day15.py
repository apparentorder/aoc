from tools.grid import Grid
from tools.coordinate import Coordinate, DistanceAlgorithm
from tools.aoc import AOCDay
from typing import Any
import re

def cfromstr(s1, s2):
	i1, i2 = int(s1), int(s2)
	return Coordinate(i1, i2)

def parse(input): # returns map, sensors, beacons, distances
	map = Grid(".")
	sensors = []
	beacons = []
	distances = []

	for line in input:
		m = re.match("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
		assert(m)

		sensor = cfromstr(m.group(1), m.group(2))
		beacon = cfromstr(m.group(3), m.group(4))
		mhd = sensor.getDistanceTo(beacon, DistanceAlgorithm.MANHATTAN)

		sensors += [sensor]
		beacons += [beacon]
		distances += [mhd]

		map.set(sensor, "S")
		map.set(beacon, "B")

	print(distances)
	return map, sensors, beacons, distances

def mark_unknowns(map, sensors, beacons, distances):
	for i, s in enumerate(sensors):
		#if s != Coordinate(8,7):
		#	continue
		for x in range(s.x - distances[i], s.x + distances[i] + 1):
			for y in range(s.y - distances[i], s.y + distances[i] + 1):
				candidate = Coordinate(x, y)
				if map.get(candidate) != ".":
					continue
				if candidate.getDistanceTo(s, DistanceAlgorithm.MANHATTAN) <= distances[i]:
					map.set(candidate, "#")

def get_unknowns(map, y, sensors, distances):
	r = 0

	print(f"range {map.rangeX()}")
	for x in range(map.minX - max(distances), map.maxX + max(distances)):
		checkpos = Coordinate(x, y)
		#print(f"x{x} y{y} checkpos {checkpos}")
		if map.get(checkpos) != ".":
			print(f"skip {checkpos} is {map.get(checkpos)}")
			continue

		for i, sensor in enumerate(sensors):
			#print(f"check sensor {sensor} distance {distances[i]}")
			if sensor.getDistanceTo(checkpos, DistanceAlgorithm.MANHATTAN) <= distances[i]:
				# checkpos is within range of a sensor
				#print(f"isnt {checkpos}")
				r += 1
				break
		else:
			pass
			#print(f"unknown {checkpos}")

	return r

def pos_unknown(map, sensors, distances, checkpos):
	for i, sensor in enumerate(sensors):
		#print(f"check sensor {sensor} distance {distances[i]}")
		if sensor.getDistanceTo(checkpos, DistanceAlgorithm.MANHATTAN) <= distances[i]:
			# checkpos is within range of a sensor, so it's known
			return False

	return True

def get_free(map, limit, sensors, distances):
	for si, sensor in enumerate(sensors):
		check_distance = distances[si] + 1

		print(f"range {range(sensor.x - check_distance, sensor.x + check_distance + 1)}")
		for x in range(sensor.x - check_distance, sensor.x + check_distance + 1):
			distance_x = check_distance - abs(sensor.x - x)
			for y in [sensor.y - distance_x, sensor.y + distance_x]:
				if not (0<=x<=limit and 0<=y<=limit):
					continue
				checkpos = Coordinate(x,y)
				#print(f"check pos {checkpos} sensor {sensor} distance {distances[si]}")
				if map.get(checkpos) == ".":
					if pos_unknown(map, sensors, distances, checkpos):
						return checkpos

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

		map, sensors, beacons, distances = parse(input)
		if False and target_y == 10:
			mark_unknowns(map, sensors, beacons, distances)
			map.print()

		return get_unknowns(map, target_y, sensors, distances)
		#map.print()
		#unknowns = [map.get(Coordinate(x, 10)) for x in map.rangeX()]

	def part2(self) -> Any:
		input = self.getInput()
		limit = 20 if len(input) == 14 else 4_000_000

		map, sensors, beacons, distances = parse(input)
		if False and target_y == 10:
			mark_unknowns(map, sensors, beacons, distances)
			map.print()

		free = get_free(map, limit, sensors, distances)
		print(f"free {free}")
		return free.x * 4_000_000 + free.y
		#map.print()
		#unknowns = [map.get(Coordinate(x, 10)) for x in map.rangeX()]

