"""-----------------------------------------------------------------------------
PURPOSE                 :   This module will process the incoming MT298-128 message which contains
                            coupon information from Strate and create stand-alone settlements
--------------------------------------------------------------------------------
HISTORY
================================================================================
Date            Change no       Developer            Description
--------------------------------------------------------------------------------
2016-08-19      CHNG0003744247  Willie vd Bank       Initial Implementation
2016-09-06      CHNG0003914707  Willie vd Bank       Amended to first look for the generic account
2016-11-22      CHNG0004119204  Willie vd Bank       Changed field 21 to reference field 21 in the 298
                                                     in stead of field 20 in the 298
2017                            Willie vd Bank       Set values for CounterpartyAccountNetworkName and
                                                     AcquirerAccountNetworkName which is required for
                                                     swift message type to work according to FA 2017 upgrade
09-11-2020      FAOPS-931       Tawanda Mukhalela    Added Support for MT298 settlements for ABSA to ABSA Payments
"""

import acm
from acm import Time
from string import split, replace
from gen_swift_functions import get_multiline_text_from_tag, get_text_from_tag
from PS_Functions import modify_asql_query
from demat_functions import GetFirstTrade
from CustomSWIFTFunctions import ENTITLED_COUPON_PAYMENT, TOTAL_ELIGIBLE_NOMINAL
from SAGEN_Set_Additional_Info import set_AdditionalInfoValue_ACM
from at_logging import getLogger
from demat_config import CFquery


LOGGER = getLogger(__name__)

def getCF(CEM, date):
    #Searches through matching cash flows and returns the one whith the correct CE reference
    
    global CFquery
    query = modify_asql_query(acm.FStoredASQLQuery[CFquery].Query(), "AdditionalInfo.Demat_CE_Reference", False, CEM)
    query = modify_asql_query(query, "PayDate", False, date)
    if len(query.Select()) == 1:
        return query.Select()[0]
    return None


def setToAuthorised(cash_flow, firstTrade):
    #Checks all existing settlements on the first trade and sets to Authorised if the settlements total matches the total coupon
    setAuth = False
    #This initial check is done to prevent the duplicate release of payments in the case where duplicate 298s are received
    settlmnts = [s for s in firstTrade.Settlements() if s.CashFlow() == cash_flow and s.Status() != 'Void']
    if len(settlmnts):
        if cash_flow.CashFlowType() != 'Fixed Amount':
            proj = abs(float(ENTITLED_COUPON_PAYMENT(settlmnts[0])[3:].replace(',', '.'))) #The format returned is ZAR123,45
        else:
            proj = abs(float(TOTAL_ELIGIBLE_NOMINAL(settlmnts[0]).replace(',', '.'))) #The format returned is 123,45
        settleAmount = 0
        for s in settlmnts:
            if ':910' in s.AdditionalInfo().Call_Confirmation():
                continue
            settleAmount += s.Amount()
        if (abs(proj) - 2) <= abs(settleAmount) <= (abs(proj) + 2):
            setAuth = True
    if setAuth:
        settlmnts = [s for s in firstTrade.Settlements() if s.CashFlow() == cash_flow and s.Status() == 'Hold']
        for s in settlmnts:
            if ':910' in s.AdditionalInfo().Call_Confirmation():
                continue
            s.Status('Authorised')
            s.AddDiaryNote('Settlements Authorised for coupon ' + str(cash_flow.Oid()))
            s.Commit()
        return 'Settlements authorised for trade ' + str(firstTrade.Oid())
    return 'Settlement created in status Hold'


def getCurraccounts(accounts):
    curraccounts = []
    curraccounts = [a.Oid() for a in accounts if a.Account() == 'GENERIC']
    if not curraccounts:
        curraccounts = [a.Oid() for a in accounts if a.Currency() and a.Currency().Name() == 'ZAR']
    return curraccounts


