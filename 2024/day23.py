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

	def part1(self) -> Any:
		self.parse_nodes()

		t_sets: set[str] = set()
		for n0 in [node for node in self.nodes.values() if node.name.startswith("t")]:
			for n1 in n0.connections:
				for n2 in n0.connections & n1.connections:
					t_sets.add(str(sorted([n0.name, n1.name, n2.name])))

		return len(t_sets)

	def part2(self) -> Any:
		self.parse_nodes()

		lan_sets: set[str] = set()
		for this_node in self.nodes.values():
			for network in self.networks:
				if all(this_node in node.connections for node in network):
					network.add(this_node)

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
