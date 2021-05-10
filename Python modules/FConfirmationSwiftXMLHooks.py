'''
This module is used to overwrite core tags defined in FConfirmationDefaultXMLHooks.

Any changes should be added to the "MT messages field rules" doc
in the confirmation and settlement section on confluence"

HISTORY
=================================================================================================================================
Date            Change no       Developer              Description
=================================================================================================================================
2017                            Willie vd Bank         Amended for 2017 upgrade
'''

import acm, ael, FSwiftUtils
from at_time import acm_date, to_datetime
from FSwiftMT305 import GetCounterAmount, GetPremiumPaymentAmount
from FSwiftMT306 import GetTypeOfAgreement, GetDateOfAgreement, GetVersionOfAgreement
from FSwiftMTConfirmation import GetPartyAOption, GetPartyAAccount, GetPartyABic, GetPartyBOption, GetPartyBAccount, GetPartyBBic

try:
    from FSwiftParameters import FAC
except ImportError:
    from FSwiftParametersTemplate import FAC

MT305_template = '''\
<SWIFT file = 'FConfirmationSwiftXMLHooks'>
    <CODE Field="22 M"><acmCode function = 'CODE'/></CODE>
    <CODE2 Field="23 O"><acmCode function = 'CODE2'/></CODE2>
    <COUNTER_AMOUNT Field="33B M"><acmCode function = 'GETCOUNTERPARTYAMOUNT' /></COUNTER_AMOUNT>
    <DATE_OF_AGREEMENT Field="77H O"><acmCode function ='GetDateOfAgreement'/></DATE_OF_AGREEMENT>
    <PREMIUM_PAYMENT_AMOUNT Field="34A M"><acmCode function = 'GETPREMIUMPAYMENTAMOUNT'/></PREMIUM_PAYMENT_AMOUNT>
    <SENDER_TO_RECEIVER_INFO Field="72 O"></SENDER_TO_RECEIVER_INFO>
    <SETTLEMENT_DATE Field="31E O"><acmCode function = 'SETTLEMENT_DATE'/></SETTLEMENT_DATE>
    <STRIKE_PRICE Field="22C M and 36 M"><acmCode function = 'STRIKE_PRICE'/></STRIKE_PRICE>
    <TYPE_OF_AGREEMENT Field="77H M"><acmCode function ='GetTypeOfAgreement'/></TYPE_OF_AGREEMENT>
    <VERSION_OF_AGREEMENT Field="77H M"><acmCode function ='GetVersionOfAgreement'/></VERSION_OF_AGREEMENT>
    <YOUR_REFERENCE Field="21 M"><acmCode function = 'YOUR_REFERENCE'/></YOUR_REFERENCE>
</SWIFT>
'''

MT320_template = '''\
<SWIFT file = 'FConfirmationSwiftXMLHooks'>
    <TERMS_CONDITIONS Field="77D O"></TERMS_CONDITIONS>
</SWIFT>
'''

commonBlock_template = '''\
<SWIFT file = 'FConfirmationSwiftXMLHooks'>
    <ACCOUNT_WITH_INSTITUTION_ACCOUNT Field="57A M"><acmCode function = 'GETPARTYBACCOUNT'/></ACCOUNT_WITH_INSTITUTION_ACCOUNT>
    <ACCOUNT_WITH_INSTITUTION_BIC Field="57A M"><acmCode function = 'GETPARTYBBIC'/></ACCOUNT_WITH_INSTITUTION_BIC>
    <ACCOUNT_WITH_INSTITUTION_OPTION Field="57A M"><acmCode function = 'GETPARTYBOPTION'/></ACCOUNT_WITH_INSTITUTION_OPTION>
    <PARTY_A_ACCOUNT Field="82A M"><acmCode function ='GETPARTYAACCOUNT'/></PARTY_A_ACCOUNT>
    <PARTY_A_BIC Field="82A M"><acmCode function ='GETPARTYABIC'/></PARTY_A_BIC>
    <PARTY_A_OPTION Field="82A M"><acmCode function ='GETPARTYAOPTION'/></PARTY_A_OPTION>
    <PARTY_B_ACCOUNT Field="87A M"><acmCode function ='GETPARTYBACCOUNT'/></PARTY_B_ACCOUNT>
    <PARTY_B_BIC Field="87A M"><acmCode function ='GETPARTYBBIC'/></PARTY_B_BIC>
    <PARTY_B_OPTION Field="87A M"><acmCode function ='GETPARTYBOPTION'/></PARTY_B_OPTION>
    <SENDER_CORRESPONDENT_ACCOUNT Field="53A O"><acmCode function = 'GETPARTYAACCOUNT'/></SENDER_CORRESPONDENT_ACCOUNT>
    <SENDER_CORRESPONDENT_BIC Field="53A O"><acmCode function = 'GETPARTYABIC'/></SENDER_CORRESPONDENT_BIC>
    <SENDER_CORRESPONDENT_OPTION Field="53A O"><acmCode function = 'GETPARTYAOPTION'/></SENDER_CORRESPONDENT_OPTION>
</SWIFT>
'''

