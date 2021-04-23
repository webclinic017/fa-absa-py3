from __future__ import print_function
"""Analysis of performance benchmark data 


(c) Copyright 2011 by Sungard FRONT ARENA. All rights reserved.
 
"""

import re 
import os.path

from sets import Set

try:
    pylab_imported_ok = False
    from pylab import *
    pylab_imported_ok = True
except ImportError:
    print ("FABenchmarkReport: Module pylab must be installed for graph support in benchmark. Proceeding without graphs")


class PerfReportOutput:

    def __init__(self, outpath):
        self.outpath = outpath
        
    def save_plot(self, fname):
        savefig( os.path.join( self.outpath, fname) )

    def write(self, *text):
        print ("".join( str(s) for s in text))
        
        
def vec_match(vec1, vec2):
    """Test if vectors are equal, disregarding any None elements"""
    for el1, el2 in zip(vec1, vec2):
        if el1 != el2 and el1 != None and el2 != None:
            return False
    return True


def calc_speedup_factor(vec):
    return vec[0] / min(vec)


def get_yvalues(series):
    return [row[1] for row in series]

    
class MtPerfData:
    model = 0
    vecsize = 1
    modelheavy = 2
    cores = 3
    
    def __init__(self): 
        self.user = None
        self.ads = None
        self.today = None
        self.prime_version = None
        self.gc = None
        self.cube = {} # { (model, vecsize, modelheavy, cores)  : runtime }

    def dump_to_xls(self, fname):
        f = open(fname, 'w')
        f.write("model\tvecsize\tmodelheavy\tcores\truntime\n")
        for (model, vecsize, modelheavy, cores) , runtime in self.cube.items():
            f.write("\t".join( str(v).replace(".", ",") for v in [ model, vecsize, modelheavy, cores, runtime ] ) + "\n")
        f.close()

    def get_dimension(self, dim):
        return sorted( Set( row[dim] for row in self.cube.keys() ) )

    def extract_vector(self, dim_vals):
        sort_key = dim_vals.index(None)
        items = [ row for row in self.cube.items() if vec_match(row[0], dim_vals) ]
        items.sort(key = lambda x: x[0][sort_key])
        return [ (item[0][sort_key], item[1] ) for item in  items ]
        
    def extract_value(self, dim_vals):
        return self.cube[dim_vals]
        
def extract_standard_metrics(pd, outpath):
    out = PerfReportOutput(outpath)
    out.write("\nFront Arena Benchmark:")

    # Metric 1 composite performance benchmark single core
    single_pde = pd.extract_value( ('finiteDifferenceModel', 1000, 90, 1) )
    single_barrier = pd.extract_value( ('barrierContinuousMonteCarlo', 1000, 20, 1) )
    single_gc = pd.gc
    
    single_composite = ( 1.89  / single_pde ) * 4 + ( 1.31 / single_barrier ) * 4 + ( 0.18 / single_gc ) * 2
    out.write( "Composite score for single thread operation = \n  --> ", single_composite, "\n")

    # Metric 2 composite performance benchmark making optimal use of multi-core
    multi_pde = min( get_yvalues( pd.extract_vector( ['finiteDifferenceModel', 1000, 90, None] ) ) )
    multi_barrier = min( get_yvalues( pd.extract_vector( ['barrierContinuousMonteCarlo', 1000, 20, None] ) ) )    
    multi_composite =  ( 1.89  / multi_pde ) * 4 + ( 1.31 / multi_barrier ) * 4 + ( 0.18 / single_gc ) * 2
    out.write( "Composite score for multi thread operation = \n  --> ", multi_composite, "\n")

    # Analysis 1
    out.write("\n\n---Details analysis----------------------------")

    out.write("       user = " + str(pd.user) )
    out.write("       ads = " + str(pd.ads) )
    out.write("       today = " + str(pd.today) )
    out.write("       prime_version = " + str(pd.prime_version) )

    # Metric 1 speedup for large vector Finite differnece    
    v =  pd.extract_vector( ['finiteDifferenceModel', 1000, 30, None] )
    if pylab_imported_ok:
        plot( *list(zip(*v)) )
        xlabel("cores")
        ylabel("calc time (s)")
        title("1000 element vector calls to finite difference 30")
        out.save_plot("finite_diff_30.png")
    out.write( "Speedup factor for large vector of calls to fast model using multi-core = \n  --> ", calc_speedup_factor( get_yvalues( v ) ) , "\n")

    # Metric 2 speedup for small (3) vector Finite differnece
    v =  pd.extract_vector( ['finiteDifferenceModel', 3, 30, None] )
    if pylab_imported_ok:
        plot( *list(zip(*v)) )
        xlabel("cores")
        ylabel("calc time (s)")
        title("3 element vector calls to finite difference 30")
        out.save_plot("finite_diff_30.png")
    out.write( "Speedup of very small vector to common model using multi-core =\n  -->  ", calc_speedup_factor( get_yvalues( v ) ) , "\n")
 
    calc_times = [( vec_size, pd.extract_vector( ['finiteDifferenceModel', vec_size, 30, None] ) ) for 
                    vec_size in pd.get_dimension(pd.vecsize)] 
    speedfacts = [  (vec_size, calc_speedup_factor( get_yvalues( v ) ) ) for vec_size,  v in calc_times if v]
    if pylab_imported_ok:
        clf()
        plot(*list(zip(*speedfacts)))
        out.save_plot("speed_facts.png")
    out.write( "Speedup factors for finite difference model (30) steps for different cores" )
    for vec_size, speedup in speedfacts:
        out.write("\t",vec_size, "\t", speedup)

    out.write("\nBreakdown of composit benchmarks")
    out.write("  Composite benchmark single core = ", single_composite)
    out.write("    pde part,        ", ( 1.89 / single_pde ) * 4 )
    out.write("    barrier part,    ",  ( 1.31 / single_barrier ) * 4)
    out.write("    gc part          ", ( 0.18 / single_gc ) * 2 )
    
    out.write("\n  Composite benchmark multi core = ", multi_composite)
    out.write("    pde part,        ", ( 1.89 / multi_pde ) * 4 )
    out.write("    barrier part,    ",  ( 1.31 / multi_barrier ) * 4)
    out.write("    gc part          ", ( 0.18 / single_gc ) * 2 )
    
