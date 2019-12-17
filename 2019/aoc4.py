#!/usr/bin/env python

pwmin = 273025
pwmax = 767253

def fixup_increase(pw):
	out = list(map(int, str(pw)))

	min_digit = 0
	fill = False
	for i in range(0, len(out)):
		if fill or out[i] < min_digit:
			out[i] = min_digit
			fill = True
		else:
			min_digit = int(out[i])

	outstr = "".join(map(str, out))

	return int(outstr)

def check_adjacent_p1(pw):
	prev = "x"
	for digit in str(pw):
		if prev == digit:
			return True

		prev = digit

	return False

def check_adjacent_p2(pw):
	s = str(pw)

	prev = "x"
	consecutive = 0
	for digit in str(pw):
		if digit == prev:
			consecutive += 1
		else:
			if consecutive == 2:
				# consecutive row breaks, but
				# we've seen exactly two matching
				# digits
				return True
			else:
				# consecutive row breaks, restarting
				# counting at 1
				consecutive = 1

		prev = digit

	if consecutive == 2:
		# we need to check again here, in case those
		# were the last two digits
		return True

	return False

pw = fixup_increase(pwmin)
count = 0

while pw <= pwmax:
	if check_adjacent_p2(pw):
		print("candidate password: %d" % pw)
		count += 1

	pw = fixup_increase(pw + 1)

print("candidate passwords: %d" % count)
