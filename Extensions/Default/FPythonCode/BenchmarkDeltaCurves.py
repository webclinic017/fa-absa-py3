
import acm

def spreadAndBenchmarkCurves():
    curves = acm.FArray()
    curves.AddAll(acm.FSpreadCurve.Select(""))
    curves.AddAll(acm.FBenchmarkCurve.Select(""))
    curves.AddAll(acm.FInflationCurve.Select(""))
    return curves.Sort()
