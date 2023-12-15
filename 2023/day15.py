from tools.aoc import AOCDay
from typing import Any
        
def run_init(initseq):
    boxes = {}
    
    for seq in initseq:
        if "=" in seq:
            parts = seq.split("=")
            label = parts[0]
            focal = int(parts[1])
        else:
            parts = seq.split("-")
            label = parts[0]
            focal = None
            
        label_hash = hash(label)
        lenses = boxes.setdefault(label_hash, [])
        
        for i, (existing_label, existing_focal) in enumerate(lenses):
            if label == existing_label and focal is None: 
                lenses.remove((existing_label, existing_focal))
                break
            if label == existing_label and focal is not None: 
                lenses[i] = (label, focal)
                break
        else:
            if focal:
                boxes[label_hash] += [(label, focal)]

    return boxes
    
def focal_power_sum(boxes):
    s = 0
    for box, lenses in boxes.items():
        for i, (_, focal) in enumerate(lenses):
            s += (box + 1) * (i + 1) * focal
            
    return s    
        
def hash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    
    return h
    
class Day(AOCDay):
    inputs = [
        [
            (1320, "input15-test"),
            (513214, "input15"),
        ],
        [
            (145, "input15-test"),
            (258826, "input15"),
        ]
    ]

    def part1(self) -> Any:
        initseq = self.getInput().split(",")
        return sum(hash(s) for s in initseq)

    def part2(self) -> Any:
        initseq = self.getInput().split(",")
        boxes = run_init(initseq)
        return focal_power_sum(boxes)


if __name__ == '__main__':
    day = Day(2023, 15)
    day.run(verbose=True)
