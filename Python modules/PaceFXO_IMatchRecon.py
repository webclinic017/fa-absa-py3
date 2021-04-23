"""Exports trades imported by PACE-FXO for IntelliMatch processing."""

# Desk   Requester        Developer              CR Number
# What
# =============================================================================

# OPS    PACE-FXO         Lukas Paluzga          CHNG0001203303
# Exports all open trades booked by PACE-FXO to a XML file. 
# This file is then feeded to IntelliMatch.
# See http://confluence.barcapint.com/display/AbCapFxIT/Environments for details.

import os, re, sys, time
from itertools import groupby
from xml.etree import ElementTree as ET

import acm, ael
import at
from at_logging import getLogger


LOGGER = getLogger(__name__)

PACE_FXO_FEEDID = 'PFXO'
"""Feed ID for PACE-FXO trades."""

TIMES = ['07:00', '10:30', '15:00', '18:22']
"""Times at which the reconciliation will be run."""

# mappings - do not modify
CASH_OR_DELIVERY_MAPPING = {
    'Cash': 'Cash',
    'Physical Delivery': 'Delivery',
    }
CUT_MAPPING = {
    'ECB 2:15 pm': 'ECB',
    'NY 10:00 am': 'NY',
    'TK 3:00 pm': 'TKY',
    'BFIX NYK 10:00AM': 'NYK',
    }
PRICEUNITS_MAPPING = {
    'Points of UndCurr': '{0} pips',
    'Pct of Nominal': '% {0}',
    }
TYPE_MAPPING = {
    'None': 'vanilla',
    'Other': 'barrier',
    }

blgd = acm.FBusinessLogicGUIDefault() 


def trade_to_xml(t):
    """Convert ACM trade to xml."""
        
    ins = t.Instrument()
    
    root = ET.Element('Trade')
    id = t.OptionalKey().split('_')[1] # Unique ID of the trade from PACE (e.g. PFXO_1212121)
    if id.endswith(":H"): # optkey may look like PFXO_1212121:H. We're not interested in Hs.
        id = id[:-2]
    root.attrib['id'] = id         
    
    def sub(name, value):
        """Creates a sub-element with root as parent."""
        el = ET.SubElement(root, name)
        el.text = str(value)
        return el
    
    is_hedge = ins.InsType() == at.INST_CURR
    
    extype = ins.ExoticType()
    root.attrib['type'] = 'hedge' if is_hedge else TYPE_MAPPING[extype]
        
    sub('_faoid', t.Oid())                # Front Arena ID
    # Hedge (FX Spot)
    sub('face', abs(t.Nominal()))              # Face nominal of the trade
    sub('strike', t.Price() if is_hedge else ins.StrikePrice())      # Strike of the Option
    if is_hedge:
        sub('delivery', t.ValueDay())         # Delivery date of the trade cash
    sub('faceccy', t.Currency().Name())   # Currency of the trade
    is_buy = t.Quantity() > 0
    sub('buy-sell', 'Buy' if is_buy else 'Sell') # Direction of the trade
    sub('homeccy', t.Currency().Name() if is_hedge else ins.Currency().Name()) # Domestic currency
    sub('foreignccy', ins.Currency().Name() if is_hedge else ins.Underlying().Name()) # Foreign currency
    sub('cpty', t.Counterparty().Name())  # Counterparty of the trade
    salesperson = t.SalesPerson()
    sub('salesId', salesperson.Name() if salesperson else '')  # Sales person on the trade
    sub('homeccyamt', abs(t.Premium()) if is_hedge else 0)        # Domestic amount on the hedge trade
    sub('foreignccyamt', abs(t.Quantity()) if is_hedge else 0)    # Foreign amount on the hedge trade
    sub('linked_deal_id', '')             # Trade type ==  PACE closing trade ? Contract Ref (deal id): leave tag as blank

    if not is_hedge: # FX Option
        insdec = acm.FOptionDecorator(ins, blgd)
    
        root.attrib['type'] = TYPE_MAPPING[extype]  # Type of message (Vanilla, Barrier)
        
        # Vanilla (in terms of fields is an extension of Hedge)
        sub('delivery', insdec.DeliveryDate())
        sub('cut', CUT_MAPPING[ins.FixingSource().Name()])      # location of expiry for time
        sub('expiry', ins.ExpiryDateOnly())                     # Expiry of the Option
        sub('ccypair', ins.Underlying().Name() + ins.Currency().Name())     # Currency pair of the Option
        sub('call-put', "{0} {1}".format(ins.Underlying().Name(), ins.OptionType())) # Trading a Put or a Call
        sub('premiumdate', t.ValueDay())                        # Value day of the trade
        priceunits = PRICEUNITS_MAPPING[ins.Quotation().Name()].format(t.Currency().Name())
        sub('priceunits', priceunits) # Quotation type of the trade
        sub('cashordelivery', CASH_OR_DELIVERY_MAPPING[ins.SettlementType()]) # Type of settlement
        sub('spotdate', t.ValueDay())                           # Date that includes the spot days after trade date
        sub('base_notional', abs(round(t.Quantity(), 2)))       # Foreign amount
        sub('ctr_notional', abs(round(t.Quantity() * ins.StrikePrice(), 2))) # Domestic amount
        sub('expirydays', insdec.ExpiryCalendarPeriod())        # Number of days till expiry 
        sub('deliverydays', insdec.DeliveryCalendarPeriod())    # Number of days till delivery 
        sub('premiumccy', t.Currency().Name())                  # Currency that the premium is in
        sub('modeldate', at.date_to_ymd_string(t.TradeTime()))  # Trade date
        sub('midpreminpremccy', t.Premium())                    # Premium amount
        sub('midpriceinpremccy', t.Price())                     # Premium price
        sub('softskim', t.SalesCredit())                        # Sales credit1
        sub('hardskim', t.AdditionalInfo().ValueAddCredits() or 0) 
        sub('comments', '')                                     # Any comments that the client enters
        sub('sdsId', t.Counterparty().AdditionalInfo().BarCap_SMS_CP_SDSID()) # Id associated with the counterparty
        sub('counterparty', t.Counterparty().Name())            # Counterparty name  
        sub('tradetime', t.TradeTime())                         # Trade time 
        
        if extype == 'Other': # Barrier...
            # Barrier (in terms of fields is an extension of Vanilla)
            sub('barrtype', ins.Exotic().BarrierOptionType()) # Type of Barrier
            sub('barrier', ins.Barrier())                         # Barrier rate
            sub('closing_status', '')                             # Trade type =='PACE closing trade' ? 'CLOSING' : blank
            
    return root


