import datetime
from typing import Callable, List, Any


class Scheduler:
    def __init__(self):
        self.jobs = {}

    def schedule(self, name: str, every: datetime.timedelta, func: Callable[..., None], *args: List[Any]):
        self.jobs[name] = {
            'call': func,
            'args': args,
            'timedelta': every,
            'runat': (datetime.datetime.utcnow() + every)
        }

    def unschedule(self, name: str):
        if name in self.jobs:
            del self.jobs[name]

    def run_pending(self):
        now = datetime.datetime.utcnow()
        for job in self.jobs.values():
            if job['runat'] <= now:
                job['runat'] += job['timedelta']
                job['call'](*job['args'])
