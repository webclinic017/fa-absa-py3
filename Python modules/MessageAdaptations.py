"""-----------------------------------------------------------------------------
MODULE	  MessageAdaptations

Version: 1.1

DESCRIPTION

This module is for adding calculated values or extra info to AMBA messages.
It is hooked in the amba.ini file on the Front Arena Server.
Changes to this AEL will only take effect if the AMBA Server Services are restarted.

History:
Date	    	    Who     	    	    	    	    What
2004-04-01  	    Anton van Staden	    	    Added BESA and Midbase info
                    Hardus Jacobs
                    Steyn Basson (CQS)
2004-04-15  	    Anton van Staden	    	    Re-Created AEL for more expandibility.
                    Hardus Jacobs
2004-05-26  	    Hardus Jacobs   	    	    Buy-Sellbacks
2004-06-30  	    Anton van Staden	    	    Add Split BTB Massage Source change
2009-05-12          Zaakirah Kajee                  Include Repo/reverse
2010-07-01          Francois Truter                 Excluded mirror trades (i.e. internal)
2011-06-09          Kim Madeley  (C680224)          include new add info called AgencyTradPrincipal for Neutron requirement from Prime
2011-07-25          Kim Madeley (C722939)           include Agency traded pricipal and internal flag for Buysellbacks, Frn and Bills
2011-08-23          Kim Madeley(C746813 - task )    check to see CP is not null - 2011 upgrade deployment
2012-11-20          Anwar Banoo                     all in price for FRN to besa is a mandatory non zero field, validation from besa was fixed with upgrade in
                                                    november, thus this was an existing bug and only now became an issue.\
2013-09-18          Anwar Banoo                     Open ended repo status moving to terminated is now catered for
2016-06-07          Anil Parbhoo                    Incorporate the 2 new field Companion_Bond and the corresponding Companion_Bond_Spread
                                                    and the 5 other new fields (Tap_Issue, Primary_Trade, Book_Over, Give_Up and Prime_Broker)
                                                    that will be defined as No even when the add_info value is blank.
                                                    the adapter is updated to cater for bigint type rather than int. However, we still want to define our own limit of 5bn
2016-10-26          Anil Parbhoo(CHNG0004036772)    Change to ensure that all the children of a split trade have add info values of the parent trade
2016-11-03          Anil Parbhoo(CHNG0004076622)    Block trades to the interface in the case where the counterparty host id is blank.
2016-11-10          Anil Parbhoo(CHNG0004086982)    new code for repos where the underlying instype is a FRN
2017-02-14          Tshepo Nkoana(CHNG0004297482)   Change templates on adaptor for 2nd leg of open-ended repo to be sent to Nutron when it is terminated.
2017-07-17          Anil Parbhoo(CHNG0004756426)    e-mail notification in the case where the face value of the trade is zero on the amba message even though it is not zero on the face of the tarde ticket
2017-07-21          Bushy Ngwako                    Function to Kill the AMBA Process when face value of the trade is zero on the amba message
2017-08-03          Anil Parbhoo (CHNG0004808708)   change e-mails for zero face value only from PROD
                                                    and (2) sent to besa trades and (3) not agg and not cash posting trade and (4) not internal suppress trade
2019-07-04          Henry Ngwaka                    Added additional logging to assist with production issues.
2019-10-24          Anil Parbhoo                    Change the e-mail address
2019-11-20          Anil Parbhoo (CHG0066843)       Dont send simulated, bo-bo confirm and bo confirm trades to the adapter                   
2019-11-25          Anil Prbhoo  (CHG0068839)       Suicide function should not be used for valid zero face value trades  
2020-01-16          Anil Parbhoo (CHG0074442)       Stop MessageAdaptations from killing it self in the case of a zero face value trade
2020-01-21          Anil Parbhoo (CHG0075772)       only send ZAR trades to the adaptor
2020-01-30          Jaysen Naicker (CHG0078530)     prevent Collateral trades from being sent the Besa adapter
2020-06-23          Anil Parbhoo (CHG0107956)       Prevent Euroclear trades from being sent to Besa adaptor 
2020-10-15          Anil Parbhoo (CHG0132240)       no longer import psutil module as the sucide function is no longer called
2020-10-22          Anil Parbhoo (CHG0133094)       include cp hostid and the jse instrument name in adaptations
ENDDESCRIPTION

-----------------------------------------------------------------------------"""

import string
import sys
import os
import traceback
import acm
import ael


from SAFI_BONDS_BESA import bond_iyl
from at_email import EmailHelper
from SAGEN_IT_Functions import get_Port_Struct_from_Port_list

acm.Log("System Path: %s" % sys.path)