def get_trade(pfxo_trade_id):
    """Get FTrade given PaceFXO trade id."""
    key = '{0}_{1}'.format(PACE_FXO_FEEDID, pfxo_trade_id)
    t = acm.FTrade.Select01('optionalKey="{0}"'.format(key), None)
    return t or acm.FTrade.Select01('optionalKey="{0}"'.format(key + ":H"), None)


def get_trades():
    """Return all trades in PACE-FXO deal where there is at least one trade with delivery date >= today."""
    addinfos = at.addInfo.find('Source System', PACE_FXO_FEEDID)
    all_pfxo_trades = [acm.FTrade[ai.Recaddr()] for ai in addinfos]
    final_trades = set()
    
    now = acm.Time.DateNow()
    
    for trade in all_pfxo_trades:
        if trade in final_trades:
            continue
            
        if trade.Status() in [at.TS_SIMULATED, at.TS_VOID]:
            continue
            
        ins = trade.Instrument()
        if not ins.IsKindOf(acm.FOption): # We will include the hedges (FX cash) using the deal lookup below.
            continue
            
        insdec = acm.FOptionDecorator(ins, blgd)
        if insdec.DeliveryDate() < now:
            continue
            
        # We found a trade in deal with delivery date >= today. Now we include all trades in deal
        dealid = trade.AdditionalInfo().PACE_FXO_DEALID()
        if dealid:
            for ai in at.addInfo.find('PACE_FXO_DEALID', str(dealid)):
                dealtrade = acm.FTrade[ai.Recaddr()]
                if dealtrade.Status() in [at.TS_SIMULATED, at.TS_VOID] or \
                        PACE_FXO_FEEDID not in dealtrade.OptionalKey():
                    continue
        
                final_trades.add(dealtrade)
        else: # Trades booked in the past do not have deal id set. Include at least the option.
            final_trades.add(trade)
    
    return list(final_trades)

ael_variables = at.ael_variables.AelVariableHandler()
ael_variables.add('output_folder', label = 'Output folder')
ael_variables.add('time', label = 'Time', mandatory = 1, collection = TIMES)
ael_variables.add('date', label = 'Date', mandatory = 0)

def ael_main(params):
    LOGGER.msg_tracker.reset()
    trades = get_trades()
    root = ET.Element('reconciliation')
    deal = ET.SubElement(root, 'Deal')
    deal.attrib['id'] = "0" # Not used for reconciliation. Probably can be removed but that would change the XML structure.
    
    trades = sorted(trades, key=lambda trade: trade.OptionalKey())
    for trade in trades:
        try:
            xml = trade_to_xml(trade)
            if xml is not None:
                deal.append(xml)
        except Exception as exc:  # Seriously.
            LOGGER.exception("ERROR on trade %d: %s", trade.Oid(), exc)
    
    xml_string = ET.tostring(root)
    if not params.get('output_folder'):
        print xml_string
        return
    
    fulldate = at.date_to_datetime('{0} {1}:00'.format(at.date_to_ymd_string(params['date'] or acm.Time.DateNow()), params['time']))
    file_name = os.path.join(params['output_folder'], "PACEFXO_Recon_File_{0}.xml".format(fulldate.strftime('%y%m%d%H%M%S'))) 
    with open(file_name, 'wb') as f:
        f.write(xml_string)
    
    LOGGER.info("XML recon written to %s", file_name)
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")
    
    LOGGER.info("Completed successfully.")
