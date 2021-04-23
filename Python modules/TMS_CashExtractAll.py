"""
Purpose:   This Module is used as an Interface for running
           TMS_CashExtract_FX and TMS_TradeStatic_FX FOR ALL NON_VOID TRADES (not only FX ones)
Requester: Mathew Berry
Developer: Balazs Juraj
CR Number: 789095

Changes:   Skip Cash Payment trades
Developer: Frantisek Jahoda
Date:      4/11/2015
CR Number: 3235450
"""

import ael
import acm
import os

from TMS_Config_Trade import EnumTradeType, isValidStatus
from TMS_TradeStatic_FX import SaveTradeStatic2
from TMS_CashExtract_FX import write_cash_file

from DateUtils import PDate
from datetime import datetime

def getPrfNbrs():
    ais = ael.AdditionalInfoSpec["BarCap_TMS_Feed"]
    ai_recs = ael.AdditionalInfo.select("addinf_specnbr=%i" % ais.specnbr)
    return (ai.recaddr for ai in ai_recs if ai.value == "Production")

def getTrades(prfnbrs):
    trades = []
    for prfnbr in prfnbrs:
        for t in ael.Trade.select("prfnbr=%i" % prfnbr):
            if (isValidStatus(EnumTradeType.PRODUCTION, t.status)
                    and t.status != 'Void'
                    and t.insaddr != t.curr):
                trades.append(t)
    return trades

def SavePortfolioMapping(filename, prfnbrs):

    ais = ael.AdditionalInfoSpec["BarCap_SMS_SB_Name"]

    f = open(filename, "wt")
    try:
        print("-- Getting portfolio mappings --")

        f.write("Portfolio,SMS Book\n")
        for prfnbr in prfnbrs:
            prf = ael.Portfolio[prfnbr]
            aiList = [ai.value for ai in prf.additional_infos() if ai.addinf_specnbr.specnbr == ais.specnbr]
            bookId = len(aiList) and aiList[0] or ("AB%s" % prf.prfid)
            f.write("%s,%s\n" % (prf.prfid, bookId.strip()))

        print(("Done\nWrote to secondary output %s" % filename))

    finally:
        f.close()

def main(repDate, path, noStatic=False):
    prfnbrs = sorted( getPrfNbrs() )
    print("Found %i portfolios" % len(prfnbrs))

    if not noStatic:
        fn = os.path.join(path, "EOD_Portfolio_SMSBook_%s.txt" % repDate.strftime('%y%m%d'))
        SavePortfolioMapping(fn, prfnbrs)

    trades = getTrades(prfnbrs)
    print("Found %i trades" % len(trades))

    if not noStatic:
        fn = os.path.join(path, "EOD_RealisedCash_TradeStatic_%s.txt" % repDate.strftime('%y%m%d'))
        SaveTradeStatic2(fn, 1, trades)

    fn = os.path.join(path, "EOD_RealisedCash_TradeCcyBalances_%s.txt" % repDate.strftime('%y%m%d'))
    acm_trades = [acm.FTrade[trade.trdnbr] for trade in trades]
    write_cash_file(fn, acm_trades, repDate)

    print("Done")

ael_variables = [("repdate", "Reporting Day", "string", None, None, 0, 0),
                 ("server", "Server Location", "string", None, "C:\\temp", 1, 0),
                 ("noStatic", "Exclude Static Data", "bool", ["Yes", "No"], "No", 1, 0)]

def ael_main(ael_dict):
    d = ael_dict["repdate"] and datetime.strptime(ael_dict["repdate"], '%y%m%d') or ael.date_today()
    main(PDate(d), ael_dict["server"], ael_dict["noStatic"])

    print("print Completed Successfully ::")
