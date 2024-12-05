from tools.aoc import AOCDay
from tools.coordinate import Coordinate
from typing import Any

class Day(AOCDay):
	def re_ordered_page_list(self, page_list_in):
		page_set = set(page_list_in)
		page_list = list(page_list_in)
		page_list_ordered = []

		while page_list:
			page = page_list.pop(0)
			pages_needed_before  = self.pages_needed_before.get(page, set()) & page_set
			pages_needed_before -= set(page_list_ordered)

			if pages_needed_before:
				page_list += [page]
				continue

			page_list_ordered += [page]

		return page_list_ordered

	def parse(self):
		(rules_str, updates_str) = self.getMultiLineInputAsArray()

		self.rule_list = [
			(int(pair[0]), int(pair[1]))
			for pair in (
				line.split("|")
				for line in rules_str
			)
		]

		self.update_list = [
			list(map(int, page_list.split(",")))
			for page_list in updates_str
		]

		self.pages_needed_before = {}
		for rule in self.rule_list:
			pages_after = self.pages_needed_before.setdefault(rule[1], set())
			pages_after.add(rule[0])

	def part1(self) -> Any:
		self.parse()
		update_list_ordered = [self.re_ordered_page_list(pl) for pl in self.update_list]
		return sum(
			# middle page for *valid* updates only
			page_list[len(page_list)//2]
			for (i, page_list) in enumerate(update_list_ordered)
			if page_list == self.update_list[i]
		)

	def part2(self) -> Any:
		self.parse()
		update_list_ordered = [self.re_ordered_page_list(pl) for pl in self.update_list]
		return sum(
			# middle page for previously *invalid* (now re-ordered) updates only
			page_list[len(page_list)//2]
			for (i, page_list) in enumerate(update_list_ordered)
			if page_list != self.update_list[i]
		)

	inputs = [
		[
			(143, "input5-test"),
			(5732, "input5"),
		],
		[
			(123, "input5-test"),
			(4716, "input5"),
		]
	]

if __name__ == '__main__':
	day = Day(2024, 5)
	day.run(verbose=True)
