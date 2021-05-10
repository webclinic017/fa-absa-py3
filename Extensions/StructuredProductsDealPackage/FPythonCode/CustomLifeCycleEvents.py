
import acm
import sys


# Not handled for accumulator:
#    - priceMode = market

def customExercise(grouping, testMode, priceMode):
    for grouperName in grouping:
        if grouperName == 'DealPackage':
            dp = acm.FDealPackage[grouping[grouperName]]
            if dp is not None:
                dpEdit = dp.Edit()
                if 'exercise' in dpEdit.TradeActionKeys():
                    cmdAction = dpEdit.TradeActionAt('exercise')
                    if cmdAction.Enabled():
                        dpAction = cmdAction.Invoke()[0]
                        dpAction.SetAttribute('exDate', acm.Time().DateToday())
                        dpAction.SetAttribute('doCommit', not testMode)
                        dpAction.SetAttribute('priceMode', priceMode)
                        dpAction.SetAttribute('useBdpLogme', True)
                        dpAction.Save()
                    return True
    return False
