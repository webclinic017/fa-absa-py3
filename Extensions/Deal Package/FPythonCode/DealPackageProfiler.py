from __future__ import print_function
import cProfile, pstats, io
class Profiler():
    def __init__(self):
        self._profiler = cProfile.Profile()
        
    def ProfilingStart(self):
        self._profiler.enable()

    def ProfilingEnd(self):
        self._profiler.disable()
        self.PrintResult()

    def PrintResult(self):
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(self._profiler, stream=s).sort_stats(sortby)
        ps.print_stats()
        print (s.getvalue())
