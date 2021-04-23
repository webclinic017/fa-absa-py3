'''-----------------------------------------------------------------------
MODULE
    CSA_ValGroup
DESCRIPTION
    Developer           : Nidheesh Sharma
    Date                : 2012-03-28
    Purpose             : Trades taken from the MarkitWire listener to automatically correct the instrument's Val Group
                          Also checks if the current Val Group is correct (Functionality is added to a menu item - "Check Val Group")
    Change Number       : C157393
ENDDESCRIPTION

HISTORY
    When:       CR Number:      Who:                    What:                                                           Requestor:
    2012-06-05  C241870         Nidheesh Sharma         Updated Check Val Group Tool - Catered for CurrSwap valGroup    Theresa Offwood Le Roux
    2013-01-28  C761405         Jan Sinkora             Updated valgroup setting for LCH-cleared trades                 Manus van den Berg
-----------------------------------------------------------------------'''

import ael, acm
from SAGEN_IT_Functions import get_Port_Struct_from_Port

AC_GLOBAL_ID = 2178
ADDINFO_CLEARINGSTATUS = 'Clearing Status'

def otc_valgroup(curr_insid):
    """Return ValGroup based on currency.

    Note that this returns None if the currency is not recognized.
    That shouldn't happend with BAU trades.

    """
    if curr_insid in ('ZAR', 'USD', 'EUR', 'GBP'):
        return 'AC_OIS_{0}'.format(curr_insid)

def CSA_valGroup(trade, instrument):
    """Return the correct ValGroup."""
    svg = None

    if trade.add_info(ADDINFO_CLEARINGSTATUS) == 'Registered':
        # the trade has been cleared on LCH
        # ValGroup will be assigned according to the currency
        curr = trade.insaddr.curr.insid
        svg = otc_valgroup(curr)

    if not svg:
        # the trade has not been cleared on LCH
        # ValGroup is assigned based on the counterparty
        counterparty = trade.counterparty_ptynbr
        portfolio = trade.prfnbr
        #returns 1 or 0 - 1 is a match so exclude and 0 is a mismatch so include
        PB_Match = get_Port_Struct_from_Port(portfolio, 'PRIME BROKER')
        #get counterparty's add_info details - CSA, CSA Collateral Curr,CSA Type
        if counterparty:
            #trade filter conditions to exclude prime broker trades and prime services mirrored trades
            if counterparty.ptyid != 'PRIME SERVICES DESK' and PB_Match == 0:
                svg = CSA_CP_valGroup(counterparty, instrument, acm.FTrade[trade.trdnbr])

    return svg

#-------------------------------------------------------------------------
#A function to return the correct Val Group name of a counterparty
#-------------------------------------------------------------------------
def CSA_CP_valGroup(counterparty, instrument, trade):
    vg_mask = 'AC_OIS_<CCY>'

    csa = counterparty.add_info('CSA')
    csa_ccy = counterparty.add_info('CSA Collateral Curr')
    csa_type = counterparty.add_info('CSA Type')

    csa_switch_date = counterparty.add_info('CSA Switch Date')
    if csa_switch_date:
        csa_switch_date = ael.date_from_string(csa_switch_date)
        if csa_switch_date <= ael.date_from_string(acm.Time().AsDate(trade.TradeTime())):
            csa_ccy = counterparty.add_info('CSA CollateralCurr2')

    if csa == 'Yes':
        #do the check and create a new valGroup for the trade
        if csa and csa_type in ['Gold', 'Strong']:
            svg = vg_mask.replace('<CCY>', csa_ccy)
            #add _XCCY to the end of a CurrSwap valGroup
            if instrument.instype == 'CurrSwap':
                svg = '%s%s' %(svg, '_XCCY')
            return svg


#-------------------------------------------------------------------------
#A function to update the Val Group in an instrument
#-------------------------------------------------------------------------
def CSA_valGroup_Update(instrument, valGroupName):
    #check if correct Val Group is already being used - if so, no update required
    if not valGroupName == instrument.product_chlnbr.entry:

        #check if new valGroup already exists
        valGroups = ael.ChoiceList['ValGroup'].members()
        valGroupExists = 'false'
        for valGroupMember in valGroups:

            #valGroup exists so use that valGroup
            if valGroupName == valGroupMember.entry:
                valGroupExists = 'true'
                instrument_clone = instrument.clone()
                instrument_clone.product_chlnbr = valGroupMember.seqnbr
                instrument_clone.commit()
                ael.poll()
                break

        #if valGroup doesnt exist, use AC_GLOBAL as default
        if valGroupExists == 'false':
            AC_GLOBAL = ael.ChoiceList[AC_GLOBAL_ID]
            instrument_clone = instrument.clone()
            instrument_clone.product_chlnbr = AC_GLOBAL.seqnbr
            instrument_clone.commit()
            ael.poll()


#-------------------------------------------------------------------------
#A function that checks if the Val Group is correct and notifies the trader
#-------------------------------------------------------------------------
def CheckValGroup(eii):
    obj = eii.ExtensionObject()
    trade = obj.OriginalTrade()
    if trade:
        instrument = trade.Instrument()
        valGroupName = CSA_valGroup(ael.Trade[trade.Oid()], ael.Instrument[instrument.Name()])

        #check if the Val Group selected by trader is correct
        if instrument.ValuationGrpChlItem().Name() == valGroupName:
            func=acm.GetFunction('msgBox', 3)
            func("Val Group Check", "Val Group is correct", 0)
        else:
            #check if new valGroup already exists
            valGroups = ael.ChoiceList['ValGroup'].members()
            valGroupExists = 'false'
            for valGroupMember in valGroups:

                #valGroup exists so use that valGroup
                if valGroupName == valGroupMember.entry:
                    valGroupExists = 'true'
                    func=acm.GetFunction('msgBox', 3)
                    func("Val Group Check", "Val Group should be "+valGroupName, 0)
                    break

            #if valGroup doesnt exist, use AC_GLOBAL as default
            if valGroupExists == 'false':
                #valGroup doesnt exist, and is already default AC_GLOBAL
                if instrument.ValuationGrpChlItem().Name() == 'AC_GLOBAL':
                    func=acm.GetFunction('msgBox', 3)
                    func("Val Group Check", "Val Group is correct", 0)
                #valGroup doesnt exist, is not AC_GLOBAL so recommend AC_GLOBAL as default
                else:
                    func=acm.GetFunction('msgBox', 3)
                    func("Val Group Check", "Val Group should be AC_GLOBAL", 0)

    else:
        func=acm.GetFunction('msgBox', 3)
        func("Val Group Check", "No trade is open to complete check", 0)


#-------------------------------------------------------------------------
#A function that monitors trades from the specified filter called by the MarketWire_Listener Module
#-------------------------------------------------------------------------
def CSA_ValGroup_Trades(o, e, arg, op):
    if e.record_type == 'Trade' and op != 'delete':
        ins = e.insaddr
        insid = ins.insid
        instrument = ael.Instrument[insid]

        svg = CSA_valGroup(e, instrument)

        if svg:
            CSA_valGroup_Update(instrument, svg)

