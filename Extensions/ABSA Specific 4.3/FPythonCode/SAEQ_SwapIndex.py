
"""

    Date                : 2011-06-09
    Purpose             : benchmark delta of TRS on 'ZAR/TRaCI' equity index
    Department and Desk : Equities 
    Requester           : Shameer Sukha
    Developer           : Anil Parbhoo
    CR Number           : 677676


History:
Herman Hoon : FPythonCode for benchmark delta in the case of a TRS where reference is a equity index

"""


import acm
cs= acm.Calculations().CreateStandardCalculationsSpaceCollection()

def calc_bm(object, *temp):
    swap = get_swap(object)
    if swap:
        ins_calc = swap.Calculation()
        return ins_calc.InterestRateBenchmarkDelta(cs).Number()
    return 0

def get_swap(object):
    indexLeg = None
    if object.IsKindOf('FTotalReturnSwap'):
        indexLeg = object.FirstTotalReturnLeg().IndexRef()
    elif object.IsKindOf('FIndex'):
        indexLeg = object
        
    if indexLeg.IsKindOf('FIndex'):
        if len(indexLeg.Instruments()) == 1:
            ins = indexLeg.Instruments().At(0)
            if ins.IsKindOf('FSwap') or ins.IsKindOf('FFra'):
                return ins
        if len(indexLeg.Instruments()) != 1:
            return indexLeg
    




    return None
