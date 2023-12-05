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
            
    def __init__(self, line):
        m = re.match('(\S+)-to-(\S+) map:', line)
        self.source = m.group(1)
        self.dest = m.group(2)
        self.mappings = []
        
    def add_mapping(self, line):
        self.mappings += [Mapper.Mapping(line)]
        
    def map(self, input):
        for m in self.mappings:
            if input in range(m.source_range_start, m.source_range_start + m.range_length):
                return m.dest_range_start + input - m.source_range_start
                
        # when no mapping matches, return input unchanged
        return input
                
class Almanac:
    def __init__(self, input):
        self._mappers = []
        self.seeds = list(map(int, input.pop(0).split()[1:]))
        input.pop(0)
        
        mapper = None
        for line in input:
            if "map" in line:
                mapper = Mapper(line)
                self._mappers += [mapper]
                continue
            
            if line == "":
                continue
            
            mapper.add_mapping(line)
            
    def map_seed(self, seed):
        mapped_value = seed
        for m in self._mappers:
            mapped_value = m.map(mapped_value)
        
        return mapped_value
        
class Day(AOCDay):
    inputs = [
        [
            (35, "input5-test"),
            (111627841, "input5"),
        ],
        [
            (46, "input5-test"),
            (None, "input5"),
        ]
    ]

    def part1(self) -> Any:
        almanac = Almanac(self.getInput())
        locations = map(almanac.map_seed, almanac.seeds)
        return min(locations)

    def part2(self) -> Any:
        almanac = Almanac(self.getInput())
        
        locations = []
        seed_data = almanac.seeds
        while len(seed_data) > 0:
            seed_range_start = seed_data.pop(0)
            seed_range_length = seed_data.pop(0)
            
            for seed in range(seed_range_start, seed_range_start + seed_range_length):
                locations += [almanac.map_seed(seed)]
                
        return min(locations)


if __name__ == '__main__':
    day = Day(2023, 5)
    day.run(verbose=True)
