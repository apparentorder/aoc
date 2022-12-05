# terraform apply -auto-approve -state=/dev/null -lock=false

locals {
	day01_input = file("inputs/${local.d01_input_name}")

	calory_list_by_elf_string = split("\n\n", local.day01_input)
	calory_list_by_elf_int = [
		for calory_list in local.calory_list_by_elf_string: [
			for calory_string in split("\n", calory_list):
			tonumber(calory_string)
			if calory_string != ""
		]
	]

	# terraform sort() always works on and returns strings! needs a little detour...
	calory_sum_by_elf = [for list in local.calory_list_by_elf_int: format("%09d", sum(list))]
	calory_sum_by_elf_desc = [
		for string in reverse(sort(local.calory_sum_by_elf)):
		tonumber(string)
	]

	d01_part1 = sum(slice(local.calory_sum_by_elf_desc, 0, 1))
	d01_part2 = sum(slice(local.calory_sum_by_elf_desc, 0, 3))
}

locals {
	# setup
	d01_input_name = "01"
	d01_input_results = {
		"01" = [72070, 211805]
		"01-test" = [24000, 45000]
	}
	d01_results = local.d01_input_results[local.d01_input_name]
}

output d01_p1 {
	value = local.d01_part1
	precondition {
		condition = local.d01_part1 == local.d01_results[0]
		error_message = "wrong result"
	}
}

output d01_p2 {
	value = local.d01_part2
	precondition {
		condition = local.d01_part2 == local.d01_results[1]
		error_message = "wrong result"
	}
}

