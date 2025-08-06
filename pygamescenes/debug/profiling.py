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
        start_time = self.sectionstarts.get(sectionname, t+1)
        del self.sectionstarts[sectionname]
        taken = t - start_time
        oldtime = self.sectiontimes.get(sectionname, taken)
        self.sectiontimes[sectionname] = (oldtime + taken) / 2
    def export_report(self, sep='\n') -> str:
        r = ""
        for name, time_ in self.sectiontimes.items():
            r += f"{name}: {time_*1000} ms{sep}"
        return r
