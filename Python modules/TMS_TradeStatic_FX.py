import ael, os, acm
from TMS_Functions import Get_BarCap_Book_ID
import FBDPCommon
import SANLD_NOMINALCURR
from TMS_Functions_Common import EnumFXCash

'''=========================================================================================================
    Purpose		: This Module is used for extracting Trade Static Data from all trades as retreived
                        : by the trade filter NLD_All_Trades. This data will be sent to the EOD data repository 
                        : for use by EOD and CRE FX
    Department and Desk	:
    Requester		: Mathew Berry
    Developer		: Babalo Edwana
    CR Number		: 261644
    
    Changes		: Added logic to include currency pair for the trades as required by EOD Api.
    Developer		: Babalo Edwana
    Date                : 06/04/2010
    CR Number		: 279327

    Changes		: Refactored to allow usage for FX trades (MOPL) and all trades (CRE).
    Developer		: Balazs Juraj
    Date              : 04/10/2011
    CR Number		: 789095
    
=========================================================================================================='''

HEADER = "Trade,Instrument_Type,Portfolio,Counterparty,CurrencyPair\n"

def isFXSwap(trade):
    acmTrade = acm.FTrade[trade.trdnbr]
    instr = acmTrade.Instrument()
    if acmTrade.IsFxSwapNearLeg() or acmTrade.IsFxSwapFarLeg():
        return acmTrade
                
def getFXHedgeCurrPair(trade):
    if trade:
        instr = trade.insaddr
        baseCcy = SANLD_NOMINALCURR.get_nomcurr_final(trade)
        if isFXSwap(trade):
            baseCurr = baseCcy
            quotedCurr = baseCcy == trade.curr.insid and trade.insaddr.curr.insid or trade.curr.insid
        else:
            baseCurr  = baseCcy == instr.curr.insid and instr.curr.insid or trade.curr.insid
            quotedCurr = baseCcy == instr.curr.insid and trade.curr.insid or instr.curr.insid
            
        return (baseCurr + quotedCurr)

def getFXOptionCurrPair(trade):
    if trade:
        instr = trade.insaddr
        und_instr = instr.und_insaddr
        
        if und_instr:
            baseCurr  = instr.curr.insid
            quotedCurr = instr.strike_curr.insid
        
        return (baseCurr + quotedCurr)
        

def getCurrencyPair(trade):
    if trade:
        baseCurr = ""
        quotedCurr = ""
        
        acmFTrade = acm.FTrade[trade.trdnbr]
        acmFCurrencyPair = acmFTrade.CurrencyPair()
        
        if acmFCurrencyPair:
            baseCurr = acmFCurrencyPair.Currency1().Currency().Name()
            quotedCurr = acmFCurrencyPair.Currency2().Currency().Name()
        else:
            instr = trade.insaddr
            if instr.instype == "Option":
                return getFXOptionCurrPair(trade)
                
            if instr.instype == "Curr":
                return getFXHedgeCurrPair(trade)
                           
        return (baseCurr + quotedCurr)
                
        
def getFXSwapCurrencyPair(trade, instr):
    if trade and instr:
        Ccy2 = trade.curr.insid
        for leg in instr.legs():
            if not leg.payleg:
                Ccy1 =  leg.curr.insid
            
        return Ccy1 + Ccy2
        
def SaveTradeStatic2(file_path, include_header, trades):

    f = open(file_path, "wt")
    try:
        print "-- Getting trade data --"

        if include_header: f.write(HEADER)
        
        for trd in trades:
            
            instr = trd.insaddr
            if instr.instype == "Combination":
                    ins = acm.FCombination[instr.insid]
                    for c_instr in acm.FCombination[instr.insid].Instruments():
                        for c_trade in c_instr.Trades():
                            trade_com = FBDPCommon.acm_to_ael(c_trade)
                            instr_com = FBDPCommon.acm_to_ael(c_instr)
                            if instr_com.instype == 'FxSwap':
                                trd_data = [trd.trdnbr, trd.insaddr.instype, trd.prfnbr.prfid, trd.counterparty_ptynbr.ptyid, getFXSwapCurrencyPair(trade_com, instr_com)]
                            else:
                                trd_data = [trd.trdnbr, trd.insaddr.instype, trd.prfnbr.prfid, trd.counterparty_ptynbr.ptyid, getCurrencyPair(trade_com)]
                            f.write( ",".join( [str(row) for row in trd_data] ) + "\n" )
                            
                            break
                        break
                            
            else:
                trd_data = [trd.trdnbr, trd.insaddr.instype, trd.prfnbr.prfid, trd.counterparty_ptynbr.ptyid, getCurrencyPair(trd)]
                f.write( ",".join( [str(row) for row in trd_data] ) + "\n" )
    finally:
        f.close()

    print "Done\nWrote to secondary output %s" % file_path


def SaveTradeStatic(date, server, filter, include_header):

    trades = ael.TradeFilter[filter].trades()
 
    FileDate = date.strftime('%y%m%d')
    file_path = os.path.join(server, "TMS_FX_Trade_Static_" + FileDate + ".txt")

    SaveTradeStatic2(file_path, include_header, trades)


