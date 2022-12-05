locals {
	d05_input = split("\n", trim(file("inputs/${local.d05_input_name}"), "\n\r"))

	d05_input_split_index = index(local.d05_input, "")
	d05_input_map = slice(local.d05_input, 0, local.d05_input_split_index - 1) # skip last line
	d05_input_moves = slice(local.d05_input, local.d05_input_split_index + 1, length(local.d05_input) - 1)

	d05_stack_count = (length(local.d05_input_map[0]) - 2) / 4
	d05_stacks = [
		for i_stack in range(local.d05_stack_count): [
			for i_line in range(length(local.d05_input_map)):
			element(split("", local.d05_input_map[i_line]), i_stack*4 + 1)
			if element(split("", local.d05_input_map[i_line]), i_stack*4 + 1) != " "
		]
	]

	d05_moves = {
		move_from = [for line in local.d05_input_moves: tonumber(split(" ", line)[3])]
		move_to = [for line in local.d05_input_moves: tonumber(split(" ", line)[5])]
		move_count = [for line in local.d05_input_moves: tonumber(split(" ", line)[1])]
	}

	# now what?

	d05_part1 = null
	d05_part2 = null
}

#output d05_debug {
#	value = local.d05_stacks
#}

locals {
	# setup
	d05_input_name = "05-test"
	d05_input_results = {
		"05" = [538, 792]
		#"05-test" = [2, 4]
		"05-test" = [null, null]
	}
	d05_results = local.d05_input_results[local.d05_input_name]
}

output d05_p1 {
	value = local.d05_part1
	precondition {
		condition = local.d05_part1 == local.d05_results[0]
		error_message = "wrong result"
	}
}

output d05_p2 {
	value = local.d05_part2
	precondition {
		condition = local.d05_part2 == local.d05_results[1]
		error_message = "wrong result"
	}
}

