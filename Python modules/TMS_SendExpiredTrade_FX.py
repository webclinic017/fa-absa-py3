import ael
import TMS_TouchTrades_FX
from time import clock

'''=======================================================================================
    Purpose        : This Module touches expired trades in front in order for the expired trade
                        : status to be sent to TMS
    Department and Desk    :
    Requester        : Mathew Berry
    Developer        : Babalo Edwana
    CR Number        : 261644
    
    Changes        : Remove log parameter  and loggin to external file, front arena scheduling implements its own logging.
    Date            : 18/05/2010
    Developer        : Babalo Edwana
    Requester        : Mathew Berry
    CR Number        : 314825
    
    Changes        : Added extra parameter to force trades to be touched.
    Date            : 06/07/2010
    Developer        : Babalo Edwana
    Requester        : Mathew Berry
    CR Number        : 363019

=========================================================================================='''

def TMS_SendExpiredTrades_FX(trdFilter, repDate,force = 1):
    status = {}
    for trade in ael.TradeFilter[trdFilter].trades():
        if TMS_TouchTrades_FX.isConsidered(trade, force) and canTouchTrade(trade, repDate):
            try:
                near_trade = trade
                far_trade = TMS_TouchTrades_FX.getOtherTrade(trade)
                status[trade.trdnbr] = TMS_TouchTrades_FX.FX_TouchTrade(near_trade, far_trade, __name__)
                
            except:
                print "The trade %i wasn't touched succesfully" % trade.trdnbr
    
    return status
	
def canTouchTrade(trade, repDate):
    instr = ael.Instrument[trade.insaddr.insaddr]
    if instr.instype == "Curr": 
        if trade.value_day == repDate:
            return True
    else:
        if instr.exp_day == repDate:
            return True
	
    return False

# ################
# User Interface
# ################
    
ael_variables = [('ReportDate', 'ReportDate', 'date', None, ael.date_today().add_days(-1), 1),
                  ('TradeFilter', 'TradeFilter', 'string', None, 'TMS_NLDIR_Opt', 1)]
                  
def ael_main(ael_dict):

    ReportDate = ael_dict["ReportDate"]
    TradeFilter = ael_dict["TradeFilter"]
    
    tic = clock()
    
    results = TMS_SendExpiredTrades_FX(TradeFilter, ReportDate)
                
    print "Done in %f seconds" % (clock() - tic)
    print "Processed %d trades." % len(results)
			
	
                
