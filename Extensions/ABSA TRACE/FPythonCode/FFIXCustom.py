"""

FFIXCustom
Houses all hooks for FINRA FIX message customisations

History
=======
2020-11-10 Snowy Mabilu https://absa.atlassian.net/browse/ARR-85    Added the customisations for populate
                                                                    the party and counterparty

"""

import acm
from protocols import amba, tnp, Layer, fix
import log
import FRegulatoryLib
from FRegulatoryLib import TradeRegInfo


def get_parties_from_trade(trade):
    fields = {}
    try:
       fields = {"pty": "ASUS"}
    except Exception as e:
        errMsg = 'ADSReportTradeBase - get_parties_from_trade - line:%d exception:%s   (%s)' % (sys.exc_info()[-1].tb_lineno, type(e).__name__, e)
        log.error(errMsg)

    return fields

def setPartyMapping(bp, trade, fixMsg):
    buyer = FRegulatoryLib.TradeRegInfo(trade).us_buyer()
    seller = FRegulatoryLib.TradeRegInfo(trade).us_seller()
    if buyer and not seller:
        side = 1
        counterSide = 2
    elif not buyer and seller:
        side = 2
        counterSide = 1
    else:
        side = 2
        counterSide = 1

    parties = get_parties_from_trade(trade)
    if parties:
        try:
            pty = parties['pty']
        except Exception as e:
            errMsg = 'ADSReportTradeBase - tradeToPTR - line:%d exception:%s   \
            (%s)' % (sys.exc_info()[-1].tb_lineno, type(e).__name__, e)
            log.warning(errMsg)
    tradeNbr, OurOrTheir = getTradeNbrFromTradeReportID(str(fixMsg.TradeReportID))

    if fixMsg.TradeReportType == '6':
    # TradaCaptureReport for cancel will have only one side of trade
        fixMsg.NoSides = 1
        if pty:
            if OurOrTheir == 'O':
                fixMsg.Side[0] = side
                # For Our side reporting role will be same as exist in FrontArena
            elif OurOrTheir == 'T':
                fixMsg.Side[0] = counterSide
                # For Our side reporting role will be opposite of what exist in FrontArena
            fixMsg.OrderID[0] = trade.Oid()
            fixMsg.NoPartyIDs[0] = 1  # No Of Party IDs
            fixMsg.PartyId[0][0] = pty
            fixMsg.PartyRole[0][0] = 1 # 1 is for Executing Firm
            fixMsg.PartyIDSource[0][0] = 'C'
            # C = Generally accepted market participant identifier (e.g. FINRA mnemonic)

    else: # This case will handle New Trade and Amended Trade
        '''Trade in Front Arena: Cpy=John, Acquirer=[an Absa acquirer with an alias that \
            has the ASUS code], BUY.
            Report 1: We send BUY, code for ASUS and C.  We do not send client name or code.\
            This will be Our Trade
            Report 2: We send SELL, code for ASUS and A.  We do not send Absa/affiliate name\
            or code. This will be Their Trade
        '''
        fixMsg.NoSides = 2
        #Always set value to 2. One side for the Reporting party and one side for the Contra party
        if pty:
            if OurOrTheir == 'O':
                fixMsg.Side[0] = side
                # For Our side reporting role will be same as exist in FrontArena
                fixMsg.Side[1] = counterSide
                # For Their side reporting role will be same as exist in FrontArena
                cpty = 'C'
            elif OurOrTheir == 'T':
                fixMsg.Side[0] = counterSide
                # For Our side reporting role will be opposite of what exist in FrontArena
                fixMsg.Side[1] = side
                # For Our side reporting role will be opposite of what exist in FrontArena
                cpty = 'A'

            fixMsg.OrderID[0] = trade.Oid()
            fixMsg.NoPartyIDs[0] = 1
            # No Of Party IDs
            fixMsg.PartyId[0][0] = pty
            fixMsg.PartyRole[0][0] = 1
            # 1 is for Executing Firm
            fixMsg.PartyIDSource[0][0] = 'C'
            # C = Generally accepted market participant identifier (e.g. FINRA mnemonic
            fixMsg.OrderCapacity[0] = 'A'
            #This is used for Agency trading, used for client trading

            fixMsg.OrderID[1] = trade.Oid()
            fixMsg.NoPartyIDs[1] = 1  # No of party IDs
            fixMsg.PartyRole[1][0] = 17  # 17 is for Contra Firm
            fixMsg.PartyId[1][0] = cpty
            fixMsg.PartyIDSource[1][0] = 'C'

        else:
            log.warning("No reporting party found for trade %d " % trade.Oid())

    if fixMsg.TradeReportType == '5':
        fixMsg.OriginalNoPartyIDs = 1
        if parties:
            pty = parties['pty']
            if pty:
                fixMsg.OriginalPartyID[0] = pty
                fixMsg.OriginalPartyRole[0] = 1
                # 1 is for Executing Firm
                fixMsg.OriginalPartyIDSource[0] = 'C'
                # C = Generally accepted market participant identifier (e.g. FINRA mnemonic)

    return fixMsg

def getTradeNbrFromTradeReportID(TradeReportID):
    i = TradeReportID.find('_')
    tradeNbr = None
    side = None
    if i >= 0:
        side = TradeReportID[i+1]
        tradeNbr = TradeReportID[0:i]
    return tradeNbr, side
    

def getBpFromTrade(trade):
    if trade:
        bps = acm.FBusinessProcess.Select('subject_seqnbr = {}'.format(trade.Oid()))
        for bp in bps:
            if bp.StateChart().Name() == 'FTRACEStateChart_36':
                return bp
    return None
    
@fix.outgoing('TradeCaptureReport')
def handleTradeCaptureReport(fixMsg):
    TradeReportID = str(fixMsg.TradeReportID)
    tradeNbr, side = getTradeNbrFromTradeReportID(TradeReportID)
    trade = acm.FTrade[tradeNbr]
    bp = getBpFromTrade(trade) 
    setPartyMapping(bp, trade, fixMsg)
