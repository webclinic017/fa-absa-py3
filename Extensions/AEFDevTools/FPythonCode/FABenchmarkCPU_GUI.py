from __future__ import print_function
"""GUI to start Front Arena Bencmhark

(c) Copyright 2011 by Sungard FRONT ARENA. All rights reserved.

"""

import os
import acm

import FABenchmarkCPU
import FABenchmarkCPUConfig
import FABenchmarkReport

trueFalse = {'False': False, 'True' : True}

def run_benchmark(outputdir):    
    bench = FABenchmarkCPU.FABenchmark(echo_to_stdout=True)    
    fname = bench.run()
    print ("Benchmark data written to : ", fname)
    pd = FABenchmarkReport.MtPerfDataParser(  )
    pd.load_from_file( open(fname) )
    pd.data.dump_to_xls("analys.xls")
    print ("Benchmark data written to : ", fname)
    print ("Summary of benchmark results:\n")
    FABenchmarkReport.extract_standard_metrics( pd.data, "")

def get_output_directory():    
    selection = acm.FFileSelection()
    selection.PickDirectory(True)
    selection.SelectedDirectory = os.getcwd()
    return selection

ael_variables = [ 
        ['outputdir', 'Output Directory', get_output_directory(), None, get_output_directory(), 0, 1, "Target directory for files produced by benchmark", None, 1],]

def ael_main(aelvars):
    outputdir = aelvars['outputdir']
    print ("Starting Front Arena benchmark. This may take several minutes to complete.")
    print ("output written to : ", outputdir)
    run_benchmark(outputdir)
