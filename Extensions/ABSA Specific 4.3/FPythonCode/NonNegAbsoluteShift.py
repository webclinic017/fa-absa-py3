
import acm

'''
Date                    : 2010-11-04
Purpose                 : New fixed value shift type for dividend scenarios to return non neg simulated dividends.
Department and Desk     : SM PCG - Valuation Control
Requester               : Masawi, Chipo
Developer               : Rohan van der Walt
CR Number               : 485065 (ABITFA-294)
'''

def NonNegAbsShift(dividends, shift):
    result = acm.FDenominatedValueArray()
    if dividends.IsKindOf("FDenominatedValueArray"):
        for curDiv in dividends:
            newDiv = acm.DenominatedValue(max(0, curDiv.Number() + shift), curDiv.Unit(), curDiv.Type(), curDiv.DateTime())
            result.AddDV(newDiv)
    else:
        newDiv = acm.DenominatedValue(max(0, dividends.Number() + shift), dividends.Unit(), dividends.Type(), dividends.DateTime())
        result.AddDV(newDiv)
    return result

