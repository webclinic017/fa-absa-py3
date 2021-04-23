import acm
import ael
import string
import smtplib
from at_email import EmailHelper

def process_Notification(email_from, email_to, tradeNumber, error):
    email_host = acm.GetCalculatedValue(0, acm.GetDefaultContext().Name(),
            'mailServerAddress').Value()
    email_body = string.join((
        "From: %s" % email_from,
        "To: %s" % email_to,
        "Subject: Front Arena Error - FX Cash Discounting Type on trade "+str(tradeNumber),
        "", str('The following issue was experienced on trade '+str(tradeNumber)+' with error: '+str(error))), "\r\n")
    if not email_host:
        raise Exception("Could not initialise the smtp Host")
    server = smtplib.SMTP(email_host)
    server.sendmail(email_from, email_to.split(','), email_body)
    server.quit()

def process_trade(t):
    acmTrade = acm.FTrade[t.trdnbr]
    
    print acmTrade.Oid(), acmTrade.Instrument().Currency().Name()
    disc_type_choice = ael.ChoiceList.read('list="DiscType" and entry="CCYBasis"')
    
    t = t.clone()
    t.disc_type_chlnbr = disc_type_choice
    
    if acmTrade.Portfolio().AdditionalInfo().Portfolio_Status() in ('Active', 'Non Standard'):
        if acmTrade.IsFxSwap():
            if acmTrade.IsFxSwapNearLeg():
                otherTrade = acmTrade.FxSwapFarLeg().Oid()
            else:
                otherTrade = acmTrade.FxSwapNearLeg().Oid()

            ot = ael.Trade[otherTrade]
            
            try:
                t.commit_fx_swap(ot)
            except Exception, e:
                print 'FX Swap commit Failed with error: {0}'
                process_Notification('FX Cash Deal Error upading the Discounting Type', 'ABCAPLiveITSupport@absacapital.com', ot.trdnbr, str(e))
        else:
            try:
                t.commit()
            except Exception, e:
                print 'Commit Failed with error:', str(e)
                process_Notification('FX Cash Deal Error upading the Discounting Type', 'ABCAPLiveITSupport@absacapital.com', acmTrade.Oid(), str(e))
    print 'Completed updating the Discounting Type on Front Arena trade', acmTrade.Oid()        
    return True

def updateFXCashTrades(temp, tradeNumber, *rest):
    tradeObj = ael.Trade[tradeNumber]

    if tradeObj.insaddr.instype == 'Curr':
        if tradeObj.disc_type_chlnbr and tradeObj.disc_type_chlnbr.entry == 'CCYBasis':
            print 'Received Trade {0} where Discount Type ChoiceList is set to CCYBasis. Trade will not be processed!'
        else:
                            # CFR needs to be distinguished in the logs, so check if this is a CFR tradtradeObj.
            is_cfr = False
            if tradeObj.counterparty_ptynbr and tradeObj.acquirer_ptynbr and (
                    'MIDAS DUAL KEY' in (tradeObj.counterparty_ptynbr.ptyid, tradeObj.acquirer_ptynbr.ptyid)):
                if tradeObj.prfnbr and (tradeObj.prfnbr.prfid.__contains__('MIDAS')):
                    if tradeObj.trader_usrnbr and tradeObj.trader_usrnbr.userid == 'STRAUSD':
                        is_cfr = True
                            
            if is_cfr:
                trade_type = 'CFR'
            else:
                trade_type = 'generic'

            
            return process_trade(tradeObj)

