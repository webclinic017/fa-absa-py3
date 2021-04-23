'''----------------------------------------------------------------------------------------------------------------------------------
# Purpose                       :  Script to amend the delivery date of FX Option trades coming in from YieldX
# Department and Desk           :  MO
# Requester                     :  Pedro de Moura
# Developer                     :  Bhavnisha Sarawan
# CR Number                     :  C
----------------------------------------------------------------------------------------------------------------------------------'''

import acm

ael_gui_parameters = {'hideExtracControls' : True,
                      'windowCaption' : 'Amend Pay Day Offset for FX Options'}
                      
ael_variables = [ ['Filter', 'Filter', acm.FTradeSelection, acm.FTradeSelection.Select(''), 'MO_YieldX_DeliveryDate', 0] ]

def SetDeliveryDate(inslist):
    for ins in inslist:
        try:
            ins_clone = ins.Clone()
            ins_clone.PayDayOffset(0)
            ins.Apply(ins_clone)
            ins.Commit()
        except Exception, e:
            print("Instrument: ", ins.Oid())
            print("Error in changing delivery date: ", e)

def GetListOfIns(tradeslist):
    inslist = []
    for trade in tradeslist.Trades():
        ins = trade.Instrument()
        if ins not in inslist:
            inslist.append(ins)
    return inslist

def ael_main(parameter):
    tradeslist = parameter['Filter']
    inslist = GetListOfIns(tradeslist)
    SetDeliveryDate(inslist)
    print('success|completed successfully')
