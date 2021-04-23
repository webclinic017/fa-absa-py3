
import acm

def TestMethod():
   return "Hello World"
   
def CalcLegPV(trade, leg, curr):
    calc_space=acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    return leg.Calculation().PresentValueSource(calc_space, trade, curr).Value()
