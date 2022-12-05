# terraform apply -auto-approve -state=/dev/null -lock=false

# rps: rock paper scissors

locals {
	rps_input = trimspace(file("inputs/${local.d02_input_name}"))

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

	d02_part1 = sum([for line in split("\n", local.rps_input): local.rps_score_map_part1[line]])
	d02_part2 = sum([for line in split("\n", local.rps_input): local.rps_score_map_part2[line]])
}

locals {
	# setup
	d02_input_name = "02"
	d02_input_results = {
		"02" = [13809, 12316]
		"02-test" = [15, 12]
	}
	d02_results = local.d02_input_results[local.d02_input_name]
}

output d02_p1 {
	value = local.d02_part1
	precondition {
		condition = local.d02_part1 == local.d02_results[0]
		error_message = "wrong result"
	}
}

output d02_p2 {
	value = local.d02_part2
	precondition {
		condition = local.d02_part2 == local.d02_results[1]
		error_message = "wrong result"
	}
}