def settmnt_mgmt_incoming(mtmessage, msg_type):

    print('Settlement processing started...')
    date = acm.Time.DateNow()
    event_reference = get_text_from_tag(':21:', mtmessage)
    CEM = event_reference.replace('CEM', '').strip()
    cash_sflow = getCF(CEM, date)
    if not cash_sflow:
        LOGGER.error('No corresponding cash flow found, no settlement will be created!')
        return
    first_trade = GetFirstTrade(cash_sflow.Leg().Instrument().Trades()[0])
    stand_alone_settlement = _create_stand_alone_payment_for_event(
        date, first_trade, cash_sflow, mtmessage, CEM
    )
    LOGGER.info('MT202 Stand Alone Settlement {} created for trade '.format(stand_alone_settlement.Oid()))
    LOGGER.info(setToAuthorised(cash_sflow, first_trade))

    #   Create MT298-128 Settlement if 57A is ABSAZAJJ or J0 for Dev
    field_57 = split(get_multiline_text_from_tag(':57A://', mtmessage))
    institution_bic = field_57[1] if len(field_57) > 1 else ''
    if institution_bic in ['ABSAZAJJ', 'ABSAZAJ0']:
        event_reference = event_reference + ':910'
        mt298_stand_alone_settlement = _create_stand_alone_payment_for_event(
            date, first_trade, cash_sflow, mtmessage, event_reference
        )
        LOGGER.info('Created MT298 Settlement {} in hold status.'.format(mt298_stand_alone_settlement.Oid()))

    LOGGER.info('Settlement processing done.')


def _create_stand_alone_payment_for_event(date, first_trade, cash_sflow, mtmessage, event_reference):
    """
    Creates Stand Alone Payment
    """
    counterparty = first_trade.Counterparty()
    acquirer = acm.FParty[2246]  # MONEY MARKET DESK
    field_57 = split(get_multiline_text_from_tag(':57A://', mtmessage))
    field_58 = split(get_multiline_text_from_tag(':58D:/', mtmessage))
    institution_account = field_57[0]
    beneficiary_account = field_58[0]
    institution_bic = field_57[1] if len(field_57) > 1 else ''
    beneficiary_name = field_58[1] if len(field_58) > 1 else ''
    amount = float(replace(get_text_from_tag(':32B:ZAR', mtmessage), ',', '.'))
    try:
        new_settle = acm.FSettlement()
        new_settle.Amount(amount)
        new_settle.Currency(acm.FCurrency['ZAR'])
        new_settle.ValueDay(date)
        new_settle.Type('Stand Alone Payment')

        new_settle.Counterparty(counterparty)
        accounts = counterparty.Accounts()
        curraccounts = getCurraccounts(accounts)
        new_settle.CounterpartyAccName(acm.FAccount[curraccounts[0]].Name())
        new_settle.CounterpartyAccount(acm.FAccount[curraccounts[0]].Account())
        new_settle.CounterpartyAccountNetworkName('SWIFT')

        new_settle.Acquirer(acquirer)
        accounts = acquirer.Accounts()
        curraccounts = getCurraccounts(accounts)
        new_settle.AcquirerAccName(acm.FAccount[curraccounts[0]].Name())
        new_settle.AcquirerAccount(acm.FAccount[curraccounts[0]].Account())
        new_settle.AcquirerAccountNetworkName('SWIFT')

        new_settle.Status('Hold')
        new_settle.Trade(first_trade)
        new_settle.CashFlow(cash_sflow)
        new_settle.Commit()

        set_AdditionalInfoValue_ACM(new_settle, 'Call_Confirmation', event_reference)
        set_AdditionalInfoValue_ACM(new_settle, 'ACC_WTH_INSTITUTION', institution_bic + ' & ' + institution_account)
        set_AdditionalInfoValue_ACM(new_settle, 'BENEF_INSTITUTION', beneficiary_name + ' & ' + beneficiary_account)

        return new_settle
    except Exception as error:
        LOGGER.error('Failed to create Stand Alone settlement')
        LOGGER.exception(error)


_message = '''{1:F01ABSAZAJ0AMG19130017057}{2:O2980808160511ZYANZAJ0GXXX56015460371605110808N}{3:{108:02734083MM10F002}}{4:
:20:2016CEM504375555
:12:128
:77E:MPDEM
:21:2016CEM504375
:32B:ZAR52997,26
:52D:/66000135
ZA632005
:57A://ZA001254
STRBZAJ0
:58D:/9876541216
ZA001254
:72:/REC/MPDEM
-}{5:{MAC:00000000}{CHK:D6EE03944770}{TNG:}}'''

#settmnt_mgmt_incoming(mtmessage, '')
