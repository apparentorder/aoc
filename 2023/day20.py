from tools.aoc import AOCDay
from typing import Any
import math

class CommSystem:
    def __init__(self, input):
        self.modules = {}
        for line in input:
            m = CommModule.from_string(self, line)
            self.modules[m.name] = m
            
        self.modules["button"] = CommModule(self, "button -> broadcaster")
        
        # collect untyped modules (like `output` in the test2 input)
        untyped = set()
        for m in self.modules.values():
            for r in m.receivers:
                if r not in self.modules:
                    untyped.add(r)
        
        for r in untyped:
            self.modules[r] = CommModule(self, r)
            
        # connect senders
        for receiving_module in self.modules.values():
            for sending_module in self.modules.values():
                if receiving_module.name in sending_module.receivers:
                    receiving_module.add_sender(sending_module.name)
                    
        self.button_pushes = 0
        self.pulse_queue = []
        self.pulses_sent = { v: 0 for v in [True, False] }
        
    def push_button(self):
        self.button_pushes += 1
        self.send("button", "broadcaster", False)
        self.process_queue()        
        
    def send(self, sender, receiver, is_high):
        self.pulse_queue += [(sender, receiver, is_high)]

    def process_queue(self):
        while self.pulse_queue:
            sender, receiver, is_high = self.pulse_queue.pop(0)
            
            # print(f"{sender} -{is_high}-> {receiver}")
            self.pulses_sent[is_high] += 1
            self.modules[receiver].receive(sender, is_high)
                
class CommModule:
    def __init__(self, commsys, s):
        parts = s.split()
        self.commsys = commsys
        self.name = parts[0]
        
        if len(parts) == 1:
            # sink module
            self.receivers = []
        else:
            self.receivers = "".join(parts[2:]).split(",")
            
        self.senders = []
        self.first_high_by_sender = {}
        
    def send_pulses(self, is_high):
        for r in self.receivers:
            self.commsys.send(self.name, r, is_high)
            
    def add_sender(self, sender):
        self.senders += [sender]
        self.first_high_by_sender[sender] = None            
        
    def receive(self, sender, is_high):
        # common for all modules
        
        if is_high and self.first_high_by_sender[sender] is None:
            # track when each input was high for the first time (for part 2)
            self.first_high_by_sender[sender] = self.commsys.button_pushes        
            
        self.receive_module_specific(sender, is_high)
        
    def receive_module_specific(self, sender, is_high):
        # default handler, unless defined by subclass -- just send the pulse along
        self.send_pulses(is_high)
        
    @classmethod
    def from_string(self, commsys, s):
        if s[0] == "%":
            return FlipFlopModule(commsys, s[1:])
        elif s[0] == "&":
            return ConjunctionModule(commsys, s[1:])
        else:
            return CommModule(commsys, s)
            
class FlipFlopModule(CommModule):
    def __init__(self, commsys, s):
        super().__init__(commsys, s)
        self.ff_state = False
        
    def receive_module_specific(self, sender, is_high):
        if is_high:
            return
        
        self.ff_state = not self.ff_state
        self.send_pulses(self.ff_state)

class ConjunctionModule(CommModule):
    def __init__(self, commsys, s):
        super().__init__(commsys, s)
        self.con_state_by_sender = {}

    def receive_module_specific(self, sender, is_high):
        self.con_state_by_sender[sender] = is_high
        
        send_high_pulse = False
        for sender in self.senders:
            if not self.con_state_by_sender.get(sender, False):
                send_high_pulse = True
                break
            
        self.send_pulses(send_high_pulse)
        
class Day(AOCDay):
    inputs = [
        [
            (32000000, "input20-test"),
            (11687500, "input20-test2"),
            (1020211150, "input20-penny"),
            (856482136, "input20"),
        ],
        [
            (238815727638557, "input20-penny"),
            (224046542165867, "input20"),
        ]
    ]

    def part1(self) -> Any:
        cs = CommSystem(self.getInput())
        
        for _ in range(1000):
            cs.push_button()

        return cs.pulses_sent[True] * cs.pulses_sent[False]

    def part2(self) -> Any:
        cs = CommSystem(self.getInput())
        
        assert len(cs.modules["rx"].senders) == 1
        rx_sender_name = cs.modules["rx"].senders[0]
        assert isinstance(cs.modules[rx_sender_name], ConjunctionModule)
        
        while True:
            cs.push_button()
        
            if all(cs.modules[rx_sender_name].first_high_by_sender.values()):
                break
            
        return math.lcm(*cs.modules[rx_sender_name].first_high_by_sender.values())
        
if __name__ == '__main__':
    day = Day(2023, 20)
    day.run(verbose=True)
