#!/usr/bin/env python

# rekursiv geht schief!

poi_routes = {}

def traverse_map(relations, start, path_in, search_poi = None):
	global poi_routes

	links = 0

	path = list(path_in)

	# n.b.: we determine this object's depth
	# before appending to the path
	depth = len(path_in)

	path.append(start)

	for r in relations:
		if r["center"] == start:
			links += traverse_map(relations,
				r["satellite"],
				path,
				search_poi)

	if search_poi == None or search_poi == start:
		if search_poi == start:
			# if we're looking for a POI, then save the path
			# for later
			poi_routes[search_poi] = path

		print("path %s depth %d links %d" % ("-".join(path), depth, links))
		return links + depth
	else:
		return links

def main():
	relations = []

	f = open("aoc6in")
	#f = open("aoc6in-sample")
	for line in f:
		x = line.strip().split(')')
		relation = {
			'center': x[0],
			'satellite': x[1]
		}
		relations.append(relation)

	f.close()

	# p1
	#x = traverse_map(relations, "COM", [])
	#print("total: %d" % x)

	# p2
	traverse_map(relations, "COM", [], "YOU")
	traverse_map(relations, "COM", [], "SAN")

	# find the longest path that's shared by YOU and
	# SANta, then add the distances from there
	last_common_orbit = "COM"
	for orbit in range(0, len(poi_routes["YOU"])):
		if poi_routes["YOU"][orbit] != poi_routes["SAN"][orbit]:
			# paths diverge, so we found our common part
			break

		last_common_orbit = poi_routes["YOU"][orbit]

	# find distances and substract 1 (do not count the final orbit of YOU/SAN)
	distance_you = traverse_map(relations, last_common_orbit, [], "YOU")
	distance_you -= 1

	distance_san = traverse_map(relations, last_common_orbit, [], "SAN")
	distance_san -= 1

	distance = distance_you + distance_san

	print("distance %s <-> {you, san} = {%d, %d} = %d"
		% (last_common_orbit, distance_you, distance_san, distance))

main()

