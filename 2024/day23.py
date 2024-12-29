from tools.aoc import AOCDay
from typing import Any, Self

class Node:
	def __init__(self, name: str):
		self.name = name
		self.connections: set[Node] = set()

	def connect(self, other_node: Self):
		self.connections.add(other_node)
		other_node.connections.add(self)

	def __repr__(self):
		return self.name

class Day(AOCDay):
	def parse_nodes(self):
		self.nodes: dict[str, Node] = {}
		self.networks: list[set[Node]] = []

		for node_pair in self.getInput():
			name0, name1 = node_pair.split("-")
			node0 = self.nodes.setdefault(name0, Node(name0))
			node1 = self.nodes.setdefault(name1, Node(name1))

			node0.connect(node1)
			self.networks += [{node0, node1}]

	def complete_networks(self):
		for this_node in self.nodes.values():
			for network in self.networks:
				if all(this_node in node.connections for node in network):
					network.add(this_node)

	def part1(self) -> Any:
		# this is weird and slow ...
		self.parse_nodes()

		t_sets = set()
		node_list = list(self.nodes.values())
		for i0, n0 in enumerate(node_list):
			for i1, n1 in enumerate(node_list[i0:]):
				for n2 in node_list[i0+i1:]:
					if not any(n.name.startswith("t") for n in [n0, n1, n2]):
						continue

					if n0 in n1.connections and n0 in n2.connections and n1 in n2.connections:
						t_sets.add(str(sorted([n0.name, n1.name, n2.name])))

		return len(t_sets)

	def part2(self) -> Any:
		# ... this isn't.
		self.parse_nodes()
		self.complete_networks()
		biggest_net = sorted(self.networks, key = len, reverse = True)[0]
		return ",".join(sorted(node.name for node in biggest_net))

	inputs = [
		[
			(7, "input23-test"),
			(1308, "input23"),
		],
		[
			("co,de,ka,ta", "input23-test"),
			("bu,fq,fz,pn,rr,st,sv,tr,un,uy,zf,zi,zy", "input23"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 23)
	day.run(verbose=True)
