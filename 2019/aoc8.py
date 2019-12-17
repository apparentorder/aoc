#!/usr/bin/env python

import sys

f = open("aoc8in")
imagedata = f.read().strip()
width = 25
height = 6

#imagedata = '0222112222120000'
#width = 2
#height = 2

layercount = len(imagedata) / (width * height)

image = [[[None for _ in range(width)] for _ in range(height)] for _ in range(layercount)]
stackedimage = [[2 for _ in range(width)] for _ in range(height)]

layerstats = [{0: 0, 1: 0, 2: 0} for _ in range(layercount)]

for layer in range(0, len(image)):
	for row in range(0, height):
		for column in range(0, width):
			pixel = int(imagedata[(layer * width * height) + row * width + column])

			if pixel in layerstats[layer]:
				layerstats[layer][pixel] += 1
			else:
				layerstats[layer][pixel] = 1

			image[layer][row][column] = pixel
			if stackedimage[row][column] == 2:
				stackedimage[row][column] = pixel

for row in range(0, height):
	for column in range(0, width):
		if stackedimage[row][column] == 1:
			sys.stdout.write("1")
		else:
			sys.stdout.write(" ")

	sys.stdout.write("\n")

exit(1)

for layer in range(0, len(image)):
	print("layer %d 0-count %d checksum %d" %
		(layer, layerstats[layer][0], layerstats[layer][1] * layerstats[layer][2]))

