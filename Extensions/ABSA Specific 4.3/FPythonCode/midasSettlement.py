import acm
import re


foreFrontTradeSystems = ['ABL', 'AOL', 'BBA', 'BBL', 'BII', 'BLG', 'BPD', 'BPS', 'BRX', 'BXA', 'C2B', 'FAR', 'FXH', 'MCC', 'NFX', 'OWM', 'REU', 'SML', 'PHO', 'FTI', 'FTC', 'XTP', 'FFO']


def isValidInstrumentType(trade):
    instype = trade.Instrument().InsType()
    
    if instype == 'Curr':
        return True
    return False

def is4FrontTrade(trade):
    tradeSystem = trade.TradeSystem()
    
    if tradeSystem in foreFrontTradeSystems:
        return True
    else:
        return False


def isPortfolioMidasEnabled(portfolio):
    return portfolio and portfolio.AdditionalInfo().MidasSettleEnabled()


def isCFRPortfolio(portfolio_name):
    return 'MIDAS_' in portfolio_name


def isCashPayment(trade):
    if trade.Currency() == trade.Instrument():
        return True
    else:
        return False


def midas_settlement(trdnbr, prfid):
    """Returns True if trade is eligible for Midas settlement.
    The logic needs to be based on the trade number and the portfolio name.
    This is necessary for the Sparks ATS listener (Sparks_ATS_amendments.py).
    """
    trade = acm.FTrade[trdnbr]
    prf = acm.FPhysicalPortfolio[prfid]
    try:
        original_trdnbr = re.findall(r'CleanPnL_(.*)', trade.Text1())[0]
        return midas_settlement(original_trdnbr, prfid)
    except:
        pass
    if not trade or not prf:
        return False
    if isValidInstrumentType(trade):
        if is4FrontTrade(trade):
            if isPortfolioMidasEnabled(prf):
                return True
        elif isCFRPortfolio(prfid):
            return True
        elif isPortfolioMidasEnabled(prf) and not isCashPayment(trade):
            return True
    return False


def evaluate(trade):
    portfolio = trade.Portfolio()
    if not portfolio:
        return False
    return midas_settlement(trade.Oid(), portfolio.Name())


def fx_manual_check(trade):
    return evaluate(trade)


def is_midas_settled(trade, *rest):

    return acm.FTrade[trade.trdnbr].MidasSettlement()
