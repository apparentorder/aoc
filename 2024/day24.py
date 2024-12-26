from tools.aoc import AOCDay
from typing import Any

class Gate:
	def __init__(self, input_line):
		self.input0, self.gate_type, self.input1, _, self.output = input_line.split()
		self.inputs = {self.input0, self.input1}

	def __repr__(self):
		return f"[{self.input0} {self.gate_type} {self.input1} -> {self.output}]"

class Day(AOCDay):
	def parse(self):
		initial_wires, gates = self.getMultiLineInputAsArray()

		self.gates = list(map(Gate, gates))
		self.gates_by_output = {g.output: g for g in self.gates}

		self.wires = {wire: None for wire in self.gates_by_output}
		self.wires.update({w.split(":")[0]: bool(int(w.split(" ")[1])) for w in initial_wires})

		self.input_bits = len([1 for w in self.wires if w.startswith("x")])
		self.swaps: set[str] = set()

	def get_value(self, prefix: str):
		values = [self.resolve_wire(wire) for wire in sorted(self.wires) if wire.startswith(prefix)]
		return sum(n<<i for i, n in enumerate(values))

	def resolve_wire(self, output_wire: str) -> bool | None:
		# print(f"rw {output_wire}")
		if (v := self.wires.get(output_wire)) is not None:
			return v

		output_gate = self.gates_by_output[output_wire]

		input0 = self.wires.get(output_gate.input0, self.resolve_wire(output_gate.input0))
		input1 = self.wires.get(output_gate.input1, self.resolve_wire(output_gate.input1))

		result = None
		if output_gate.gate_type == "AND":
			result = input0 & input1
		elif output_gate.gate_type == "OR":
			result = input0 | input1
		elif output_gate.gate_type == "XOR":
			result = input0 ^ input1

		self.wires[output_wire] = result
		return result

	def resolve_inputs(self, output_wire: str, path_taken: list[list[str]] = []) -> []:
		gate_key = output_wire
		if output_wire.startswith("x") or output_wire.startswith("y"):
			return [path_taken + [gate_key]]

		gate = self.gates_by_output[output_wire]
		gate_key = f"{output_wire} {gate.gate_type}"

		return (
			self.resolve_inputs(gate.input0, path_taken=path_taken + [gate_key]) +
			self.resolve_inputs(gate.input1, path_taken=path_taken + [gate_key])
		)

	def get_input_gate(self, input_bit: int, gate_type: str) -> Gate:
		input_wires = {f"x{input_bit:02}", f"y{input_bit:02}"}
		return next(gate for gate in self.gates if gate.inputs == input_wires and gate.gate_type == gate_type)

	def check_and_swap(self, gate_to_check: Gate, expected_output_wire: str):
		if gate_to_check.output != expected_output_wire:
			other_gate = next(g for g in self.gates if g.output == expected_output_wire)
			# print(f"MISMATCH: found wrong gate {gate_to_check} expected output {expected_output_wire} = gate {other_gate} -- swapping")

			self.swaps.add(gate_to_check.output)
			self.swaps.add(expected_output_wire)

			other_gate.output = gate_to_check.output
			gate_to_check.output = expected_output_wire

	def magic(self, bit: int) -> Gate:
		#
		# Computation for common bits is as shown below.
		#
		# Exceptions are bit 0 (just XOR), bit 1 (XOR, AND) and the final most-significant bit, which will
		# not have the first XOR with its matching x/y input wires (the XOR usually on the left-hand side
		# in the output below).
		#
		# ['z04 XOR', 'rhk XOR', 'x04']
		# ['z04 XOR', 'rhk XOR', 'y04']
		# ['z04 XOR', 'pkm OR', 'wcf AND', 'x03']
		# ['z04 XOR', 'pkm OR', 'wcf AND', 'y03']
		# ['z04 XOR', 'pkm OR', 'fbs AND', 'psp XOR', 'y03']
		# ['z04 XOR', 'pkm OR', 'fbs AND', 'psp XOR', 'x03']
		# ['z04 XOR', 'pkm OR', 'fbs AND', 'qjq OR', 'dqj AND', 'x02']
		# ['z04 XOR', 'pkm OR', 'fbs AND', 'qjq OR', 'dqj AND', 'y02']
		# ['z04 XOR', 'pkm OR', 'fbs AND', 'qjq OR', 'qwd AND', 'dgk XOR', 'y02']
		# ['z04 XOR', 'pkm OR', 'fbs AND', 'qjq OR', 'qwd AND', 'dgk XOR', 'x02']
		# ['z04 XOR', 'pkm OR', 'fbs AND', 'qjq OR', 'qwd AND', 'nkn OR', 'tvb AND', 'y01']
		# ['z04 XOR', 'pkm OR', 'fbs AND', 'qjq OR', 'qwd AND', 'nkn OR', 'tvb AND', 'x01']
		# ['z04 XOR', 'pkm OR', 'fbs AND', 'qjq OR', 'qwd AND', 'nkn OR', 'prh AND', 'wrd AND', 'y00']
		# ['z04 XOR', 'pkm OR', 'fbs AND', 'qjq OR', 'qwd AND', 'nkn OR', 'prh AND', 'wrd AND', 'x00']
		# ['z04 XOR', 'pkm OR', 'fbs AND', 'qjq OR', 'qwd AND', 'nkn OR', 'prh AND', 'npf XOR', 'y01']
		# ['z04 XOR', 'pkm OR', 'fbs AND', 'qjq OR', 'qwd AND', 'nkn OR', 'prh AND', 'npf XOR', 'x01']
		#
		# For any given Gate / operation, the left-hand side is the output wire and the column on the
		# right shows the exactly two input wires.
		#
		# Reverse engineered from input. No idea if other inputs work.
		#

		output_wire = f"z{bit:02}"

		if bit == 0:
			return self.get_input_gate(bit, "XOR")

		if bit == 1:
			or_gate = self.get_input_gate(bit - 1, "AND")
		else:
			input0 = self.get_input_gate(bit - 1, "XOR")
			input1 = self.magic(bit - 1) # this is where it cascades to all the lower bits.
			and_gate = next(g for g in self.gates if g.gate_type == "AND" and g.inputs == {input0.output, input1.output})

			input0 = self.get_input_gate(bit - 1, "AND")
			input1 = and_gate
			or_gate = next(g for g in self.gates if g.gate_type == "OR" and g.inputs == {input0.output, input1.output})

		input0 = self.get_input_gate(bit, "XOR")
		input1 = or_gate

		# The correctness of output bits can be verified from both sides, i.e. either from the computation
		# (verifying the correct final i.e. left-most XOR gate), or by looking up the final XOR via its
		# output field, which should be `z<bit>` if everything works correctly.
		#
		# This catches all bad swaps in my input. Other inputs need to be tested.
		#
		if xor_gate := next((g for g in self.gates if g.gate_type == "XOR" and g.inputs == {input0.output, input1.output}), None):
			self.check_and_swap(expected_output_wire=output_wire, gate_to_check=xor_gate)
		elif xor_gate_rev := next((g for g in self.gates if g.gate_type == "XOR" and g.output == output_wire), None):
			if input0.output not in xor_gate_rev.inputs:
				eo = xor_gate_rev.input0 if xor_gate_rev.input0 != input1.output else xor_gate_rev.input1
				self.check_and_swap(expected_output_wire=eo, gate_to_check=input0)
			elif input1.output not in xor_gate_rev.inputs:
				eo = xor_gate_rev.input1 if xor_gate_rev.input1 != input0.output else xor_gate_rev.input0
				self.check_and_swap(expected_output_wire=eo, gate_to_check=input1)
		else:
			raise Exception("no XOR gate found")

		return or_gate

	def part1(self) -> Any:
		self.parse()
		return self.get_value("z")

	def part2(self):
		# HINT:
		#
		# The test input for part 2 uses a simple `AND` operation
		# instead of addition, so it's rather worthless.
		#
		# HELPFUL OUTPUT:
		#
		# for line in sorted(self.resolve_inputs("z04"), key = len):
		# 	print(line)

		self.magic(bit = self.input_bits - 1)

		if len(self.swaps) != 8:
			raise Exception("wrong number of mismatches")

		return ",".join(sorted(self.swaps))

	inputs = [
		[
			(2024, "input24-test"),
			(42883464055378, "input24-penny"),
			(51715173446832, "input24"),
		],
		[
			# ("z00,z01,z02,z05", "input24-test-p2"),
			("dqr,dtk,pfw,shh,vgs,z21,z33,z39", "input24-penny"),
			("dpg,kmb,mmf,tvp,vdk,z10,z15,z25", "input24"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 24)
	day.run(verbose=True)
