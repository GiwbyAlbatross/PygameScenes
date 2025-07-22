import time

class Profiler:
    sectiontimes: dict[str, float]
    sectionstarts: dict[str, float]
    def __init__(self) -> None:
        self.sectiontimes = {}
        self.sectionstarts = {}
    def start_section(self, sectionname: str) -> None:
        self.sectionstarts[sectionname] = time.time()
    def end_section(self, sectionname: str) -> None:
        t = time.time()
        start_time = self.sectionstarts[sectionname]
        taken = t - start_time
        oldtime = self.sectiontimes.get(sectionname, taken)
        self.sectiontimes[sectionname] = (oldtime + taken) / 2