def get_account(party, currency):
    for acc in party.Accounts():
        if acc.Currency() == currency:
            return acc.Account()

'''field 82A on MT305'''
def GETPARTYAOPTION(confirmation):
    option = GetPartyAOption(confirmation)
    if confirmation.MTMessages() == '305':
        if option == '':
            return 'A'
    return option

def GETPARTYAACCOUNT(confirmation):
    account = GetPartyAAccount()
    if confirmation.MTMessages() == '305':
        if account == '':
            return get_account(confirmation.Trade().Acquirer(), confirmation.Trade().Currency())
    return account

def GETPARTYABIC(confirmation):
    bic = GetPartyABic()
    if confirmation.MTMessages() == '305':
        if bic == '':
            return confirmation.AcquirerAddress()
    return bic

'''field 87A on MT305'''
def GETPARTYBACCOUNT(confirmation):
    account = GetPartyBAccount()
    if confirmation.MTMessages() == '305':
        if account == '':
            return get_account(confirmation.Trade().Counterparty(), confirmation.Trade().Currency())
    return account

def GETPARTYBOPTION(confirmation):
    option = GetPartyBOption(confirmation)
    if confirmation.MTMessages() == '305':
        if option == '':
            return 'A'
    return option

def GETPARTYBBIC(confirmation):
    bic = GetPartyBBic()
    if confirmation.MTMessages() == '305':
        if bic == '':
            return confirmation.CounterpartyAddress()
    return bic

'''mandatory Field 21 on MT305'''
def YOUR_REFERENCE(confirmation):
    yourReference = ''
    confType = confirmation.EventType()
    if confType == 'New Trade':
        yourReference = 'NEW'
    elif confType in ('New Trade Amendment', 'New Trade Cancellation'):
        confRef = confirmation.ConfirmationReference()
        if confRef and FAC and FAC.strip():
            yourReference = "%s-%s" % (FAC, str(confRef.Oid()))
    return yourReference


'''field 31E on MT305'''
def SETTLEMENT_DATE(confirmation):
    instrument = confirmation.Trade().Instrument()
    settlment_date = ael.date(instrument.DeliveryDate())

    return acm_date(settlment_date)

'''field 36 on MT305'''
def STRIKE_PRICE(confirmation):
    instrument = confirmation.Trade().Instrument()

    return instrument.StrikePrice()

'''mandatory field 22 on MT305'''
def CODE(confirmation):
    typeOfCode = {'New Trade':'NEW', 'New Trade Amendment':'AMEND', \
                   'New Trade Cancellation':'CANCEL', 'New Trade Close':'CLOSEOUT'}
    confType = confirmation.EventType()
    return typeOfCode.get(confType, '')

'''this together with code1, code3 and underlying currency forms the optional field 23'''
def CODE2(confirmation):
    if confirmation.Trade().Instrument().IsCallOption():
        return 'CALL'
    else:
        return 'PUT'

'''this together with counter_currency forms the mandatory field 33B'''
def GETCOUNTERPARTYAMOUNT(confirmation):
    amount = GetCounterAmount(confirmation)
    return FSwiftUtils.ApplyCurrencyPrecision(confirmation.Trade().Currency().Name(), amount)

'''This together with PREMIUM_PAYMENT_OPTION,PREMIUM_PAYMENT_DATE
   and PREMIUM_PAYMENT_CURRENCY forms the mandatory field 34A in SWIFT'''    
def GETPREMIUMPAYMENTAMOUNT(confirmation):
    amount = GetPremiumPaymentAmount(confirmation)
    return FSwiftUtils.ApplyCurrencyPrecision(confirmation.Trade().Currency().Name(), amount)