def notify_Ops_RTB(tradeNumber, main, reason):
    TESTMESSAGES = True
    for item in ael.ServerData.select():
        if item.customer_name == 'Production':
            TESTMESSAGES = False
    environment = 'TEST' if TESTMESSAGES else 'PROD'
    if environment == 'PROD':
        subject = 'Trade %s %s %s adapter' %(tradeNumber, main, environment)
        body = '%s' %(reason)
        mail_to = ['AbcapCMBonds@absa.africa', 'CIBAfricaFrontCore@absa.africa',
        'BushyHenry.Ngwako@absa.africa', 'Moreetsi.Kgaboesele@absa.africa', 'Zain.Beg@absa.africa', 'Anil.Parbhoo@absa.africa']
        EMAIL_FROM = 'ABCapITRTBFrontArena@absa.africa'
        email = EmailHelper(body, subject, mail_to, EMAIL_FROM)
        email.sender_type = EmailHelper.SENDER_TYPE_SMTP
        email.host = EmailHelper.get_acm_host()

        try:
            email.send()
        except Exception as e:
            acm.Log("!!! Exception: {0}\n".format(e))
            acm.Log(traceback.format_exc())
            exc_type, _exc_obj, exc_tb = sys.exc_info()
            filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            acm.Log("%s %s %s" % (exc_type, filename, exc_tb.tb_lineno))


def BESA_Rounding(amount):
    BESA_ROUNDING_SPEC = 5
    return round(amount, BESA_ROUNDING_SPEC)


def AMOUNT_Rounding(amount):
    AMOUNT_ROUNDING_SPEC = 2
    return round(amount, AMOUNT_ROUNDING_SPEC)


def amba_send(e, op):
    list = [["objtype", e.record_type]]
    BESA_Additionals = BESA(e, op)
    MIDBASE_Additionals = MIDBASE(e, op)
    MessageAdaptations = BESA_Additionals + MIDBASE_Additionals + list
    return MessageAdaptations

def notifyRTBmail(e):
    notify = 'has ZERO face value on'
    message = 'trade %s has ZERO face value.\
       If not booking error in FA\
       RTB to check log of amba_btb_production\
       to check that this zero face value trade is NOT stopping other valid trades from feeding to the adaptor' % e.trdnbr
       
    acm.Log(message)
    notify_Ops_RTB(e.trdnbr, notify, message)


def getFaceValue(e):
    FaceValue = e.nominal_amount()
    SendToBesa = e.insaddr.add_info('Exchange') == 'BESA' or (e.insaddr.und_insaddr and e.insaddr.und_insaddr.add_info('Exchange') == 'BESA')
    SuppressInternal = e.counterparty_ptynbr.add_info('UnexCor Code') == 'INTERNAL'
    agg_trade_type = ['Aggregate', 'Cash Posting']
    

    if FaceValue == 0.0 and SendToBesa and (e.type not in agg_trade_type) and (not SuppressInternal):
        ael.poll()
        FaceValue = e.nominal_amount()
        if FaceValue == 0.0 and SendToBesa and (e.type not in agg_trade_type) and (not SuppressInternal):
            notifyRTBmail(e)
             
                
    return FaceValue


