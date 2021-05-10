"""-----------------------------------------------------------------------------
MODULE
    PS_RepoBonds_BSBBooker

DESCRIPTION
    Date                : 17 May 2013
    Purpose             : BuySellBack booking functions
    Department and Desk : Prime Services Desk
    Requester           : Francois Henrion & Kelly Hattingh
    Developer           : Peter Fabian
    CR Number           : CHNG0001033361
    
NOTES
    This code is based on code in cm_BuySellBackProcess script which 
    probably already works well in Prod. 
    
HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2013-05-27 C1056001     Peter Fabian       Adjustable price for BSB booking (YMtM column)
2013-07-26 C1197225     Peter Fabian       Add support for transactions and non-mirror BSBacks

ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import acm
import ael
import FBDPCommon

def _createBuySellBackInstrument(startDate, endDate, rate, underlying, businessLogicHandler, transaction):
    """ Creates a BSB instrument with specified parameters.
        Returns instrument and its decorator objects.
    """
    valuationGroup = acm.FChoiceList.Select01("list = 'ValGroup' and name ='AC_GLOBAL_Bonds'", None)

    instrument = acm.FBuySellBack()
    decorator = acm.FBuySellBackDecorator(instrument, businessLogicHandler)
    decorator.StartDate(startDate)
    decorator.ExpiryDate(endDate)
    decorator.Rate(rate)
    decorator.Underlying(underlying)
    decorator.DayCountMethod('Act/365')
    # since used price for corpbonds is nan, we set the ref price and ref value later
    decorator.ValuationGrpChlItem(valuationGroup)
    instrument.Commit()
    if transaction:
        transaction.append(instrument)
    return instrument, decorator

def _bookBuySellBackTrade(startDate, endDate, portfolio, underlying, amount,
                          rate, acquirer, ctpty, cp_prf, tradeDate, startPrice,
                          businessLogicHandler, transaction, status):
    """ Creates a BSB instrument and trade on the instrument according to 
        specified parameters. Creates a mirror trade if cp_prf is specified.
        
        Returns list of created trades (in case of creating mirror trades, there are two)
        
        Adds all the created objects to the transaction list so it can be rolled back
        in some custom way as one can't create BSBack instruments and trades in an acm
        transaction.
    """
    instrument, instrumentDecorator = _createBuySellBackInstrument(startDate, endDate,
                                                                   rate, underlying,
                                                                   businessLogicHandler,
                                                                   transaction)
    trade = acm.FTrade()
    tradeDecorator = acm.FTradeLogicDecorator(trade, businessLogicHandler)
    tradeDecorator.Instrument(instrument)
    tradeDecorator.Currency(instrument.Currency())
    tradeDecorator.TradeTime(tradeDate)
    tradeDecorator.Acquirer(acquirer)
    tradeDecorator.Portfolio(portfolio)
    tradeDecorator.Counterparty(ctpty)
    tradeDecorator.AcquireDay(startDate)
    tradeDecorator.ValueDay(startDate)
    tradeDecorator.HaircutType('Discount')
    tradeDecorator.Quantity(amount)
    tradeDecorator.Status(status)
    tradeDecorator.Text1('AutoRepo Process')
    tradeDecorator.Price(startPrice)
    tradeDecorator.Trader(acm.User())
    if cp_prf:
        tradeDecorator.MirrorPortfolio(cp_prf)
    tradeDecorator.PremiumCalculationMethod(acm.EnumFromString("PremiumCalculationMethod", "Price"))
    trade.Commit()
    if transaction:
        transaction.append(trade)
    if cp_prf:
        mirrorTrade = trade.MirrorTrade()
        if transaction:
            transaction.append(mirrorTrade)

    # These calculations aren't available in ACM, therefore accessing them using the AEL trade object
    ael_trade = FBDPCommon.acm_to_ael(trade)
    tradeDecorator.Premium(ael_trade.premium_from_quote(ael.date(startDate), trade.Price()))
    instrumentDecorator.RefPrice(ael_trade.buy_sellback_ref_price())
    instrumentDecorator.RefValue(ael_trade.buy_sellback_ref_value(1))
    instrument.Commit()


    return [trade.Oid(), mirrorTrade.Oid()] if cp_prf else [trade.Oid()]

def bookBsb(startDate, endDate, repoRate, underlying, qty, portfolio, acquirer,
            ctpty, cp_prf, tradeDate, acquireDate, startPrice, transaction, 
            status='Simulated'):
    """ Creates a BSB instrument and trade on the instrument according to 
        specified parameters. Creates a mirror trade if cp_prf is specified.
        
        Returns list of created trades (in case of creating mirror trades, there are two)
        
        Adds all the created objects to the transaction list so it can be rolled back
        in some custom way as one can't create BSBack instruments and trades in an acm
        transaction.
    """
    businessLogicGUIDefaultHandler = acm.FBusinessLogicGUIDefault()

    tradeNumbers = _bookBuySellBackTrade(startDate, endDate, portfolio,
            underlying, qty, repoRate, acquirer, ctpty, cp_prf, tradeDate, startPrice,
            businessLogicGUIDefaultHandler, transaction, status)
    if cp_prf:
        acm.LogAll('    Booked Buy-Sell-Back for portfolio %(portfolio)s,'
                ' instrument %(instrument)s, amount %(amount)f:'
                ' %(tradeNumber)i, %(mirrorNumber)i' %
                {'portfolio': portfolio.Name(),
                 'instrument': underlying.Name(), 'amount': qty,
                 'tradeNumber': tradeNumbers[0], 'mirrorNumber': tradeNumbers[1]}
            )
    else:
        acm.LogAll('    Booked Buy-Sell-Back for portfolio %(portfolio)s,'
                ' instrument %(instrument)s, amount %(amount)f: '
                '%(tradeNumber)i' %
                {'portfolio': portfolio.Name(),
                 'instrument': underlying.Name(), 'amount': qty,
                 'tradeNumber': tradeNumbers[0]}
            )
    return tradeNumbers

