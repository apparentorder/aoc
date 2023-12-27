from tools.aoc import AOCDay
from typing import Any
import collections

class Wire:
    def __init__(self, c1, c2):
        assert c1 != c2
        self.c1, self.c2 = sorted([c1, c2], key = lambda c: c.id)
        self.id = f"{self.c1}/{self.c2}"
        
    def other(self, c):
        return self.c1 if c == self.c2 else self.c2
        
    def __repr__(self):
        return self.id
        
class Component:
    def __init__(self, id):
        self.id = id
        self.wires = set()
        self.wire_to = {}
        
    def connect(self, other):
        wire = Wire(self, other)
        self.wires.add(wire)
        self.wire_to[other] = wire
        other.wires.add(wire)
        other.wire_to[self] = wire
    
    @property
    def targets(self):
        return [w.other(self) for w in self.wires]
                
    def paths(self, target, blacklisted_wires):
        # if target, returns the path of wires used
        # if not target, returns all reachable components
        
        unresolved = set([self])
        resolved = set()
        prev_c = {}
        prev_c[self] = None
        steps_to = {}
        steps_to[self] = 0
        
        while unresolved:
            c = min(unresolved, key = lambda c: steps_to[c])
            unresolved.remove(c)
            resolved.add(c)
            
            if target == c:
                break
            
            for w in c.wires - blacklisted_wires:
                c_other = w.other(c)
                if c_other in resolved:
                    continue
                    
                unresolved.add(c_other)
                
                dist = steps_to[c] + 1
                if dist < steps_to.get(c_other, 2**63):
                    steps_to[c_other] = dist
                    prev_c[c_other] = c

        if not target:
            return steps_to
            
        if target not in prev_c:
            return None
            
        path = []
        c = target
        while prev_c[c]:
            path += [c.wire_to[prev_c[c]]]
            c = prev_c[c]
            
        return path
        
    def __repr__(self):
        return self.id
        
def parse(input):
    components = {}
    
    for line in input:
        parts = line.replace(":", "").split()
        
        for c_id in parts:
            if not c_id in components:
                c = Component(c_id)
                components[c_id] = c
                
        for target_id in parts[1:]:
            components[parts[0]].connect(components[target_id])
            
    for c in components.values():
        assert len(c.wires) > 3
        
    wires = set(w for c in components.values() for w in c.wires)
    return components, wires
    
class Day(AOCDay):
    inputs = [
        [
            (54, "input25-test"),
            (544523, "input25-penny"),
            (545528, "input25"),
        ],
        [],
    ]
    
    def part1(self):
        # every node is connected to at least four other nodes.
        #
        # if exactly three wires can be disconnected to form two separate graphs,
        # then each of those wires can find a path between its two components only
        # via itself and the two other connecting wires.
        #
        # for each wire, we figure out a path and then repeat the process with
        # the previous path wires blacklisted. if there still is a way between
        # a wire's components after that, it's not a wire that can be disconnected.
        #
        # runtime is about a minute, though.
        
        _, wires = parse(self.getInput())
        
        bridge_wires = []
        for w in wires:
            bl = set()
            
            bl.add(w)
            p = w.c1.paths(target = w.c2, blacklisted_wires = bl)
            # print(f"pts({w}) #1 bl = {bl} = {p}")
            
            bl |= set(p[1:-1])
            p = w.c1.paths(target = w.c2, blacklisted_wires = bl)
            # print(f"pts({w}) #2 bl = {bl} = {p}")
            
            bl |= set(p[1:-1])
            p = w.c1.paths(target = w.c2, blacklisted_wires = bl)
            
            # print(f"pts({w}) #3 bl = {bl} = {p}")
            if p is None:
                print(f"pts({w}) #3 bl = {bl} = {p}")
                bridge_wires += [w]
                
                if len(bridge_wires) == 3:
                    break
                
        assert len(bridge_wires) == 3
        
        cc1 = bridge_wires[0].c1.paths(target = None, blacklisted_wires = set(bridge_wires))
        cc2 = bridge_wires[0].c2.paths(target = None, blacklisted_wires = set(bridge_wires))
        return len(cc1) * len(cc2)


if __name__ == '__main__':
    day = Day(2023, 25)
    day.run(verbose=True)