def BESA(e, op):
    if e.record_type == "Trade":
        if op != "Delete":
            if e.insaddr.instype in ('BuySellback', 'Bond', 'Bill', 'FRN', 'IndexLinkedBond', 'Repo/Reverse', 'Zero') and (e.status not in ('Simulated', 'BO Confirmed', 'BO-BO Confirmed')) and (e.counterparty_ptynbr.hostid) and (e.insaddr.curr.insid in ('ZAR')) and (e.settle_category_chlnbr.entry not in ('Euroclear')):
                FaceValue = getFaceValue(e)
                Yield1 = e.price
                Yield2 = e.price
                SendToBesa = e.insaddr.add_info('Exchange') == 'BESA' or (e.insaddr.und_insaddr and e.insaddr.und_insaddr.add_info('Exchange') == 'BESA')
                #if this is an internal department or absa bank ltd, etc then to suppress flow to the exchange then make unexcor code INTERNAL
                SuppressInternal = e.counterparty_ptynbr.add_info('UnexCor Code') == 'INTERNAL'
                #the adapter is updated to cater for bigint type rather than int. However, we still want to define our own limit of 5bn
                SuppressLarge = abs(FaceValue) > 5000000000
                if e.insaddr.instype in ('BuySellback'):
                    i = e.insaddr
                    StartAccrued = i.und_insaddr.interest_accrued(None, i.start_day, i.curr.insid) * 100 / i.contr_size
                    EndAccrued = i.und_insaddr.interest_accrued(None, i.exp_day, i.curr.insid) * 100 / i.contr_size

                    if i.und_insaddr.instype == 'FRN':
                        AllIn_L1 = e.price
                        AllIn_L2 = i.ref_price
                        Clean_L1 = AllIn_L1 - StartAccrued
                        Clean_L2 = AllIn_L2 - EndAccrued
                    else:
                        Clean_L1 = i.und_insaddr.clean_from_yield(i.start_day, None, None, e.price)
                        Clean_L2 = i.und_insaddr.clean_from_yield(i.exp_day, None, None, i.ref_price)
                        AllIn_L1 = i.und_insaddr.dirty_from_yield(i.start_day, None, None, e.price)
                        AllIn_L2 = i.und_insaddr.dirty_from_yield(i.exp_day, None, None, i.ref_price)

                    EndCash = i.ref_value * e.quantity
                    BESA_TRADER = e.trader_usrnbr.add_info('BESA ID')
                    BROKERUNEXCOR = e.counterparty_ptynbr.hostid
                    JSE_INS = e.insaddr.und_insaddr.extern_id1
                    RepoRate = i.rate
                    InternalFlag = ''
                    if e.counterparty_ptynbr:
                        if e.counterparty_ptynbr.type == 'Intern Dept':
                            InternalFlag = 'Yes'
                        else:
                            InternalFlag = 'No'
                    AgencyTradPrincipal = ''
                    if e.prfnbr:
                        if e.prfnbr.add_info('AgencyTradPrincipal'):
                            AgencyTradPrincipal = e.prfnbr.add_info('AgencyTradPrincipal')
                    Yield2 = i.ref_price

                    if i.und_insaddr.instype in ('Bond', 'FRN', 'IndexLinkedBond'):
                        if i.und_insaddr.settle_category_chlnbr and i.und_insaddr.settle_category_chlnbr.entry == 'PriceTraded':
                            Yield1 = BESA_Rounding(AllIn_L1)
                            Yield2 = BESA_Rounding(AllIn_L2)
                    comp = ''
                    spread = 0.0
                    TapIssue = 'No'
                    PrimaryTrade = 'No'
                    BookOver = 'No'
                    GiveUp = 'No'
                    PrimeBroker = 'No'

                    BESA_Adaptations = [["Clean_L1", `BESA_Rounding(Clean_L1)`]] \
                                        + [["Clean_L2", `BESA_Rounding(Clean_L2)`]] \
                                        + [["AllIn_L1", `BESA_Rounding(AllIn_L1)`]] \
                                        + [["AllIn_L2", `BESA_Rounding(AllIn_L2)`]] \
                                        + [["ENDCASH", `EndCash`]] \
                                        + [["StartAccrued", `StartAccrued`]] \
                                        + [["EndAccrued", `EndAccrued`]] \
                                        + [["RepoRate", `RepoRate`]] \
                                        + [["BESA_Trader", BESA_TRADER]] \
                                        + [["BROKERUNEXCOR", BROKERUNEXCOR]]\
                                        + [["JSE_INS", JSE_INS]]\
                                        + [["AgencyTradPrincipal", `AgencyTradPrincipal`]]\
                                        + [["InternalFlag", InternalFlag]]\
                                        + [["FaceValue", `BESA_Rounding(FaceValue)`]]\
                                        + [["Yield_L1", `BESA_Rounding(Yield1)`]]\
                                        + [["Yield_L2", `BESA_Rounding(Yield2)`]]\
                                        + [["SendToBesa", `SendToBesa`]]\
                                        + [["SuppressInternal", `SuppressInternal`]]\
                                        + [["SuppressLarge", `SuppressLarge`]]\
                                        + [["Companion_Bond", `comp`]]\
                                        + [["Companion_Bond_Spread", `spread`]]\
                                        + [["Tap_issue", `TapIssue`]]\
                                        + [["Primary_Trade", `PrimaryTrade`]]\
                                        + [["Book_Over", `BookOver`]]\
                                        + [["Give_Up", `GiveUp`]]\
                                        + [["Prime_Broker", `PrimeBroker`]]

                    print 'trdnbr = ', e.trdnbr, 'contract_trdnbr = ', e.contract_trdnbr, 'instype = ', e.insaddr.instype, 'BESA Adaptations = ', BESA_Adaptations
                    return BESA_Adaptations

                elif e.insaddr.instype == 'Repo/Reverse' and e.insaddr.und_instype in ('IndexLinkedBond', 'Bond'):
                    ins = e.insaddr
                    leg = ins.legs()[0]
                    s_day = leg.start_day
                    e_day = ins.exp_day
                    price1 = ins.ref_price
                    EndCash = leg.projected_cf(s_day, e_day)*e.quantity
                    val = EndCash*100/(ins.ref_value*e.quantity)
                    try:
                        price2 = bond_iyl(ins.und_insaddr, val, e_day)
                    except Exception as e:
                        acm.Log("!!! Exception: {0}\n".format(e))
                        acm.Log(traceback.format_exc())
                        price2 = 0

                    RepoRate = leg.fixed_rate

                    Clean_L1 = ins.und_insaddr.clean_from_yield(s_day, None, None, price1)
                    Clean_L2 = ins.und_insaddr.clean_from_yield(e_day, None, None, price2)
                    AllIn_L1 = ins.und_insaddr.dirty_from_yield(s_day, None, None, price1)
                    AllIn_L2 = ins.und_insaddr.dirty_from_yield(e_day, None, None, price2)
                    StartAccrued = ins.und_insaddr.interest_accrued(None, s_day, ins.curr.insid) * 100 / ins.contr_size
                    EndAccrued = ins.und_insaddr.interest_accrued(None, e_day, ins.curr.insid) * 100 / ins.contr_size
                    BESA_TRADER = e.trader_usrnbr.add_info('BESA ID')
                    BROKERUNEXCOR = e.counterparty_ptynbr.hostid
                    JSE_INS = e.insaddr.und_insaddr.extern_id1
                    FaceValue = e.insaddr.ref_value * e.quantity
                    #the adapter is updated to cater for bigint type rather than int. However, we still want to define our own limit of 5bn
                    SuppressLarge = abs(FaceValue) > 5000000000
                    Yield1 = price1
                    Yield2 = price2
                    if ins.und_insaddr.instype in ('Bond', 'FRN', 'IndexLinkedBond'):
                        if ins.und_insaddr.settle_category_chlnbr and ins.und_insaddr.settle_category_chlnbr.entry == 'PriceTraded':
                            Yield1 = BESA_Rounding(AllIn_L1)
                            Yield2 = BESA_Rounding(AllIn_L2)
                    comp = ''
                    spread = 0.0
                    TapIssue = 'No'
                    PrimaryTrade = 'No'
                    BookOver = 'No'
                    GiveUp = 'No'
                    PrimeBroker = 'No'

                    BESA_Adaptations = [["Clean_L1", `BESA_Rounding(Clean_L1)`]] \
                                        + [["Clean_L2", `BESA_Rounding(Clean_L2)`]] \
                                        + [["AllIn_L1", `BESA_Rounding(AllIn_L1)`]] \
                                        + [["AllIn_L2", `BESA_Rounding(AllIn_L2)`]] \
                                        + [["ENDCASH", `EndCash`]] \
                                        + [["StartAccrued", `StartAccrued`]] \
                                        + [["EndAccrued", `EndAccrued`]] \
                                        + [["RepoRate", `RepoRate`]] \
                                        + [["BESA_Trader", BESA_TRADER]] \
                                        + [["BROKERUNEXCOR", BROKERUNEXCOR]]\
                                        + [["JSE_INS", JSE_INS]]\
                                        + [["PRICE_L2", `price2`]]\
                                        + [["FaceValue", `BESA_Rounding(FaceValue)`]]\
                                        + [["Yield_L1", `BESA_Rounding(Yield1)`]]\
                                        + [["Yield_L2", `BESA_Rounding(Yield2)`]]\
                                        + [["SendToBesa", `SendToBesa`]]\
                                        + [["SuppressInternal", `SuppressInternal`]]\
                                        + [["SuppressLarge", `SuppressLarge`]]\
                                        + [["Companion_Bond", `comp`]]\
                                        + [["Companion_Bond_Spread", `spread`]]\
                                        + [["Tap_issue", `TapIssue`]]\
                                        + [["Primary_Trade", `PrimaryTrade`]]\
                                        + [["Book_Over", `BookOver`]]\
                                        + [["Give_Up", `GiveUp`]]\
                                        + [["Prime_Broker", `PrimeBroker`]]
                    print 'trdnbr = ', e.trdnbr, 'contract_trdnbr = ', e.contract_trdnbr, 'instype = ', e.insaddr.instype, 'BESA Adaptations = ', BESA_Adaptations
                    return BESA_Adaptations

                elif e.insaddr.instype == 'Repo/Reverse' and e.insaddr.und_instype in ('FRN'):
                    ins = e.insaddr
                    leg = ins.legs()[0]
                    s_day = leg.start_day
                    e_day = ins.exp_day

                    EndCash = leg.projected_cf(s_day, e_day)*e.quantity
                    RepoRate = leg.fixed_rate
                    StartAccrued = ins.und_insaddr.interest_accrued(None, s_day, ins.curr.insid) * 100 / ins.contr_size
                    EndAccrued = ins.und_insaddr.interest_accrued(None, e_day, ins.curr.insid) * 100 / ins.contr_size
                    trade_ticket_quantity = ins.ref_value*e.quantity/ins.contr_size

                    AllIn_L1 = ins.ref_price
                    Clean_L1 = AllIn_L1 - StartAccrued
                    Yield1 = AllIn_L1
                    AllIn_L2 = abs(EndCash / trade_ticket_quantity / (ins.contr_size/100))
                    Clean_L2 = AllIn_L2 - EndAccrued
                    Yield2 = AllIn_L2
                    price2 = AllIn_L2

                    BESA_TRADER = e.trader_usrnbr.add_info('BESA ID')
                    BROKERUNEXCOR = e.counterparty_ptynbr.hostid
                    JSE_INS = e.insaddr.und_insaddr.extern_id1
                    FaceValue = e.insaddr.ref_value * e.quantity
                    # the adapter is updated to cater for bigint type rather than int. However, we still want to define our own limit of 5bn
                    SuppressLarge = abs(FaceValue) > 5000000000

                    comp = ''
                    spread = 0.0
                    TapIssue = 'No'
                    PrimaryTrade = 'No'
                    BookOver = 'No'
                    GiveUp = 'No'
                    PrimeBroker = 'No'

                    BESA_Adaptations = [["Clean_L1", `BESA_Rounding(Clean_L1)`]] \
                                        + [["Clean_L2", `BESA_Rounding(Clean_L2)`]] \
                                        + [["AllIn_L1", `BESA_Rounding(AllIn_L1)`]] \
                                        + [["AllIn_L2", `BESA_Rounding(AllIn_L2)`]] \
                                        + [["ENDCASH", `EndCash`]] \
                                        + [["StartAccrued", `StartAccrued`]] \
                                        + [["EndAccrued", `EndAccrued`]] \
                                        + [["RepoRate", `RepoRate`]] \
                                        + [["BESA_Trader", BESA_TRADER]] \
                                        + [["BROKERUNEXCOR", BROKERUNEXCOR]]\
                                        + [["JSE_INS", JSE_INS]]\
                                        + [["PRICE_L2", `price2`]]\
                                        + [["FaceValue", `AMOUNT_Rounding(FaceValue)`]]\
                                        + [["Yield_L1", `BESA_Rounding(Yield1)`]]\
                                        + [["Yield_L2", `BESA_Rounding(Yield2)`]]\
                                        + [["SendToBesa", `SendToBesa`]]\
                                        + [["SuppressInternal", `SuppressInternal`]]\
                                        + [["SuppressLarge", `SuppressLarge`]]\
                                        + [["Companion_Bond", `comp`]]\
                                        + [["Companion_Bond_Spread", `spread`]]\
                                        + [["Tap_issue", `TapIssue`]]\
                                        + [["Primary_Trade", `PrimaryTrade`]]\
                                        + [["Book_Over", `BookOver`]]\
                                        + [["Give_Up", `GiveUp`]]\
                                        + [["Prime_Broker", `PrimeBroker`]]
                    print 'trdnbr = ', e.trdnbr, 'contract_trdnbr = ', e.contract_trdnbr, 'instype = ', e.insaddr.instype, 'BESA Adaptations = ', BESA_Adaptations
                    return BESA_Adaptations

                elif e.insaddr.instype in ('IndexLinkedBond', 'Bond', 'Bill', 'FRN'):
                    try:
                        Accrued = abs(e.premium/e.nominal_amount()*100) - e.insaddr.clean_from_yield(e.value_day, None, None, e.price)
                    except Exception as e:
                        acm.Log("!!! Exception: {0}\n".format(e))
                        acm.Log(traceback.format_exc())
                        Accrued = 0

                    if e.insaddr.instype == 'FRN':
                        apvar = e.price
                    else:
                        apvar = ael.Instrument[e.insaddr.insaddr].dirty_from_yield(e.value_day, None, None, e.price)

                    if e.insaddr.instype in ('Bond', 'FRN', 'IndexLinkedBond'):
                        if e.insaddr.settle_category_chlnbr and e.insaddr.settle_category_chlnbr.entry == 'PriceTraded':
                            Yield1 = BESA_Rounding(apvar)

                    cpvar = ael.Instrument[e.insaddr.insaddr].clean_from_yield(e.value_day, None, None, e.price)
                    covar = ael.Instrument[e.insaddr.insaddr].dirty_from_yield(e.value_day, None, None, e.price)*abs(e.quantity)*10000
                    BESA_TRADER = e.trader_usrnbr.add_info('BESA ID')
                    BROKERUNEXCOR = e.counterparty_ptynbr.hostid
                    JSE_INS = e.insaddr.extern_id1
                    InternalFlag = ''
                    if e.counterparty_ptynbr:
                        if e.counterparty_ptynbr.type == 'Intern Dept':
                            InternalFlag = 'Yes'
                        else:
                            InternalFlag = 'No'
                    AgencyTradPrincipal = ''
                    if e.prfnbr:
                        if e.prfnbr.add_info('AgencyTradPrincipal'):
                            AgencyTradPrincipal = e.prfnbr.add_info('AgencyTradPrincipal')

                    if e.insaddr.add_info('Companion'):
                        comp = e.insaddr.add_info('Companion')
                    else:
                        comp = ''

                    if e.trdnbr != e.contract_trdnbr and (e.contract_trdnbr == e.connected_trdnbr.trdnbr): # this is a child split trade

                        if ael.Trade[e.contract_trdnbr].add_info('Companion_Spread'):
                            spread = BESA_Rounding(float(ael.Trade[e.contract_trdnbr].add_info('Companion_Spread')))
                        else:
                            spread = 0.00

                        if ael.Trade[e.contract_trdnbr].add_info('Book_Over') == 'Yes':
                            BookOver = 'Yes'
                        else:
                            BookOver = 'No'

                        if ael.Trade[e.contract_trdnbr].add_info('Tap_Issue') == 'Yes':
                            TapIssue = 'Yes'
                        else:
                            TapIssue = 'No'

                        if ael.Trade[e.contract_trdnbr].add_info('Primary_Trade') == 'Yes':
                            PrimaryTrade = 'Yes'
                        else:
                            PrimaryTrade = 'No'

                        if ael.Trade[e.contract_trdnbr].add_info('Give_Up') == 'Yes':
                            GiveUp = 'Yes'
                        else:
                            GiveUp = 'No'

                        if ael.Trade[e.contract_trdnbr].add_info('Prime_Broker') == 'Yes':
                            PrimeBroker = 'Yes'
                        else:
                            PrimeBroker = 'No'

                    else: # this is not a child split trade
                        if e.add_info('Companion_Spread'):
                            spread = BESA_Rounding(float(e.add_info('Companion_Spread')))
                        else:
                            spread = 0.0

                        if e.add_info('Book_Over') == 'Yes':
                            BookOver = 'Yes'
                        else:
                            BookOver = 'No'

                        if e.add_info('Tap_Issue') == 'Yes':
                            TapIssue = 'Yes'
                        else:
                            TapIssue = 'No'

                        if e.add_info('Primary_Trade') == 'Yes':
                            PrimaryTrade = 'Yes'
                        else:
                            PrimaryTrade = 'No'

                        if e.add_info('Give_Up') == 'Yes':
                            GiveUp = 'Yes'
                        else:
                            GiveUp = 'No'

                        if e.add_info('Prime_Broker') == 'Yes':
                            PrimeBroker = 'Yes'
                        else:
                            PrimeBroker = 'No'

                    BESA_Adaptations = [["AllInPrice", `BESA_Rounding(apvar)`]] \
                                        + [["CleanPrice", `BESA_Rounding(cpvar)`]] \
                                        + [["Consideration", `covar`]] \
                                        + [["Accrued", `Accrued`]] \
                                        + [["BESA_Trader", BESA_TRADER]]\
                                        + [["BROKERUNEXCOR", BROKERUNEXCOR]]\
                                        + [["JSE_INS", JSE_INS]]\
                                        + [["AgencyTradPrincipal", `AgencyTradPrincipal`]]\
                                        + [["InternalFlag", InternalFlag]]\
                                        + [["FaceValue", `BESA_Rounding(FaceValue)`]]\
                                        + [["Yield_L1", `BESA_Rounding(Yield1)`]]\
                                        + [["Yield_L2", `BESA_Rounding(Yield2)`]]\
                                        + [["SendToBesa", `SendToBesa`]]\
                                        + [["SuppressInternal", `SuppressInternal`]]\
                                        + [["SuppressLarge", `SuppressLarge`]]\
                                        + [["Companion_Bond", `comp`]]\
                                        + [["Companion_Bond_Spread", `spread`]]\
                                        + [["Tap_issue", `TapIssue`]]\
                                        + [["Primary_Trade", `PrimaryTrade`]]\
                                        + [["Book_Over", `BookOver`]]\
                                        + [["Give_Up", `GiveUp`]]\
                                        + [["Prime_Broker", `PrimeBroker`]]

                    print 'trdnbr = ', e.trdnbr, 'contract_trdnbr = ', e.contract_trdnbr, 'instype = ', e.insaddr.instype, 'BESA Adaptations = ', BESA_Adaptations
                    return BESA_Adaptations

                else:
                    try:
                        Accrued = abs(e.premium/e.nominal_amount()*100) - e.insaddr.clean_from_yield(e.value_day, None, None, e.price)
                    except Exception as e:
                        acm.Log("!!! Exception: {0}\n".format(e))
                        acm.Log(traceback.format_exc())
                        Accrued = 0

                    apvar = ael.Instrument[e.insaddr.insaddr].dirty_from_yield(e.value_day, None, None, e.price)
                    cpvar = ael.Instrument[e.insaddr.insaddr].clean_from_yield(e.value_day, None, None, e.price)
                    covar = ael.Instrument[e.insaddr.insaddr].dirty_from_yield(e.value_day, None, None, e.price)*abs(e.quantity)*10000
                    BESA_TRADER = e.trader_usrnbr.add_info('BESA ID')
                    BROKERUNEXCOR = e.counterparty_ptynbr.hostid
                    JSE_INS = e.insaddr.extern_id1
                    comp = ''
                    spread = 0.0
                    TapIssue = 'No'
                    PrimaryTrade = 'No'
                    BookOver = 'No'
                    GiveUp = 'No'
                    PrimeBroker = 'No'

                    BESA_Adaptations = [["AllInPrice", `BESA_Rounding(apvar)`]] \
                                        + [["CleanPrice", `BESA_Rounding(cpvar)`]] \
                                        + [["Consideration", `covar`]] \
                                        + [["Accrued", `Accrued`]] \
                                        + [["BESA_Trader", BESA_TRADER]]\
                                        + [["BROKERUNEXCOR", BROKERUNEXCOR]]\
                                        + [["JSE_INS", JSE_INS]]\
                                        + [["FaceValue", `BESA_Rounding(FaceValue)`]]\
                                        + [["Yield_L1", `BESA_Rounding(Yield1)`]]\
                                        + [["Yield_L2", `BESA_Rounding(Yield2)`]]\
                                        + [["SendToBesa", `SendToBesa`]]\
                                        + [["SuppressInternal", `SuppressInternal`]]\
                                        + [["SuppressLarge", `SuppressLarge`]]\
                                        + [["Companion_Bond", `comp`]]\
                                        + [["Companion_Bond_Spread", `spread`]]\
                                        + [["Tap_issue", `TapIssue`]]\
                                        + [["Primary_Trade", `PrimaryTrade`]]\
                                        + [["Book_Over", `BookOver`]]\
                                        + [["Give_Up", `GiveUp`]]\
                                        + [["Prime_Broker", `PrimeBroker`]]


                    return BESA_Adaptations
            else:
                BESA_Adaptations = [[]]
                return BESA_Adaptations

        else:
            BESA_Adaptations = [[]]
            return BESA_Adaptations

    else:
        BESA_Adaptations = [[]]
        return BESA_Adaptations


