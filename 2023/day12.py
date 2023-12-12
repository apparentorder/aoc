from tools.aoc import AOCDay
from typing import Any

def parse(input, unfold = 1):
    springs = []
    reference = []

    for line in input:
        parts = line.split()
        springs += [list(parts[0])]
        reference += [list(map(int, parts[1].split(',')))]
        
        for _ in range(1, unfold):
            springs[-1] += ["?"] + list(parts[0])
            reference[-1] += list(map(int, parts[1].split(',')))
            
    return springs, reference
    
def valid_arrangements(springlist, reference):
    springcount = springlist.count("#")
    refsum = sum(reference)
    
    groupcount = 1 if springlist[0] == "#" else 0
    for i in range(1, len(springlist)):
        if springlist[i] == "#" and springlist[i - 1] == ".": groupcount += 1
    
    if springlist.count("#") > sum(reference):
        #print(f"abort: {springlist} ref {reference} # > {refsum}")
        return 0
        
    if springcount + springlist.count("?") < refsum:
        #print(f"abort: {springlist} ref {reference} #+? < {refsum}")
        return 0
        
    if groupcount + springlist.count("?") < len(reference):
        #print(f"abort: {springlist} ref {reference} gc {groupcount} + slc {springlist.count('?')} < lr {len(reference)}")
        return 0        
        
    if groupcount > len(reference):
        #print(f"abort: {springlist} ref {reference} gc {groupcount} > lr {len(reference)}")
        return 0
        
    if "?" not in springlist:
        sl = "".join(springlist)
        springs = [s for s in sl.split(".") if s] # remove empty
        
        if len(springs) != len(reference):
            #print(f"abort: {springlist} ref {reference} ls {len(springs)} != lr {len(reference)}")
            return 0
        
        for i, ref in enumerate(reference):
            if ref != len(springs[i]):
                #print(f"abort: {springlist} ref {reference} ref {ref} != lsi {len(springs[i])}")
                return 0
                
        # we have a winner!
        #print(f"YES: {springlist} ref {reference} #>ref")
        return 1
    
    count = 0
    springlist = springlist.copy()
    i = springlist.index("?")
    
    springlist[i] = "#"
    r = valid_arrangements(springlist, reference)
    #print(f"try {springlist} for {reference} result {r}")
    count += r
    
    springlist[i] = "."
    r = valid_arrangements(springlist, reference)
    #print(f"try {springlist} for {reference} result {r}")
    count += r
    
    return count
    
class Day(AOCDay):
    inputs = [
        [
            (21, "input12-test"),
            (7286, "input12"),
        ],
        [
            (525152, "input12-test"),
            (None, "input12"),
        ]
    ]

    def part1(self) -> Any:
        springs, reference = parse(self.getInput())
        return sum(valid_arrangements(springs[i], reference[i]) for i in range(len(springs)))

    def part2(self) -> Any:
        return ""


if __name__ == '__main__':
    day = Day(2023, 12)
    day.run(verbose=True)
