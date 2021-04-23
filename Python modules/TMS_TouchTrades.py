''' =======================================================================
    TMS Touch Trades

    This module is used to touch an additional info field on a group of 
    trades such as to send those trades through to TMS.
    
    Eben Mare
    ======================================================================= '''

import ael

from TMS_Config_Trade import *
from TMS_Functions import TMS_Filter

from pprint import pprint
from time import clock

def isConsidered(trade, force):
    #Skip checking neccesary pre-post conditionas if we are forcing the trade through
    if force: return 1

    #Determine the desk of the trade and do the correct check
    return TMS_Filter(trade, trade.insaddr)

def TouchTrades(trades, force = 0):
    status = {}
    for trade in trades:
        #Only send the trade if it satisfies the neccesary conditions
        if isConsidered(trade, force):
            status[trade.trdnbr] = TouchTrade(trade, __name__)
        else:
            status[trade.trdnbr] = "Trade Not Considered for CRE"

    return status

# ################
# User Interface
# ################

ael_variables = [("tf", "Trade Filter", "string", [tf.fltid for tf in ael.TradeFilter], "", 1, 0),
                 ("log", "Log File Name", "string", None, r"C:\temp\touched_log.txt", 1, 0),
                 ("force", "Force", "bool", [0, 1], 0, 1, 0)]

def ael_main(ael_dict):
    tic = clock()
    results = TouchTrades(ael.TradeFilter[ael_dict["tf"]].trades(), ael_dict["force"])

    file = open(ael_dict["log"], "w")
    try:
        file.write( "\n".join( ["%d: %s" % (k, results[k]) for k in results.keys()] ))
    finally:
        file.close()

    print("Done in %f seconds" % (clock() - tic))
    print("Processed %d trades. Please see %s for more detail." % (len(results), ael_dict["log"]))