def MIDBASE(e, op):
    if e.record_type == "Trade":
        if op != "Delete":
            #MIDBASE_Adaptations = [["PV",`0.00`]] + [["Nominal",`e.nominal_amount()`]]
            MIDBASE_Adaptations = [["PV", `0.00`]] + [["Nominal", `0.00`]]
            return MIDBASE_Adaptations
        else:
            MIDBASE_Adaptations = [[]]
            return MIDBASE_Adaptations
    else:
        MIDBASE_Adaptations = [[]]
        return MIDBASE_Adaptations
        

def is_Collateral(trd):
    acquirer = get_value(trd, 'ACQUIRER_PTYNBR.PTYID')
    portfolio = get_value(trd, 'PRFNBR.PRFID')
    tradeCategory = get_value(trd, 'CATEGORY')
    
    if acquirer and acquirer == 'SECURITY LENDINGS DESK':
        if portfolio and get_Port_Struct_from_Port_list(ael.Portfolio[portfolio], 1, 'SBL_NONCASH_COLLATERAL'):
            if tradeCategory and tradeCategory in ('Collateral', 'COLLATERAL', 'TRADE_CATEGORY_COLLATERAL'):
                return True
    return False

def Modify_Send(m, s):
    msg = m
    msgtype = get_message_type(msg)
    mtype = string.rstrip(msgtype)

    if mtype in ('UPDATE_INSTRUMENT'):
        inst = msg.mbf_find_object('INSTRUMENT', 'MBFE_BEGINNING')
        try:
            Inst_Type = inst.mbf_find_object('INSTYPE', 'MBFE_BEGINNING')
        except Exception as e:
            acm.Log("!!! Exception: {0}\n".format(e))
            acm.Log(traceback.format_exc())
            return None

        if Inst_Type.mbf_get_value() in ('INS_REPO/REVERSE', 'INS_REPO'):
            try:
                Inst_Name = inst.mbf_find_object('INSID', 'MBFE_BEGINNING')
            except Exception as e:
                acm.Log("!!! Exception: {0}\n".format(e))
                acm.Log(traceback.format_exc())
                return None

            findName = Inst_Name.mbf_get_value()
            print 'Touch trades on %s' %findName
            for t in acm.FInstrument[findName].Trades():
                if t.Status() not in ('Simulated', 'Void', 'FO Sales', 'BO Confirmed', 'BO-BO Confirmed'):
                    t.Touch()
                    t.Commit()

        return None


    # Test if the message is a valid Trade message
    # If the message is not a trade, return None
    if mtype not in ('INSERT_TRADE', 'UPDATE_TRADE', 'DELETE_TRADE'):
        return None

    # Search for instrument type to determine if trade should be posted
    # to an external exchange.-E.g Bond Exchange

    trd = msg.mbf_find_object('TRADE', 'MBFE_BEGINNING')
    try:
        Inst_Type = trd.mbf_find_object('INSADDR.INSTYPE', 'MBFE_BEGINNING')
    except Exception as e:
        acm.Log("!!! Exception: {0}\n".format(e))
        acm.Log(traceback.format_exc())
        return None

    #print 'InsType=:',Inst_Type.mbf_get_value()
    if Inst_Type.mbf_get_value() in ('INS_BUY_SELLBACK', 'INS_BOND', 'INS_BILL', 'INS_FRN', 'INS_INDEX_LINKED_BOND',
                                     'INS_REPO/REVERSE', 'INS_REPO', 'INS_ZERO'):

        tradeNo = get_value(trd, 'TRDNBR')
        
        if is_Collateral(trd):
            acm.Log('Supress collateral trade %s.' % tradeNo)
            return None
        
        if not is_BESA_Trade(trd):
            acm.Log('Supress non BESA trade %s.  Instrument additional info for Exchange is not set to BESA.  '
                    'TCU action required.' % tradeNo)
            return None
        if is_Internal_Suppression(trd):
            acm.Log('Supress internal trade %s.  Counterparty additional info for UnexcorCode is set to INTERNAL, '
                    'thus suppressing trade from feeding.' % tradeNo)
            return None
        if is_Large_Suppression(trd):
            faceValue = get_value(trd, 'FACEVALUE')
            notify = 'is blocked on'
            message = 'Large trade %s with %s facevalue is surpressed.\
                       If correct in FA, then manual booking on exchange is required' %(tradeNo, faceValue)
            acm.Log(message)
            notify_Ops_RTB(tradeNo, notify, message)
            return None
        if is_mirror_trade(trd):
            acm.Log('Supress mirror trade %s.  Trade between two parties of type Internal is not sent to '
                    'exchange.' % tradeNo)
            return None
        if is_booked_by_cm_BuySellBackProcess(trd):
            acm.Log('Supress internal buysellbackprocess trade %s.  Trade booked via automated internal process is '
                    'not sent to exchange.' % tradeNo)
            return None

            
        msg.mbf_find_object('SOURCE', 'MBFE_BEGINNING')
        msg.mbf_replace_string('SOURCE', 'ADS_BTB_TRADE')
        return (msg, s)

    return None

