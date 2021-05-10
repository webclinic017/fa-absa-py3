"""
Description
===========
Date                          :  
Purpose                       :  
Department and Desk           :  
Requester                     :  
Developer                     :  
CR Number                     :



"C:\Program Files\Front\Front Arena\ATS\ATS\ats.exe" -server "10.110.92.110:9101" -kerberos -module_name CFR_Trade_Subscription

History
=======

Date            CR              Developer               Description
====            ======          ================        =============

2016-10-27                      Andrei Conicov          Using at_logging and transactions
"""
import ael, acm, datetime

from at_logging import getLogger, ats_start, ats_stop

LOGGER = getLogger(__name__)
HANDLER = None  # this is the MQ handler

def start():
    global HANDLER
    HANDLER = ats_start("ATSEconTradeAmend")
    
    LOGGER.info('Starting Trade Subscription...')

    ael.Trade.subscribe(subscriber)

def stop():
    LOGGER.info('Stopping Trade Subscription...')
    ael.Trade.unsubscribe(subscriber)
    
    ats_stop(HANDLER)

def process_trade(t):
    acmTrade = acm.FTrade[t.trdnbr]
    disc_type_choice = ael.ChoiceList.read('list="DiscType" and entry="CCYBasis"')
    
    try:
        ael.begin_transaction()
        t = t.clone()
        t.disc_type_chlnbr = disc_type_choice
        
        if acmTrade.IsFxSwap():
            LOGGER.info("Processing FX Swap")
            if acmTrade.IsFxSwapNearLeg():
                otherTrade = acmTrade.FxSwapFarLeg().Oid()
            else:
                otherTrade = acmTrade.FxSwapNearLeg().Oid()
    
            ot = ael.Trade[otherTrade]
            t.commit_fx_swap(ot)
        else:
            t.commit()
        
        ael.commit_transaction()
        LOGGER.info('Commit Successful!')
    except Exception:
        LOGGER.exception("Commit failed")
        ael.abort_transaction()

    return True

def subscriber(o, e, arg, op):
    if e.record_type != 'Trade' or op != 'insert' or e.insaddr.instype != 'Curr':
        return

    if e.disc_type_chlnbr and e.disc_type_chlnbr.entry == 'CCYBasis':
        LOGGER.info('Received Trade %s where Discount Type ChoiceList is set to CCYBasis. Trade will not be processed!',
                    e.trdnbr)
        return
    
	# CFR needs to be distinguished in the logs, so check if this is a CFR trade.
    is_cfr = False
    if e.counterparty_ptynbr and e.acquirer_ptynbr and (
            'MIDAS DUAL KEY' in (e.counterparty_ptynbr.ptyid, e.acquirer_ptynbr.ptyid)):
        if e.prfnbr and (e.prfnbr.prfid.__contains__('MIDAS')):
            if e.trader_usrnbr and e.trader_usrnbr.userid == 'STRAUSD':
                is_cfr = True
	
    if is_cfr:
        trade_type = 'CFR'
    else:
        trade_type = 'generic'

    LOGGER.info('Received %s trade %s. Setting Discount Type ChoiceList to CCYBasis',
                trade_type, e.trdnbr)

    process_trade(e)

# start()
# stop()

