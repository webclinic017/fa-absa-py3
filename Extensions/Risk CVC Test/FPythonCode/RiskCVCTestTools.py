
import acm

def RiskFactorsAsString(riskFactors):
    if len(riskFactors) == 1:
        if riskFactors[0] is  None:
            return ""
    copy = []
    copy.extend( riskFactors )
    copy.sort()
    arr = acm.FArray()
    arr.AddAll(copy)
    return str(arr)