def get_message_type(m):
    # Get Message Type.
    type = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    return type.mbf_get_value()


def get_value(msg, field):
    try:
        object = msg.mbf_find_object(field, 'MBFE_BEGINNING')
        if object:
            return object.mbf_get_value()
    except Exception as e:
        acm.Log("!!! Exception: {0}\n".format(e))
        acm.Log(traceback.format_exc())

    return None


def is_mirror_trade(tradeMsg):
    mirror_trade_number = get_value(tradeMsg, 'MIRROR_TRDNBR')
    return mirror_trade_number and mirror_trade_number >= 0


def is_booked_by_cm_BuySellBackProcess(tradeMsg):
    text1 = get_value(tradeMsg, 'TEXT1')
    return text1 and text1 == 'Booked cm_BuySellBackProcess'


def is_BESA_Trade(tradeMsg):
    SendToBesa = get_value(tradeMsg, 'SendToBesa')
    return SendToBesa and SendToBesa == 'True'


def is_Internal_Suppression(tradeMsg):
    SuppressInternal = get_value(tradeMsg, 'SuppressInternal')
    return SuppressInternal and SuppressInternal == 'True'


def is_Large_Suppression(tradeMsg):
    SuppressLarge = get_value(tradeMsg, 'SuppressLarge')
    return SuppressLarge and SuppressLarge == 'True'


acm.Log("MessageAdaptations Hook loaded...")
TESTMESSAGES = True
for item in ael.ServerData.select():
    if item.customer_name == 'Production':
        TESTMESSAGES = False
acm.Log('Run using test message = %s' % TESTMESSAGES)
