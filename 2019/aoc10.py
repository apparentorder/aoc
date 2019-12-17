#!/usr/bin/env python

import math

fn = "aoc10in"
f = open(fn)

mapdata = list(f)
f.close()

rows = len(mapdata)
columns = len(mapdata[0])

asteroids = []

class Coordinates:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "(%d,%d)" % (self.x, self.y)

	def iszero(self):
		return (self.x == 0 and self.y == 0)

class Asteroid:
	def __init__(self, x, y):
		self.coord = Coordinates(x, y)
		self.other_angles = {}

	def __str__(self):
		return str(self.coord)

	def get_path(self, other):
		path = Coordinates(other.coord.x - self.coord.x,
			other.coord.y - self.coord.y)

		return path

	def register_other(self, other):
		# for each potential station (on an asteroid),
		# figure out in which *directions* objects can be
		# seen
		# we do not care about objects being blocked, because
		# all objects in the exact same direction count as 1
		# (i.e. additionally blocked asteroids don't count extra)
		#
		# thank you so much, internet.
		# https://stackoverflow.com/questions/21483999/using-atan2-to-find-angle-between-two-vectors
		# we invert the y-axis there so that 0 points "up" (as
		# required for part2) and 2*pi is a full clockwise turn.

		path = self.get_path(other)

		if path.iszero():
			# watching myself?
			return

		angle = math.atan2(path.x, -1*path.y)
		if angle < 0:
			angle += 2*math.pi

		if angle not in self.other_angles.keys():
			self.other_angles[angle] = []

		self.other_angles[angle].append(other)
		#print("registered %s at %s" % (other, self))

for r in range(0, rows):
	for c in range(0, columns):
		if mapdata[r][c] == "#":
			asteroids.append(Asteroid(c, r))

max_others = 0
best_station = None

for station in asteroids:
	for other in asteroids:
		station.register_other(other)

	others = len(station.other_angles.keys())
	#print("station %s => (%d objects)"
	#	% (station, others))

	if others > max_others:
		max_others = others
		best_station = station

print("best is station %s with %d objects in sight" % (best_station, max_others))

vaporized = 0
while len(best_station.other_angles.keys()):
	angles_sorted = sorted(best_station.other_angles.keys())
	for a in angles_sorted:
		min_distance = 999999999
		closest = None
		for other in best_station.other_angles[a]:
			p = best_station.get_path(other)
			distance = abs(p.x) + abs(p.y)

			if distance < min_distance:
				min_distance = distance
				closest = other

		vaporized += 1
		print("[%03d] angle %s vaporizing %s" % (vaporized, a, closest))
		best_station.other_angles[a].remove(closest)

		if len(best_station.other_angles[a]) == 0:
			del best_station.other_angles[a]

