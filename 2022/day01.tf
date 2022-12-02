# terraform apply -auto-approve -state=/dev/null -lock=false

locals {
	#input = file("inputs/01-test")
	input = file("inputs/01")

	calory_list_by_elf_string = split("\n\n", local.input)
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
}

output day01_p1 {
	value = sum(slice(local.calory_sum_by_elf_desc, 0, 1))
}

output day01_p2 {
	value = sum(slice(local.calory_sum_by_elf_desc, 0, 3))
}

