'''
Name       : Mr_RecoveryRate
Developer  : Tshepo Mabena
Date       : 11-02-2009
Descripion : This module is used to calculate the difference in PV of a CD when the assuemd recovery rate is changed.
             The module is used by market risk on the credit derivatives desk. 
'''
import ael, acm

class CalcSpace(object):

    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def Recovery_Shift_Size(yc ,shiftsize, stf , syc , Party , dcount, dunit,*rest):
    
    yc=acm.FYieldCurve[syc]
    pv1 = 0
    pv0 = 0
    
    tf = acm.FTradeSelection[stf]
    
    for attribute in yc.Attributes():
        if str(attribute.AttributeName()) == Party:
        
            
            tf_calc = tf.Calculation()
            pv0=tf_calc.PresentValue(CalcSpace.calcSpace).Number()
            
            RecRate = attribute.Clone()
            
            RecRate.RecoveryRate = RecRate.RecoveryRate()+ shiftsize
            
            attribute.Apply(RecRate)
            #yc.simulate()
            pv1=tf_calc.PresentValue(CalcSpace.calcSpace).Number()
            attribute.Undo()
            #yc.unsimulate()
  
            pv01 = pv1 - pv0 
        
    return pv01
    
