
import acm

ael_variables = []

def ael_main_ex(parameters, dictExtra):
    shiftVector = acm.CreateShiftVector('*', 'valuation add on', None)
    shiftVector.AddShiftItem(0.0, 'No Add-on')
    return [shiftVector]
