locals {
	d04_input = split("\n", trimspace(file("inputs/${local.d04_input_name}")))

	# list of list of "char" (single-byte strings)
	d04_pairs = [
		for line in local.d04_input: [
			for pair in split(",", line):
			[for n in split("-", pair): tonumber(n)]
		]
	]

	d04_part1 = sum([
		for pair in local.d04_pairs: 1
		if (pair[1][0] >= pair[0][0] && pair[1][1] <= pair[0][1])
		|| (pair[0][0] >= pair[1][0] && pair[0][1] <= pair[1][1])
	])

	d04_part2 = sum([
		for pair in local.d04_pairs: 1
		if (pair[0][1] >= pair[1][0] && pair[0][1] <= pair[1][1])
		|| (pair[1][1] >= pair[0][0] && pair[1][1] <= pair[0][1])
	])
}

locals {
	# setup
	d04_input_name = "04"
	d04_input_results = {
		"04" = [538, 792]
		"04-test" = [2, 4]
	}
	d04_results = local.d04_input_results[local.d04_input_name]
}

output d04_p1 {
	value = local.d04_part1
	precondition {
		condition = local.d04_part1 == local.d04_results[0]
		error_message = "wrong result"
	}
}

output d04_p2 {
	value = local.d04_part2
	precondition {
		condition = local.d04_part2 == local.d04_results[1]
		error_message = "wrong result"
	}
}

