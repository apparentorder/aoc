from time import perf_counter_ns
from .types import IntOrNone


def get_time_string_from_ns(ns: int) -> str:
    # mis, ns = ns // 1000, ns % 1000
    # ms, mis = mis // 1000, mis % 1000
    # s, ms = ms // 1000, ms % 1000
    # m, s = s // 60, s % 60
    # h, m = m // 60, m % 60
    # d, h = h // 24, h % 24

    units = ['ns', 'µs', 'ms', 's']
    unit = 0
    while ns > 1_000:
        if unit > 3:
            break
        ns /= 1000
        unit += 1

    return "%1.2f%s" % (ns, units[unit])


class StopWatch:
    started: IntOrNone = None
    stopped: IntOrNone = None

    def __init__(self, auto_start=True):
        if auto_start:
            self.start()

    def start(self):
        self.started = perf_counter_ns()
        self.stopped = None

    def stop(self) -> float:
        self.stopped = perf_counter_ns()
        return self.elapsed()

    reset = start

    def elapsed(self) -> float:
        if self.stopped is None:
            return perf_counter_ns() - self.started
        else:
            return self.stopped - self.started

    def elapsed_string(self) -> str:
        return get_time_string_from_ns(self.elapsed())

    def avg_elapsed(self, divider: int) -> float:
        return self.elapsed() / divider

    def avg_string(self, divider: int) -> str:
        return get_time_string_from_ns(int(self.avg_elapsed(divider)))

    def __str__(self):
        return self.avg_string(1)
