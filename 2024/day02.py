from tools.aoc import AOCDay
from typing import Any

class Day(AOCDay):
	def report_is_safe(self, report: [int]):
		diffs = [report[i] - report[i+1] for i in range(len(report) - 1)]
		if all(map(lambda x: x in range(1,4), diffs)): return True
		if all(map(lambda x: x in range(-3,0), diffs)): return True
		return False

	def report_is_safe_with_skip(self, report: [int]):
		reports_to_try = [report]
		for i in range(len(report)):
			report_with_skip = list(report)
			del report_with_skip[i]
			reports_to_try += [report_with_skip]

		return any(map(self.report_is_safe, reports_to_try))

	inputs = [
		[
			(2, "input2-test"),
			(486, "input2"),
		],
		[
			(4, "input2-test"),
			(540, "input2"),
		]
	]

	def part1(self) -> Any:
		report_list = self.getInputAsArraySplit(" ", int)
		return list(map(self.report_is_safe, report_list)).count(True)

	def part2(self) -> Any:
		report_list = self.getInputAsArraySplit(" ", int)
		return list(map(self.report_is_safe_with_skip, report_list)).count(True)

if __name__ == '__main__':
	day = Day(2024, 2)
	day.run(verbose=True)
