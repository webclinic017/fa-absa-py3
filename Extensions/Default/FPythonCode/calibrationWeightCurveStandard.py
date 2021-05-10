import acm
import math

ael_variables = []

'''Weight function for curves'''       
def ael_main_ex( parameters, dictExtra ):

    #Unpack Filter parameters
    #No parameters used, hence nothing to unpack.

    #Unpack extra provided data for Weight functions
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()
    calibrationRowObject = dict.At('calibrationRowObject')
    
    # A Curve calibration row object encapsulates a benchmark, type FBenchmark.
    # Hence, calibrationRowObject.SourceObject() a benchmark.
    # Note: benchmarks "always" have an instrument.
    result = calibrationRowObject.SourceObject().LossValue()
        
    return [result]
