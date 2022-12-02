# terraform apply -auto-approve -state=/dev/null -lock=false

# rps: rock paper scissors

locals {
	#rps_input = trimspace(file("inputs/02-test"))
	rps_input = trimspace(file("inputs/02"))

	rps_score_map_part1 = {
		# A|X Rock
		# B|Y Paper
		# C|Z Scissors
		# note: first column = first; second column = self
		"A X" = 1 + 3 # same
		"B Y" = 2 + 3 # same
		"C Z" = 3 + 3 # same
		"C X" = 1 + 6 # Rock defeats Scissors
		"A Y" = 2 + 6 # Paper defeats Rock
		"B Z" = 3 + 6 # Scissors defeats Paper
		"B X" = 1 + 0 # defeat
		"C Y" = 2 + 0 # defeat
		"A Z" = 3 + 0 # defeat
	}

	rps_score_map_part2 = {
		# A|X Rock
		# B|Y Paper
		# C|Z Scissors
		# X=lose Y=draw Z=win
		# note: first column = first; second column = self
		"A X" = 3 + 0
		"A Y" = 1 + 3
		"A Z" = 2 + 6
		"B X" = 1 + 0
		"B Y" = 2 + 3
		"B Z" = 3 + 6
		"C X" = 2 + 0
		"C Y" = 3 + 3
		"C Z" = 1 + 6
	}

	rps_score_part1 = sum([for line in split("\n", local.rps_input): local.rps_score_map_part1[line]])
	rps_score_part2 = sum([for line in split("\n", local.rps_input): local.rps_score_map_part2[line]])
}

output day02_p1 {
	value = local.rps_score_part1
}

output day02_p2 {
	value = local.rps_score_part2
}

