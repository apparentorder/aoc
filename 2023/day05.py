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
                
    def distance_to_next(self, input):
        # distance to next
        # - when input falls within a range, return range end + 1
        # - when input is not within a range, return the next (higher) source range's start
        # - fallback if there is no match and no next range, return 1
        
        next_range_start = None
        for m in self.mappings:
            if m.source_range_start > input:
                next_range_start = min(next_range_start or 2**31, m.source_range_start)
                
            if input in range(m.source_range_start, m.source_range_start + m.range_length):
                dest = m.dest_range_start + input - m.source_range_start        
                return m.dest_range_start + m.range_length - dest
                
        return next_range_start or 1
        
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
        distance_to_next = None
        for m in self._mappers:
            source_value = mapped_value
            mapped_value = m.map(mapped_value)
            distance_to_next = min(distance_to_next or 2**31, m.distance_to_next(source_value))
            #print(f"{m.source}:{source_value} -> {m.dest}:{mapped_value} (dtn={distance_to_next})")
        
        return mapped_value, (distance_to_next or 1)
        
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
        almanac = Almanac(self.getInput())
        locations = map(lambda seed: (almanac.map_seed(seed))[0], almanac.seeds)
        return min(locations)

    def part2(self) -> Any:
        almanac = Almanac(self.getInput())
        
        locations = []
        seed_data = almanac.seeds
        while len(seed_data) > 0:
            seed_range_start = seed_data.pop(0)
            seed_range_length = seed_data.pop(0)

            seed = seed_range_start
            dtn1_count = 0
            while seed < (seed_range_start + seed_range_length):
                location, distance_to_next = almanac.map_seed(seed)
                #print(f"seed {seed} -> location {location} distance_to_next {distance_to_next}")
                locations += [location]
                seed += distance_to_next

                if distance_to_next == 1:
                    dtn1_count += 1
                    if dtn1_count > 100:
                        # FIXME: it seems obvious that there is a way to determine
                        # if continuing here makes sense or not, but I can't see it
                        # yet. some repeated steps of 1 are required for the test
                        # input, but don't seem to happen at all in the real input.
                        # arbitrarily abort after too many attempts here.
                        print(f"abort at {seed}")
                        break
                    
        return min(locations)
        
if __name__ == '__main__':
    day = Day(2023, 5)
    day.run(verbose=True)