def test2(pd):  
    extract_standard_metrics(pd)

def ensure_list(obj):
    if not isinstance(obj , list ):
        return [obj]
    return obj
    
class MtPerfDataParser:
    """Parse performance data from a file"""

    handlers = {}  # Re -> method to handle 
    
    def __init__(self):
        self.enter_handler = MtPerfDataParser.handler_null
        self.collect_handler = MtPerfDataParser.handler_null
        self.exit_handler = MtPerfDataParser.handler_null
        self._key_value = {}       
        self.data = MtPerfData()
        
    def load_from_file(self, file_):
        for line in file_:
            if line.startswith("***"):
                new_handlers = None
                for handler_re, handlers in MtPerfDataParser.handlers.items():
                    if re.match(handler_re, line):
                        new_handlers = handlers
                        break
                if not new_handlers:
                    new_handlers = (MtPerfDataParser.handler_null, MtPerfDataParser.handler_null, MtPerfDataParser.handler_null)
                self.exit_handler(self, line)
                self.enter_handler, self.collect_handler, self.exit_handler = new_handlers
                self.enter_handler(self, line)
            else:
                self.collect_handler(self, line)
        self.exit_handler(self, "")
    def make_value(self, text):
        """Convert text to propper value, float, array etc"""
        text = text.strip()
        try:
            return int(text)
        except ValueError:
            pass
        try:
            return float(text)
        except ValueError:
            pass
        try:
            return [float(cell) for cell in text.split("\t")]          
        except ValueError:
            pass           
        return text
            
    def handler_null(self, _line):
        pass
        
    def handler_sys_info(self, _line):
        self.data.user = self._key_value['User']
        self.data.ads = self._key_value['ADS']
        self.data.today = self._key_value['Today']
        self.data.prime_version = self._key_value['PRIME Version']
        
    def handler_gc(self, _line):
        self.data.gc = self._key_value['gctime']

    def handler_key_value(self, line):
        splitline = line.split("\t", 1)
        if len(splitline) == 2:            
            self._key_value[self.make_value(splitline[0])] = self.make_value( splitline[1] )
    
    def handler_clear_key_value(self, _line):        
        self._key_value = {}

    def handler_table(self, _line):
        model, veclength = self._key_value.pop("model"), self._key_value.pop("size")
        modelheavies = self._key_value.pop("") # Table headings, '' as key
        for cores, row_cells in self._key_value.items():            
            for modelheavy, runtime in zip(ensure_list(modelheavies), ensure_list(row_cells)):
                self.data.cube[ (model, veclength, modelheavy, cores) ] =  runtime        
                
    handlers[r"\*\*\*System.*"] = handler_clear_key_value, handler_key_value, handler_sys_info
    handlers[r"\*\*\*Model X Nbr Jobs X Cores X Job Cost.*"] = handler_clear_key_value, handler_key_value, handler_table
    handlers[r"\*\*\*GC benchmark.*"] = handler_clear_key_value, handler_key_value, handler_gc
    
def test():
    pd = MtPerfDataParser(  )
    pd.load_from_file( open("perf.txt") )
    pd.data.dump_to_xls("analys.xls")
    test2( pd.data ) 
        
if __name__ == '__main__':
    test()



