import copy
from tools.aoc import AOCDay
from typing import Any
import re

class Valve:
	def __init__(self, s):
		e = s.split()

		self.id = e[1]
		self.rate = int(e[4].split("=")[1].rstrip(";"))
		self.tunnels_to = [v.rstrip(",") for v in e[9:]]

	def __repr__(self):
		#return f"[valve={self.id} rate={self.rate} to={self.tunnels_to}]"
		return f"{self.id}@{self.rate}"

class Cave:
	def __init__(self, input, minutes_total):
		self.valves = {}
		self.minutes_total = minutes_total

		for line in input:
			v = Valve(line)
			self.valves[v.id] = v

		self.__get_poi_distance_map()

	def get_distance(self, source, target):
		return self.distance_map[source][target]

	def __get_poi_distance_map(self):
		self.distance_map = {}

		for v1 in self.valves.values():
			if not (v1.id == 'AA' or v1.rate > 0): continue
			self.distance_map[v1.id] = {}

			for v2 in self.valves.values():
				if not (v2.id == 'AA' or v2.rate > 0): continue
				if v1 == v2: continue

				self.distance_map[v1.id][v2.id] = self.__calc_distance(v1.id, v2.id)

		#print(self.distance_map)

	def __calc_distance(self, vstart, vend):
		paths = [[vstart]]

		while True:
			next_paths = []

			for path in paths:
				targets = self.valves[path[-1]].tunnels_to
				for target in targets:
					if target == vend:
						return len(path)
					if target in path:
						# don't go back
						continue
					next_paths += [path + [target]]

			paths = next_paths

class State:
	def __init__(self, cave, players = 1, internal_copy = False):
		self.cave = cave
		self.players = players
		self.pressure_release = 0
		self.minutes_left = cave.minutes_total

		if not internal_copy:
			# when called by copy(), we don't need to waste time generating these lists
			self.__path = [['AA'] for _ in range(players)]
			self.pressure_release_per_player = [0 for _ in range(players)]
			self.minutes_left_per_player = [cave.minutes_total for _ in range(players)]

	def copy(self):
		new = State(self.cave, players = self.players, internal_copy = True)

		new.pressure_release = self.pressure_release
		new.minutes_left = self.minutes_left

		new.__path = [list(vo_player) for vo_player in self.__path]
		new.pressure_release_per_player = list(self.pressure_release_per_player)
		new.minutes_left_per_player = list(self.minutes_left_per_player)

		return new

	def get_path(self, player = 0):
		return self.__path[player]

	def get_path_len(self, player = 0):
		players = [player] if player is not None else list(range(self.players))
		return sum(len(p) for i, p in enumerate(self.__path) if i in players)

	def get_valves_remaining(self):
		r  = set(self.cave.distance_map.keys()) - set(valve for path_player in self.__path for valve in path_player)
		return r

	def __update_player(self, player):
		# formula:
		# pressure released per valve =
		# (minutes - sum(steps_taken) - sum(stops)) * valve_rate
		# where
		# - minutes is the number of turns/minutes,
		# - sum(steps_taken) is the sum of *movements* needed to get from AA to this valve,
		# - sum(stops) is the number of extra turns waited for opening a valve (equal to position in list!)

		released = 0
		sum_steps = 0
		sum_stops = 0

		for i in range(1, len(self.__path[player])):
			distance = self.cave.get_distance(self.__path[player][i-1], self.__path[player][i])

			sum_steps += distance
			sum_stops += 1

			released += (self.cave.minutes_total - sum_steps - sum_stops) * self.cave.valves[self.__path[player][i]].rate

		self.pressure_release_per_player[player] = released
		self.minutes_left_per_player[player] = self.cave.minutes_total - sum_steps - sum_stops

	def update(self, player = None):
		players = [player] if player is not None else list(range(self.players))

		for player in players:
			self.__update_player(player)

		self.pressure_release = sum(self.pressure_release_per_player)
		self.minutes_left = min(self.minutes_left_per_player)

	def is_valid_move(self, v, player = 0):
		distance = self.cave.get_distance(self.__path[player][-1], v)
		if self.minutes_left_per_player[player] - distance - 1 <= 0:
			return False

		return True

	def path_add(self, v, player = 0):
		self.__path[player] += [v]
		self.update(player)

	def is_comparable_to(self, other):
		for player in range(self.players):
			# path's last element is the current position, must be identical
			if self.__path[player][-1] != other.__path[player][-1]:
				return False

			# all other elements are valid in any order to be comparable
			path_set_self = set(self.__path[player][:-1])
			path_set_other = set(other.__path[player][:-1])
			if path_set_self != path_set_other:
				return False

def max_release(cave, optimize_heuristic_top_percent = False, players = 1):
	max_pressure_released = 0

	initial_state = State(cave, players = players)
	states = [initial_state]

	while len(states) > 0:
		new_states = []

		# continue the state with the most pressure released so far
		states.sort(reverse = True, key = lambda s: s.pressure_release)

		state = states.pop(0)

		if state.pressure_release > max_pressure_released:
			print(f"path {state.get_path()} = {state.pressure_release}")
			max_pressure_released = state.pressure_release

		remaining_valves = state.get_valves_remaining()
		#print(f"at path {state.get_path()} remaining {remaining_valves} min left {state.minutes_left}")

		# optimization:
		# - if there's more time left than half the total time,
		#   we probably haven't visited enough paths (i.e. it's too early to tell)
		# - if there's less time than that, we should be within some fraction of the currently-known
		#   best path. this is hacky and optimal values differ wildly per input.
		is_viable = state.minutes_left > state.cave.minutes_total//2 or state.pressure_release > max_pressure_released//1.5

		if is_viable or not optimize_heuristic_top_percent:
			for player in range(players):
				for next_valve in remaining_valves:
					if state.is_valid_move(next_valve, player=player):
						new = state.copy()
						new.path_add(next_valve, player = player)
						new_states += [new]

		states = states + new_states

	return max_pressure_released

class Day(AOCDay):
	inputs = [
		[
			#(1651, '16'),
			(1651, '16-test')
			,(1850, '16-penny')
			,(1947, '16')
		],
		[
			(1707, '16-test')
			,(2306, '16-penny')
			,(2556, '16')
		]
	]

	def part1(self) -> Any:
		cave = Cave(self.getInput(), minutes_total = 30)
		return max_release(cave, players = 1, optimize_heuristic_top_percent=True)

	def part2(self) -> Any:
		cave = Cave(self.getInput(), minutes_total = 26)
		return max_release(cave, players = 2, optimize_heuristic_top_percent=True)

