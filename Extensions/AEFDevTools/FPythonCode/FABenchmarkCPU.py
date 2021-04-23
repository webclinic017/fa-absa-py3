from __future__ import print_function
"""Benchmark Front Arena raw calculation performance on multi-core platform

(c) Copyright 2011 by Sungard FRONT ARENA. All rights reserved.

"""


import sys
import os
import time
import acm

def tNow():
    return "2009-01-01"

def t1y():
    return "2010-01-01"
    
def DV(num): 
    """Create denominated value from number"""
    return acm.DenominatedValue(num, "EUR", tNow())

def safe_nbr(obj):
    """Safely convert objects including FDenominatedValues to float"""
    if hasattr(obj, "Number"):
        return obj.Number()
    return float(obj)

def time_function(func, args, N = 10):
    """Time a function, return (max, min, avg) of 10 calls"""
    max_, min_, sum_ = 0, 9999999, 0
    for i in range(N):
        tic = time.clock()
        func(*args)
        toc = time.clock() - tic
        max_, min_, sum_ = max(max_, toc), min(min_, toc), sum_ +  toc
    return max_, min_, sum_ / N

class BasicTextOutput:
    """Output result of benchmark to basic tab separated file"""
    
    def __init__(self, outpath, echo_to_stdout = True):
        self.echo_to_stdout = echo_to_stdout
        self.fname = os.path.join( outpath, "FA_perf_" + time.strftime("%y-%m-%d_%H%M%S") + ".txt" )
        self._outfile = open(self.fname, 'wt')
        self._outfile.flush()
        
    def heading(self, text):
        if self.echo_to_stdout: print ("\n***", text)
        self._outfile.write( "\n***" + str(text) + "\n")
        self._outfile.flush()
        
    def subheading(self, text):
        if self.echo_to_stdout: print ("-", text)
        self._outfile.write( "-" + str(text) + "\n")
        self._outfile.flush()
        
    def key_value(self, key, value):
        if self.echo_to_stdout: print (" ", key , " -> ", value)
        self._outfile.write( str(key) + "\t" + str(value) + "\n")
        self._outfile.flush()
        
    def table(self, data):
        for row in data:
            if self.echo_to_stdout: print ("\t".join(str(cell) for cell in row))
            self._outfile.write("\t".join(str(cell) for cell in row) +  "\n" )
            self._outfile.flush()    
            
            
class BenchConfig():
    """Read config info for benchmark, currently from a Python file"""
    data = "uninitialized"
    def get(key, default):
        if BenchConfig.data == "uninitialized":
            try:            
                BenchConfig.data = __import__("FABenchmarkCPUConfig")
            except Exception as err:
                print ("Failed to read config data, using defaults. Err = ", err)
                BenchConfig.data = None    
        return getattr(BenchConfig.data, key, default)
    get = staticmethod(get)


class BenchmarkFunction():
    repository = {} # name --> BenchmarkFunction
    def __init__(self, func_name, args, shiftable_arg, scalable_arg):
        self.func_name = func_name
        self.func = acm.GetFunction(func_name, len(args) )
        self.args = list(args)
        self.shiftable_arg = shiftable_arg
        self.scalable_arg = scalable_arg
        self._unique_int = 1
    
    def make_single_call(self):
        return self.func(*self.args)

    def make_vector_call(self, N, heavines = None):
        uint = self.unique_int()
        base_val = safe_nbr( self.args[self.shiftable_arg] )
        shifts = [base_val + 0.001 *i + float(uint) / 100000000 for i in range(N) ]        
        args = self.args[:]
        args[self.shiftable_arg] = shifts
        if heavines != None:
            args[self.scalable_arg] = heavines
        tic = time.clock()
        res = self.func(*args)
        toc = time.clock() - tic
        return res, toc
        #self.eval_adfl("""barrierContinuousMonteCarlo(%s, 0.3, denominatedvalue(20), 0.03, 0.01, 0, 1, "2009-01-01", "2010-01-01", 0, 0, 1, 1, 10, 30, 0, 0,[],  0, %s, 0, 0, 0)""" % (shifts, str(mc_steps) ) )

    def unique_int(self):
        self._unique_int += 1
        return self._unique_int

    def add(func_name, args, shiftable_arg, scalable_arg):
        BenchmarkFunction.repository[func_name] = BenchmarkFunction(func_name, args, shiftable_arg, scalable_arg)
    add = staticmethod(add)
    
    def build_repository():
        if BenchmarkFunction.repository:
            return
        BenchmarkFunction.add( "barrierContinuousMonteCarlo", ( DV(20), 0.3, DV(20), 0.03, 0.01, 0, 1, tNow(), t1y(), 0, 0, 1, 1, 10, 30, 0, 0,[],  0, 50, 0, 0, 0), 2, 19 )
        BenchmarkFunction.add( "finiteDifferenceModel", (DV(20), 0.3, DV(20), 1, 0.03, 0.01, 1, 1, 1, 1, [], "2009-09-01", "2010-01-01", 1, 30, {}, 1), 3 , 14)     
        BenchmarkFunction.add( "add", (1,2), 0, 1)     
    build_repository = staticmethod(build_repository)

    def get(func_name):
        BenchmarkFunction.build_repository()
        return BenchmarkFunction.repository[func_name]
    get = staticmethod(get)

    def get_all_func_names():
        BenchmarkFunction.build_repository()
        return BenchmarkFunction.repository.keys()
    get_all_func_names = staticmethod(get_all_func_names)
        
        
