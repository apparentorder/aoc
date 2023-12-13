from tools.aoc import AOCDay
from typing import Any
    
def mirror_value_smudged(mirror):
    v_orig = mirror_value(mirror)
        
    for m in generate_smudges(mirror):
        if (v := mirror_value(m, except_for = v_orig)):
            return v
    
    print(mirror)
    raise Exception("bad luck")        
            
def mirror_value(mirror, except_for = None):
    return (
        mirror_lines(mirror, "left",  except_for = except_for) or 
        mirror_lines(mirror, "above", except_for = except_for)
    )
            
def mirror_lines(mirror, where, except_for = None):
    if where == "above":
        m_max = len(mirror) - 1
        get_line_xy = lambda y: mirror[y]
    else: # "left"
        m_max = len(mirror[0]) - 1
        get_line_xy = lambda x: str([m[x] for m in mirror])
 
    for v in range(m_max):
        line = get_line_xy(v)
       
        if line == get_line_xy(v + 1):
            # have match, check other lines
            
            for v_after in range(v + 2, min(m_max, v + 1 + v) + 1):
                v_before = v + 1 - (v_after - v)
                if get_line_xy(v_before) != get_line_xy(v_after):
                    break
            else:
                res = (v + 1) * (100 if where == "above" else 1)
                if not except_for or except_for != res:
                    return res
            
    return None
    
def generate_smudges(mirror):
    for y in range(len(mirror)):
        for x in range(len(mirror[0])):
            m = mirror.copy()
            m[y] = m[y][0:x] + ("#" if m[y][x] == "." else ".") + m[y][x+1:]
            yield m
    
class Day(AOCDay):
    inputs = [
        [
            (405, "input13-test"),
            (30158, "input13"),
        ],
        [
            (400, "input13-test"),
            (36474, "input13"),
        ]
    ]

    def part1(self) -> Any:
        mirrors = self.getMultiLineInputAsArray()
        return sum(mirror_value(m) for m in mirrors)

    def part2(self) -> Any:
        mirrors = self.getMultiLineInputAsArray()
        return sum(mirror_value_smudged(m) for m in mirrors)

if __name__ == '__main__':
    day = Day(2023, 13)
    day.run(verbose=True)
