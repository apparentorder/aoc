locals {
	d06_input = split("\n", trim(file("inputs/${local.d06_input_name}"), "\n\r"))
	d06_buffer = split("", local.d06_input[0])

	# range(): Terraform imposes an artificial limit of 1024 numbers in the resulting sequence :E
	# Therefore use enumerated lists with ugly workarounds for slice() bounds instead.
	# With thanks to https://blog.sharebear.co.uk/2022/01/increasing-your-range-in-terraform/

	d06_packets = [
		for i, _ in local.d06_buffer: i
		if length(toset(slice(local.d06_buffer, (i < 4 ? 4 : i) - 4, i))) == 4
	]

	d06_messages = [
		for i, _ in local.d06_buffer: i
		if length(toset(slice(local.d06_buffer, (i < 14 ? 14 : i) - 14, i))) == 14
	]

	d06_part1 = local.d06_packets[0]
	d06_part2 = local.d06_messages[0]
}

locals {
	# setup
	d06_input_name = "06-test1"
	d06_input_results = {
		"06" = [1034, 2472]
		"06-test1" = [7, 19]
	}
	d06_results = local.d06_input_results[local.d06_input_name]
}

output d06_p1 {
	value = local.d06_part1
	precondition {
		condition = local.d06_part1 == local.d06_results[0]
		error_message = "wrong result"
	}
}

output d06_p2 {
	value = local.d06_part2
	precondition {
		condition = local.d06_part2 == local.d06_results[1]
		error_message = "wrong result"
	}
}

