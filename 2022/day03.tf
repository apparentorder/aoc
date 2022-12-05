# terraform apply -auto-approve -state=/dev/null -lock=false

# rucksack: Rucksack Reorganization

locals {
	d03_input = split("\n", trimspace(file("inputs/${local.d03_input_name}")))

	# part 1
	# list of list of "char" (single-byte strings)
	d03_compartments = [for line in local.d03_input: chunklist(split("", line), length(line)/2)]
	d03_compartments_intersections = [for comp in local.d03_compartments: setintersection(comp[0], comp[1])]
	d03_part1 = sum([for char in flatten(local.d03_compartments_intersections): parseint(char, 62) - 9])

	# part 2
	d03_groups = chunklist(local.d03_input, 3)
	d03_group_compartments = [for group in local.d03_groups: [for chunk_item in group: split("", chunk_item)]]
	d03_group_intersections = [for comp in local.d03_group_compartments: setintersection(comp[0], comp[1], comp[2])]
	d03_part2 = sum([for char in flatten(local.d03_group_intersections): parseint(char, 62) - 9])
}

locals {
	# setup
	d03_input_name = "03"
	d03_input_results = {
		"03" = [7742, 2276]
		"03-test" = [157, 70]
	}
	d03_results = local.d03_input_results[local.d03_input_name]
}

output d03_p1 {
	value = local.d03_part1
	precondition {
		condition = local.d03_part1 == local.d03_results[0]
		error_message = "wrong result"
	}
}

output d03_p2 {
	value = local.d03_part2
	precondition {
		condition = local.d03_part2 == local.d03_results[1]
		error_message = "wrong result"
	}
}