class FABenchmark():

    def __init__(self, scale = 10, echo_to_stdout = True):
        self.echo_to_stdout = echo_to_stdout
        self.out = BasicTextOutput(BenchConfig.get("out_path", "c:\\"), echo_to_stdout)
        self.scale = scale
        acm.Memory.GcBackgroundFinalization(False)
        
    def run(self):
        """Run benchmark return name of file with results"""
        self.out.heading("Starting benchmark run")
        self.run_system_info()
        self.run_raw_cpu()
        self.run_gc_bench()
        self.run_cores_x_jobsize()
        # self.lots_processing() # Dissabled due to core issues
        return self.out.fname
        
    def run_system_info(self):
        self.out.heading("System Info")
        self.out.key_value("User", acm.UserName())
        self.out.key_value("ADS", acm.ADSAddress())
        self.out.key_value("Today", acm.Time.DateToday())
        self.out.key_value("PRIME Version", acm.Version())

    def run_raw_cpu(self):
        self.out.heading("Raw single core CPU performance")
        for func_name in sorted(BenchmarkFunction.get_all_func_names()):
            self.out.subheading("10 calls to " + func_name)
            func = BenchmarkFunction.get(func_name)
            max_, min_, avg = time_function(func.make_single_call, tuple() )
            self.out.key_value("max", max_)
            self.out.key_value("min", min_)
            self.out.key_value("avg", avg)

    def run_gc_bench(self):
        def create_garbage():
            for i in range(BenchConfig.get("gc_n_arrays", 1000)):
                arr = acm.FArray()
                for i in range(BenchConfig.get("gc_array_size", 100)):
                    narr = acm.FArray()
                    arr.Add( narr )
                    arr = narr

        self.out.heading("GC benchmark, 10 collects")
        tottime = 0
        for i in range(self.scale):
            create_garbage()  
            tic = time.clock()
            acm.Memory.GcWorldStoppedCollect()
            tottime += time.clock() - tic
        self.out.key_value("gctime", tottime )
        
        
    def run_cores_x_jobsize(self):
        for model_name in ["add", "barrierContinuousMonteCarlo", "finiteDifferenceModel"]:                            
            for lots_size in BenchConfig.get("I_default_lot_sizes", [500]):            
                self.out.heading("Model X Nbr Jobs X Cores X Job Cost: " )
                self.out.key_value("model", model_name)
                self.out.key_value("size", lots_size)
                mc_steps = BenchConfig.get("I_steps_" + model_name, [1,5,20] )
                data = [ [""] + mc_steps ]
                for cores in BenchConfig.get("cores", [1,2,3,4,5]):
                    row  = [cores]
                    for mc_step in mc_steps:
                        res = 999999
                        measurements = 5
                        if model_name == 'add':
                            measurements = 10
                        for i in range(measurements):
                            res = min(res, self._time_model(model_name, mc_step, lots_size, cores))
                        row.append( res )
                    data.append(row)
                    if self.echo_to_stdout: print (" THREADS -> ", acm.FWUThread.Instances().Size())
                self.out.table(data)
    
    def lots_processing(self):
        self.out.heading("Multidimensional FLots processing")
        data = [["cores", "time"]]
        for cores in BenchConfig.get("cores", [1,2,3,4,5]):
            self.set_threads(cores)
            l1 = acm.GetFunction('lot', 1)(list(20+float(i)/100 for i in range(10)))
            x = []
            for n in range(10):
                x.append(l1)
            l2 = acm.GetFunction('lot', 2)(x, 1)
            f = acm.GetFunction('.*', 2)     
            a = acm.FArray()
            a.AddAll(list(float(i) for i in range(1000)))

            res = 999999
            for n in range(5):
                tic = time.clock()
                f(l2, a)
                toc = time.clock() - tic
                res = min(res, toc)        
            data.append( [ cores, res ] )
            time.sleep(1)
        self.out.table(data)

    def set_threads(self, N):
        if acm.WorkUnitThreads.PoolSize() != N:
            acm.WorkUnitThreads.PoolSize(N)
        
    def _time_model(self, model_name, mc_steps, N, threads):
        self.set_threads(threads)
        benchmark_function = BenchmarkFunction.get(model_name)
        res, toc = benchmark_function.make_vector_call(N, mc_steps)
        return toc

def main():
    print ("\n"*100)
    bench = FABenchmark()    
    bench.run()

if __name__ == '__main__':     
    main()

