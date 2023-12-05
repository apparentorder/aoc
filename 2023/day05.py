from tools.aoc import AOCDay
from typing import Any
import re

class Mapper:
    class Mapping:
        def __init__(self, line):
            (
                self.dest_range_start,
                self.source_range_start,
                self.range_length,
            ) = map(int, line.split())
            
            self.source_range = range(self.source_range_start, self.source_range_start + self.range_length)
            self.dest_range = range(self.dest_range_start, self.dest_range_start + self.range_length)
            self.adjust = self.dest_range_start - self.source_range_start
            
        def __repr__(self):
            return f"{self.source_range_start} .. {self.source_range_start + self.range_length - 1}"
            
    def __init__(self, line):
        self.mappings = []
        
    def add_mapping(self, line):
        self.mappings += [Mapper.Mapping(line)]
        
    def map(self, input):
        distance_to_next = 2**63
        for m in self.mappings:
            if input in m.source_range:
                return input + m.adjust, m.source_range.stop - input
                
            if m.source_range.start > input:
                distance_to_next = min(distance_to_next, m.source_range.start - input)
                
        return input, distance_to_next
        
class Almanac:
    def __init__(self, input, is_part2):
        self._mappers = []
        
        self.seed_ranges = []
        seed_data = list(map(int, input[0].split()[1:]))
        while len(seed_data) > 0:
            seed_range_start = seed_data.pop(0)
            seed_range_length = seed_data.pop(0) if is_part2 else 1
            self.seed_ranges += [range(seed_range_start, seed_range_start + seed_range_length)]        
        
        mapper = None
        for line in input[2:]:
            if "map" in line:
                mapper = Mapper(line)
                self._mappers += [mapper]
                continue
            
            if line == "":
                continue
            
            mapper.add_mapping(line)
            
    def map_seed(self, seed):
        mapped_value = seed
        distance_to_next = 2**63
        for m in self._mappers:
            mapped_value, dtn = m.map(mapped_value)
            distance_to_next = min(distance_to_next, dtn)
            #print(f"-> {mapped_value} (dtn={distance_to_next})")
        
        return mapped_value, distance_to_next        
                
    def min_location(self):
        min_location = 2**63
        for sr in self.seed_ranges:
            seed = sr.start
            while seed <= sr.stop:
                location, distance_to_next = self.map_seed(seed)
                min_location = min(min_location, location)
                seed += distance_to_next

        return min_location
        
class Day(AOCDay):
    inputs = [
        [
            (35, "input5-test"),
            (111627841, "input5"),
        ],
        [
            (46, "input5-test"),
            (69323688, "input5"),
        ]
    ]

    def part1(self) -> Any:
        almanac = Almanac(self.getInput(), is_part2 = False)
        return almanac.min_location()

    def part2(self) -> Any:
        almanac = Almanac(self.getInput(), is_part2 = True)
        return almanac.min_location()
        
if __name__ == '__main__':
    day = Day(2023, 5)
    day.run(verbose=True)
