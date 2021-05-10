
import acm
import FUxCore
import deltaDynamicInstruments

def ael_custom_label(parameters, dictExtra):
    return deltaDynamicInstruments.ael_custom_label(parameters, dictExtra)

def ael_custom_dialog_show(shell, params):
    return deltaDynamicInstruments.ael_custom_dialog_show(shell, params)
    
def ael_custom_dialog_main(parameters, dictExtra):
    asqlQuery = parameters.At('asqlQuery')
    benchmarks = deltaDynamicInstruments.createInstruments(asqlQuery)

    resultVector = []
    for ins in benchmarks:
        params = acm.FNamedParameters()
        params.Name(ins.Name())
        params.UniqueTag(ins.Oid())
        params.AddParameter('instrument', ins)
        resultVector.append(params)
    return resultVector
