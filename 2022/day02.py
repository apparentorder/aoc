from tools.aoc import AOCDay
from typing import Any

class RPS():
	def __init__(self, letter):
		match letter:
			case 'A' | 'X':
				self.shape = "Rock"
				self.score = 1
			case 'B' | 'Y':
				self.shape = "Paper"
				self.score = 2
			case 'C' | 'Z':
				self.shape = "Scissors"
				self.score = 3
			case _:
				raise Exception("invalid letter: " + letter)

	def against(self, opponent):
		# returns outcome (score points) of game
		match self.shape:
			case opponent.shape:
				return 3
			case "Rock" if opponent.shape == "Scissors":
				return 6
			case "Scissors" if opponent.shape == "Paper":
				return 6
			case "Paper" if opponent.shape == "Rock":
				return 6
			case _:
				return 0

	def __repr__(self):
		return "%s@%d" % (self.shape, self.score)

def game(strategy, is_part2):
	score = 0

	for choices in strategy:
		opponent_shape = RPS(choices[0])
		self_shape = RPS(choices[1])

		if is_part2:
			expected_score = 0 if choices[1] == "X" else 3 if choices[1] == "Y" else 6

			for try_shape in ["A", "B", "C"]:
				self_shape = RPS(try_shape)
				if self_shape.against(opponent_shape) == expected_score:
					break

		outcome = self_shape.against(opponent_shape)
		score += outcome
		score += self_shape.score

		#print("Opponent=%s vs. Self=%s: outcome %d" % (opponent_shape, self_shape, outcome))

	return score

def parse(input):
	return map(lambda x: x.split(), input)

class Day(AOCDay):
	inputs = [
		[
			(15, '02-test'),
			(13_809, '02')
		],
		[
			(12, '02-test'),
			(12_316, '02')
		]
	]

	def part1(self) -> Any:
		return game(parse(self.input), False)

	def part2(self) -> Any:
		return game(parse(self.input), True)

