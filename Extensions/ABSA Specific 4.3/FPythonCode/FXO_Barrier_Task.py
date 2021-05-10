import acm
import FXO_Barriers as main
        
ael_gui_parameters = {'windowCaption':'CRE FXO Barrier Trades processing'}

def listOfTradeFilters():
    return acm.FStoredASQLQuery.Select('')

ael_variables = [
['tf', 'Trade Query', acm.FStoredASQLQuery, listOfTradeFilters(), None, 0, 0, 'Trade Query Folder to process', None, 1]]

def ael_main(dict):
    trades =  dict['tf'].Query().Select()
    if trades:
        main.ProcessKnockInBarriers(trades)
