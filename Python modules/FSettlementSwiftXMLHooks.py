"""-----------------------------------------------------------------------------
HISTORY
================================================================================
Date            Change no       Developer           Description
--------------------------------------------------------------------------------
2016-08-19      CHNG0003744247  Willie vd Bank      Demat Implementation
2016-08-23      CHNG0003898744  Willie vd Bank      Amended the way netted
                                                    settlements are identified
2016-09-06      CHNG0003914707  Willie vd Bank      Updated function get_our_curr_NOSTRO_SWIFT
                                                    so as to return the correct nostro account
2016-09-13      CHNG0003938092  Gabriel Marko       BENEFICIARY_CUSTOMER_NAME, ORDERING_CUSTOMER_NAME Tag:
                                                    Use Counterparty.Name if fullname is not avaible
2016-10-11      CHNG0003970520  Gabriel Marko       Fix Netted Settlements for Money Market and Founding Desk:
                                                    Use trade from child settlement for TRADING_DESK tag
2016-12-06      CHNG0004158509  Gabriel Marko       Prevent settlements to be debited of the Derivatives cash book
                                                    instead of the Money Market cash book for COLLATERAL DESK
2017-02-07      CHNG0004274270  Willie vd Bank      Fixed an issue where ACCOUNT_WITH_INSTITUTION NAME and/or
                                                    ADDRESS can be longer than 35 characters and then fail
                                                    Adaptiv core validation
2017-08-26                      Willie vd Bank      Upgrade 2017: Added SENDERS_CORRESPONDENT_ACCOUNT on MT103
2017-09-27      CHNG0004982874  Willie vd Bank      Added SENDERS_CORRESPONDENT_ACCOUNT on MT202
2017-10-12      CHNG0005034523  Willie vd Bank      Added CHECK_CP_REF, Rec code functionality
                                                    Added DIS functionality
                                                    Modified RECEIVER_BIC to read swift code from account on cpty
                                                    in stead of counterparty correspondent Bic field.
2017-11-07      CHNG0005090917  Ntuthuko Matthews   Handle scenarios where relation type doesn't contain Net
2017-12-11      CHNG0005220511  Willie vd Bank      Removed try and except for is_dis import
2017-12-20      CHNG0005244993  Willie vd Bank      Added / to SENDERS_CORRESPONDENT_LOCATION for DIS
2018-01-18      CHG1000050648   Willie vd Bank      Your_Reference should always return NONREF
2018-05-11      CHG1000406751   Willie vd Bank      Added overrides for MT540 series
2018-09-15                      Sadanand Upase      If trade category is set to Euroclear then field 22F should be TRAD
2019-08-01      FAOPS-587       Tawanda Mukhalela   Added End Cash Consideration for End Security Settlements
2019-08-28      FAOPS-592       Tawanda Mukhalela   Updated SENDER_TO_RECEIVER_INFO to accommodate SRG Changes.
2019-10-01      FAOPS-643       Tawanda Mukhalela   Updated SENDER_TO_RECEIVER_INFO to accommodate CFC Payments.
2019-10-30      FAOPS-664       Jaysen Naicker      Change field 70C payment type from Premium to Broker Fee.
2019-11-19      FAOPS-612       Tawanda Mukhalela   Added REC Code adjustment to reflect accordingly on nettes
                                                    settlements. Code Refactor.
2019-03-22      FAOPS-659       Joash Moodley       Generate MT202's for SSA MT54x securities Funding.
2020-04-21      FAOPS-700       Cuen Edwards        MT540 changes for internal and external transfers.
2020-05-28      FAOPS-683       Joash Moodley       EuroClear Custody Funding (MT210 & MT222(custom 202)).
2020-05-28      FAOPS-740       Joash Moodley       EuroClear Custody Funding (MT200).
2020-09-14      FAOPS-864       Jaysen Naicker      Enable End Cash for Euroclear Repo/Reverse and
                                                    incl BSB ins type in Funding
09-11-2020      FAOPS-931       Tawanda Mukhalela   Added Support for MT298 settlements
2020-10-02      FAOPS-881       Tawanda MUkhalela   Added Support for field 21 to get capital Event from Payment
                                                    when settlement has no cashflows, this only applies to DIS Bonds
2020-11-10      FAOPS-836       Tawanda Mukhalela   Reverted Trading Desk to MMA for SBL Collateral
2021-01-06      FAOPS-1024      Tawanda Mukhalela   Changed date formating on Function DATE
2020-11-24      FAOPS-861       Ntokozo Skosana     Update  fields 57A on MT210 and MT202
2020-02-25      FAOPS-997       Ntokozo Skosana     Added functionality to support Euroclear payments.
"""

import acm, ael, time, re, FLogger, os, tempfile
import datetime
from SAGEN_IT_Functions import get_lowest_settlement
from FSettlementHooks import (
    get_is_internal,
    is_demat,
    is_demat_initial_settmnt,
    is_dis
)
from SettlementGLAccounts import GL_Acc
from FSwiftMTBase import GetPartyBic
import FOperationsUtils as UtilsMod
from FSwiftMTSettlement import GetReceiverBic
from SAGEN_IT_Functions import get_trd_from_possible_nettsettle
from gen_absa_xml_config_settings import AbsaXmlConfigSettings
from FSwiftMT103 import (
    GetInterbankSettledAmount,
    GetOrderingCustomerOption,
    GetOrderingCustomerBic,
    GetBankOperationCode
)
from FSwiftMT202 import GetSendersCorrespondentAccount
from FSwiftMTSecuritiesSettlement import (
    GetQualifier,
    GetIndicator,
    GetMandatoryIndicator,
    GetPartyDetails,
    GetPartyQualifier,
    GetPartyIdentifierCode,
    GetPartyCountryCode,
    GetPartyFullName,
    GetPartyAddress,
    GetDataSourceScheme,
    GetPartyProprietaryCode,
    GetPartySafekeepingOption,
    GetPartySafekeepingAccount,
    GetPartySafekeepingQualifier,
    GetPartyOption
)
from FSwiftMTSecuritiesSettlement import (
    GetAmountQualifier,
    GetCurrencyCode
)
from FSettlementEnums import SettlementType
from FSettlementHooks import is_valid_curr_euroclear_payment, get_payment_currency_name
from decimal import Decimal
absa_swift_param = AbsaXmlConfigSettings().GetUniqueNode('AbcapSwiftParameters')
strate_swift_param = AbsaXmlConfigSettings().GetUniqueNode('StrateSwiftParameters')
GLOBAL_SEPARATOR = "/"
OUR_BANK = "ABSA BANK LTD"
calc_space_tradesheet = acm.Calculations().CreateCalculationSpace('Standard', 'FTradeSheet')
VALID_PAYMENT_CURRENCIES_FOR_222 = ['USD', 'ZAR', 'JPY', 'GBP']
TESTMESSAGES = True
for item in ael.ServerData.select():
    CUSTOMERNAME = item.customer_name
    if CUSTOMERNAME == 'Production':
        TESTMESSAGES = False
    else:
        print 'Run using test message BICS =', TESTMESSAGES

getLogDir = acm.GetFunction('getLogDir', 0)
if getLogDir:
    LogPath = getLogDir()
else:
    LogPath = tempfile.gettempdir()

logFileName = os.path.join(LogPath, "%s%s.log" % (acm.User().Name(), time.strftime('%Y%m%d')))

logger = FLogger.FLogger(logToFileAtSpecifiedPath=logFileName)
logger.LOG('Main Customer Name is %s' % CUSTOMERNAME)
logger.LOG('Main Test environment parameter value is %s,' % TESTMESSAGES)

MT103_template = '''\
<SWIFT file = 'FSettlementSwiftXMLHooks'>
    <ACCOUNT_WITH_INSTITUTION_ACCOUNT Field="57 O"><acmCode function = 'ACCOUNT_WITH_INSTITUTION_ACCOUNT'/></ACCOUNT_WITH_INSTITUTION_ACCOUNT>
    <ACCOUNT_WITH_INSTITUTION_ADDRESS Field="57A M"></ACCOUNT_WITH_INSTITUTION_ADDRESS>
    <ACCOUNT_WITH_INSTITUTION_BIC Field="57 O"><acmCode function = 'ACCOUNT_WITH_INSTITUTION_BIC'/></ACCOUNT_WITH_INSTITUTION_BIC>
    <ACCOUNT_WITH_INSTITUTION_NAME Field="57A O"></ACCOUNT_WITH_INSTITUTION_NAME>
    <BENEFICIARY_CUSTOMER_ACCOUNT><acmCode function = 'BENEFICIARY_CUSTOMER_ACCOUNT'/></BENEFICIARY_CUSTOMER_ACCOUNT>
    <BENEFICIARY_CUSTOMER_ADDRESS></BENEFICIARY_CUSTOMER_ADDRESS>
    <BENEFICIARY_CUSTOMER_NAME><acmCode function = 'BENEFICIARY_CUSTOMER_NAME'/></BENEFICIARY_CUSTOMER_NAME>
    <BENEFICIARY_CUSTOMER_OPTION><acmCode function = 'BENEFICIARY_CUSTOMER_OPTION'/></BENEFICIARY_CUSTOMER_OPTION>
    <DETAILS_OF_CHARGES><acmCode function = 'DETAILS_OF_CHARGES'/></DETAILS_OF_CHARGES>
    <ORDERING_CUSTOMER_ACCOUNT><acmCode function = 'ORDERING_CUSTOMER_ACCOUNT'/></ORDERING_CUSTOMER_ACCOUNT>
    <ORDERING_CUSTOMER_ADDRESS></ORDERING_CUSTOMER_ADDRESS>
    <ORDERING_CUSTOMER_NAME><acmCode function = 'ORDERING_CUSTOMER_NAME'/></ORDERING_CUSTOMER_NAME>
    <ORDERING_INSTITUTION_ACCOUNT Field="52 O"></ORDERING_INSTITUTION_ACCOUNT>
    <ORDERING_INSTITUTION_BIC Field="52 O"><acmCode function = 'ORDERING_INSTITUTION_BIC'/></ORDERING_INSTITUTION_BIC>
    <ORDERING_INSTITUTION_OPTION Field="52 O"><acmCode function = 'ORDERING_INSTITUTION_OPTION'/></ORDERING_INSTITUTION_OPTION>
    <REMITTANCE_INFO><acmCode function = 'REMITTANCE_INFO'/></REMITTANCE_INFO>
    <SENDERS_CORRESPONDENT_ACCOUNT Field="53A O"></SENDERS_CORRESPONDENT_ACCOUNT>
    <SENDERS_CORRESPONDENT_BIC Field="53 O"><acmCode function = 'SENDERS_CORRESPONDENT_BIC'/></SENDERS_CORRESPONDENT_BIC>
    <SENDERS_CORRESPONDENT_LOCATION Field="53 O">/MMARK</SENDERS_CORRESPONDENT_LOCATION>
    <SENDERS_CORRESPONDENT_OPTION Field="53 O"><acmCode function = 'SENDERS_CORRESPONDENT_OPTION'/></SENDERS_CORRESPONDENT_OPTION>
    <SENDER_TO_RECEIVER_INFO><acmCode function = 'SENDER_TO_RECEIVER_INFO'/></SENDER_TO_RECEIVER_INFO>
</SWIFT>
'''

MT202_template = '''\
<SWIFT file = 'FSettlementSwiftXMLHooks'>
    <ACCOUNT_WITH_INSTITUTION_ACCOUNT Field="57 O"><acmCode function = 'ACCOUNT_WITH_INSTITUTION_ACCOUNT'/></ACCOUNT_WITH_INSTITUTION_ACCOUNT>
    <ACCOUNT_WITH_INSTITUTION_ADDRESS Field="57A M"></ACCOUNT_WITH_INSTITUTION_ADDRESS>
    <ACCOUNT_WITH_INSTITUTION_BIC Field="57 O"><acmCode function = 'ACCOUNT_WITH_INSTITUTION_BIC'/></ACCOUNT_WITH_INSTITUTION_BIC>
    <ACCOUNT_WITH_INSTITUTION_NAME Field="57A O"></ACCOUNT_WITH_INSTITUTION_NAME>
    <ACCOUNT_WITH_INSTITUTION_OPTION Field="57 O"><acmCode function = 'ACCOUNT_WITH_INSTITUTION_OPTION'/></ACCOUNT_WITH_INSTITUTION_OPTION>
    <BENEFICIARY_INSTITUTION_ACCOUNT Field="58 M"><acmCode function = 'BENEFICIARY_INSTITUTION_ACCOUNT'/></BENEFICIARY_INSTITUTION_ACCOUNT>
    <BENEFICIARY_INSTITUTION_ADDRESS Field="58A M"></BENEFICIARY_INSTITUTION_ADDRESS>
    <BENEFICIARY_INSTITUTION_BIC Field="58 M"><acmCode function = 'BENEFICIARY_INSTITUTION_BIC'/></BENEFICIARY_INSTITUTION_BIC>
    <BENEFICIARY_INSTITUTION_NAME Field="58 M"><acmCode function = 'BENEFICIARY_INSTITUTION_NAME'/></BENEFICIARY_INSTITUTION_NAME>
    <BENEFICIARY_INSTITUTION_OPTION Field="58 M"><acmCode function = 'BENEFICIARY_INSTITUTION_OPTION'/></BENEFICIARY_INSTITUTION_OPTION>
    <INTERMEDIARY_ACCOUNT><acmCode function = 'INTERMEDIARY_ACCOUNT'/></INTERMEDIARY_ACCOUNT>
    <ORDERING_INSTITUTION_ACCOUNT></ORDERING_INSTITUTION_ACCOUNT>
    <ORDERING_INSTITUTION_BIC><acmCode function = 'ORDERING_INSTITUTION_BIC'/></ORDERING_INSTITUTION_BIC>
    <ORDERING_INSTITUTION_OPTION><acmCode function = 'ORDERING_INSTITUTION_OPTION'/></ORDERING_INSTITUTION_OPTION>
    <SENDERS_CORRESPONDENT_ACCOUNT Field="53A O"></SENDERS_CORRESPONDENT_ACCOUNT>
    <SENDERS_CORRESPONDENT_BIC Field="53 O"><acmCode function = 'SENDERS_CORRESPONDENT_BIC'/></SENDERS_CORRESPONDENT_BIC>
    <SENDERS_CORRESPONDENT_LOCATION Field="53 O"><acmCode function = 'SENDERS_CORRESPONDENT_LOCATION'/></SENDERS_CORRESPONDENT_LOCATION>
    <SENDERS_CORRESPONDENT_OPTION Field="53 O"><acmCode function = 'SENDERS_CORRESPONDENT_OPTION'/></SENDERS_CORRESPONDENT_OPTION>
    <SENDER_TO_RECEIVER_INFO><acmCode function = 'SENDER_TO_RECEIVER_INFO'/></SENDER_TO_RECEIVER_INFO>
    <YOUR_REFERENCE><acmCode function = 'YOUR_REFERENCE'/></YOUR_REFERENCE>
</SWIFT>
'''

MT202_custom_template = '''\
<MESSAGE>
<SWIFT file = 'FSettlementSwiftXMLHooks'> 
    <BOND_FUNDING Field="21"><acmCode function = 'GET_FUNDING_TYPE'/></BOND_FUNDING>
    <AMOUNT Field="32A"><acmCode function = 'DATE'/><acmCode function = 'AMOUNT'/></AMOUNT>
    <INTERMEDIARY_ACCOUNT Field="56A M"><acmCode function = 'GET_CASH_ACCOUNT_NUMBER'/></INTERMEDIARY_ACCOUNT>
    <SENDERS_CORRESPONDENT_ACCOUNT Field="53A"><acmCode function = 'GET_ACQUIRER_ACC_NUM'/></SENDERS_CORRESPONDENT_ACCOUNT>
    <RECEIVER_BIC><acmCode function = 'GET_RECEIVER_BIC'/></RECEIVER_BIC>
    <EUROCLEAR_BIC><acmCode function = 'GET_NetworkAlias'/></EUROCLEAR_BIC>
    <ACCOUNT_WITH_INSTITUTION_ADDRESS Field="57A M"><acmCode function = 'GET_FIELD_57A_FOR_CUSTOM_202'/></ACCOUNT_WITH_INSTITUTION_ADDRESS>
    <BENEFICIARY_INSTITUTION_ADDRESS Field="58A M">/<acmCode function = 'GET_SECURITY_ACCOUNT_NUMBER'/></BENEFICIARY_INSTITUTION_ADDRESS>
    <SENDER_BIC><acmCode function = 'ALIAS'/></SENDER_BIC>
    <CURRENCY><acmCode function = 'GET_CURRENCY'/></CURRENCY>
    <SWIFT_MESSAGE_TYPE>222</SWIFT_MESSAGE_TYPE>
    <SEQREF Field="20 M">FAS</SEQREF> 
</SWIFT>
<SETTLEMENT>
    <SEQNBR Field="20 M" ><acmCode method ='Oid' ignoreUpdate ='True'/></SEQNBR>
  </SETTLEMENT>
</MESSAGE>
'''

MT210_custom_template = '''\
<MESSAGE>
<SWIFT file = 'FSettlementSwiftXMLHooks'>
    <BOND_FUNDING Field="21"><acmCode function = 'GET_FUNDING_TYPE'/></BOND_FUNDING>
    <CORES_BANK_ACC Field="25">/<acmCode function = 'GET_SECURITY_ACCOUNT_NUMBER'/></CORES_BANK_ACC>
    <VALUE_DATE><acmCode function = 'GET_VALUE_DATE'/></VALUE_DATE>
    <AMOUNT Field="32B"><acmCode function = 'AMOUNT'/></AMOUNT>
    <ALIAS Field="52A"><acmCode function = 'ALIAS'/></ALIAS>
    <INTERMEDIARY_ACCOUNT Field="56A M"><acmCode function = 'GET_FIELD_56A_FOR_CUSTOM_210'/></INTERMEDIARY_ACCOUNT>
    <RECEIVER_BIC><acmCode function = 'GET_NetworkAlias'/></RECEIVER_BIC>
    <SENDER_BIC><acmCode function = 'ALIAS'/></SENDER_BIC>
    <SWIFT_MESSAGE_TYPE>210</SWIFT_MESSAGE_TYPE>
    <SEQREF Field="20 M">FAS</SEQREF> 
</SWIFT>
<SETTLEMENT>
    <SEQNBR Field="20 M" ><acmCode method ='Oid' ignoreUpdate ='True'/></SEQNBR>
  </SETTLEMENT>
</MESSAGE>
'''

MT200_custom_template = '''\
<MESSAGE>
<SWIFT file = 'FSettlementSwiftXMLHooks'>
    <BOND_FUNDING Field="21"><acmCode function = 'GET_FUNDING_TYPE'/></BOND_FUNDING>
    <AMOUNT Field="32A"><acmCode function = 'DATE'/><acmCode function = 'AMOUNT'/></AMOUNT>
    <CORES_BANK_ACC Field="53B">/<acmCode function = 'GET_SECURITY_ACCOUNT_NUMBER'/></CORES_BANK_ACC>
    <ACCOUNT_WITH_INSTITUTION_ADDRESS Field="57A M"><acmCode function = 'CP_CODE_EUROCLER'/></ACCOUNT_WITH_INSTITUTION_ADDRESS>
    <RECEIVER_BIC><acmCode function = 'GET_NetworkAlias'/></RECEIVER_BIC>
    <SENDER_BIC><acmCode function = 'ALIAS'/></SENDER_BIC>
    <SENDER_TO_RECEIVER_INFO>/ACC/<acmCode function = 'GET_SENDER_TO_RECEIVER_INFO'/></SENDER_TO_RECEIVER_INFO>
    <EUROCLEAR_BIC><acmCode function = 'CP_CODE_DR'/></EUROCLEAR_BIC>
    <SWIFT_MESSAGE_TYPE>200</SWIFT_MESSAGE_TYPE>
    <SEQREF Field="20 M">FAS</SEQREF> 
</SWIFT>
<SETTLEMENT>
    <SEQNBR Field="20 M" ><acmCode method ='Oid' ignoreUpdate ='True'/></SEQNBR>
  </SETTLEMENT>
</MESSAGE>
'''

MT298_custom_template = '''\
<MESSAGE>
    <SWIFT file = 'FSettlementSwiftXMLHooks'>
        <CAPITAL_EVENT_REFERENCE><acmCode function = 'CAPITAL_EVENT_REFERENCE'/></CAPITAL_EVENT_REFERENCE>
        <TOTAL_COUPON_PAYMENT><acmCode function = 'DATE'/><acmCode function = 'AMOUNT'/></TOTAL_COUPON_PAYMENT>
        <ACQUIRER_ACCOUNT><acmCode function = 'ACCOUNT_WITH_INSTITUTION_BIC'/></ACQUIRER_ACCOUNT>
        <COUNTERPARTY_ACCOUNT><acmCode function = 'ACCOUNT_WITH_INSTITUTION_BIC'/></COUNTERPARTY_ACCOUNT>
        <SENDER_TO_RECEIVER_INFO><acmCode function = 'SENDER_TO_RECEIVER_INFO'/></SENDER_TO_RECEIVER_INFO>
        <REC_CODE><acmCode function = 'GET_REC_CODE'/></REC_CODE>
        <YOUR_REFERENCE><acmCode function = 'YOUR_REFERENCE'/></YOUR_REFERENCE>
        <SWIFT_MESSAGE_TYPE>298</SWIFT_MESSAGE_TYPE>
        <RECEIVER_BIC><acmCode function = 'MT298_RECEIVER_BIC'/></RECEIVER_BIC>
        <SENDER_BIC><acmCode function = 'MT298_SENDER_BIC'/></SENDER_BIC>
        <MESSAGE_USER_REFERENCE><acmCode function = 'MESSAGE_USER_REFERENCE'/></MESSAGE_USER_REFERENCE>
        <SEQREF Field="20 M">FAS</SEQREF>         
    </SWIFT>
    <SETTLEMENT>
        <SEQNBR Field="20 M"><acmCode method ='Oid' ignoreUpdate ='True'/></SEQNBR>
    </SETTLEMENT>
</MESSAGE>
'''

MT402_template = '''\
<SWIFT file = 'FSettlementSwiftXMLHooks'>
    <ACCOUNT_WITH_INSTITUTION_ACCOUNT><acmCode function = 'ACCOUNT_WITH_INSTITUTION_ACCOUNT'/></ACCOUNT_WITH_INSTITUTION_ACCOUNT>
    <ACCOUNT_WITH_INSTITUTION_ADDRESS Field="57A M"></ACCOUNT_WITH_INSTITUTION_ADDRESS>
    <ACCOUNT_WITH_INSTITUTION_BIC><acmCode function = 'ACCOUNT_WITH_INSTITUTION_BIC'/></ACCOUNT_WITH_INSTITUTION_BIC>
    <ACCOUNT_WITH_INSTITUTION_NAME Field="57A O"></ACCOUNT_WITH_INSTITUTION_NAME>
    <ACCOUNT_WITH_INSTITUTION_OPTION><acmCode function = 'ACCOUNT_WITH_INSTITUTION_OPTION'/></ACCOUNT_WITH_INSTITUTION_OPTION>
    <BANK_OPERATION_CODE><acmCode function = 'GetBankOperationCode'/></BANK_OPERATION_CODE>
    <BENEFICIARY_CUSTOMER_ACCOUNT><acmCode function = 'BENEFICIARY_CUSTOMER_ACCOUNT'/></BENEFICIARY_CUSTOMER_ACCOUNT>
    <BENEFICIARY_CUSTOMER_ADDRESS></BENEFICIARY_CUSTOMER_ADDRESS>
    <BENEFICIARY_CUSTOMER_NAME><acmCode function = 'BENEFICIARY_CUSTOMER_NAME'/></BENEFICIARY_CUSTOMER_NAME>
    <BENEFICIARY_CUSTOMER_OPTION><acmCode function = 'BENEFICIARY_CUSTOMER_OPTION'/></BENEFICIARY_CUSTOMER_OPTION>
    <BENEFICIARY_INSTITUTION_ACCOUNT><acmCode function = 'BENEFICIARY_INSTITUTION_ACCOUNT_COV'/></BENEFICIARY_INSTITUTION_ACCOUNT>
    <BENEFICIARY_INSTITUTION_BIC><acmCode function = 'BENEFICIARY_INSTITUTION_BIC'/></BENEFICIARY_INSTITUTION_BIC>
    <BENEFICIARY_INSTITUTION_OPTION>A</BENEFICIARY_INSTITUTION_OPTION>
    <DETAILS_OF_CHARGES><acmCode function = 'DETAILS_OF_CHARGES'/></DETAILS_OF_CHARGES>
    <INTERBANK_SETTLED_AMOUNT><acmCode function = 'GetInterbankSettledAmount'/></INTERBANK_SETTLED_AMOUNT>
    <ORDERING_CUSTOMER_ADDRESS></ORDERING_CUSTOMER_ADDRESS>
    <ORDERING_CUSTOMER_ACCOUNT></ORDERING_CUSTOMER_ACCOUNT>
    <ORDERING_CUSTOMER_BIC><acmCode function = 'GetOrderingCustomerBic'/></ORDERING_CUSTOMER_BIC>
    <ORDERING_CUSTOMER_OPTION><acmCode function = 'GetOrderingCustomerOption'/></ORDERING_CUSTOMER_OPTION>
    <ORDERING_INSTITUTION_OPTION><acmCode function = 'ORDERING_INSTITUTION_OPTION'/></ORDERING_INSTITUTION_OPTION>
    <ORDERING_INSTITUTION_BIC><acmCode function = 'ORDERING_INSTITUTION_BIC'/></ORDERING_INSTITUTION_BIC>
    <ORDERING_INSTITUTION_ACCOUNT></ORDERING_INSTITUTION_ACCOUNT>
    <REMITTANCE_INFO><acmCode function = 'REMITTANCE_INFO'/></REMITTANCE_INFO>
    <REMITTANCE_INFO2><acmCode function = 'REMITTANCE_INFO2'/></REMITTANCE_INFO2>
    <SENDERS_CORRESPONDENT_BIC><acmCode function = 'SENDERS_CORRESPONDENT_BIC_COV'/></SENDERS_CORRESPONDENT_BIC>
    <SENDERS_CORRESPONDENT_OPTION><acmCode function = 'SENDERS_CORRESPONDENT_OPTION'/></SENDERS_CORRESPONDENT_OPTION>
    <SENDER_TO_RECEIVER_INFO><acmCode function = 'SENDER_TO_RECEIVER_INFO'/></SENDER_TO_RECEIVER_INFO>
    <SENDER_TO_RECEIVER_INFO2><acmCode function = 'SENDER_TO_RECEIVER_INFO2'/></SENDER_TO_RECEIVER_INFO2>
    <YOUR_REFERENCE><acmCode function = 'YOUR_REFERENCE'/></YOUR_REFERENCE>
    <RECEIVERS_CORRESPONDENT_BIC><acmCode function = 'RECEIVERS_CORRESPONDENT_BIC'/></RECEIVERS_CORRESPONDENT_BIC>
    <RECEIVERS_CORRESPONDENT_OPTION>A</RECEIVERS_CORRESPONDENT_OPTION>
    <RECEIVERS_CORRESPONDENT_ADDRESS></RECEIVERS_CORRESPONDENT_ADDRESS>
    <RECEIVERS_CORRESPONDENT_NAME></RECEIVERS_CORRESPONDENT_NAME>
    <RECEIVERS_CORRESPONDENT_ACCOUNT></RECEIVERS_CORRESPONDENT_ACCOUNT>
</SWIFT>
'''

MT540_template = '''\
<SWIFT file = 'FSettlementSwiftXMLHooks'>
    <DEAL_PRICE Field="90B O"><acmCode function = 'DEAL_PRICE'/></DEAL_PRICE>
    <INDICATOR Field="22F M" acmLoop = "INDICATORS">
        <INDICATOR_QUALIFIER Field="22F M"><acmCode function = 'GetQualifier'/></INDICATOR_QUALIFIER>
        <INDICATOR_INDICATOR Field="22F M"><acmCode function = 'GetIndicator'/></INDICATOR_INDICATOR>
    </INDICATOR>
    <PARTY acmLoop = "GET_PARTY_DETAILS">
        <PARTY_OPTION Field="95A M"><acmCode function = 'PARTY_OPTION'/></PARTY_OPTION>
        <PARTY_QUALIFIER Field="95A M"><acmCode function = 'GetPartyQualifier'/></PARTY_QUALIFIER>
        <PARTY_IDENTIFIER_CODE Field="95A M"><acmCode function = 'GetPartyIdentifierCode'/></PARTY_IDENTIFIER_CODE>
        <PARTY_COUNTRY_CODE Field="95A M"><acmCode function = 'GetPartyCountryCode'/></PARTY_COUNTRY_CODE>
        <PARTY_NAME Field="95A M"><acmCode function = 'PARTY_NAME'/></PARTY_NAME>
        <PARTY_ADDRESS Field="95A M"><acmCode function = 'GetPartyAddress'/></PARTY_ADDRESS>
        <PARTY_DATA_SOURCE_SCHEME Field="95A M"><acmCode function = 'GetDataSourceScheme'/></PARTY_DATA_SOURCE_SCHEME>
        <PARTY_PROPRIETARY_CODE Field="95A M"><acmCode function = 'GetPartyProprietaryCode'/></PARTY_PROPRIETARY_CODE>
        <PARTY_SAFEKEEPING_OPTION Field="97A O"><acmCode function = 'GetPartySafekeepingOptionOverridden'/></PARTY_SAFEKEEPING_OPTION>
        <PARTY_SAFEKEEPING_ACCOUNT Field="97A O"><acmCode function = 'GetPartySafekeepingAccount'/></PARTY_SAFEKEEPING_ACCOUNT>
        <PARTY_SAFEKEEPING_QUALIFIER Field="97A O"><acmCode function = 'GetPartySafekeepingQualifier'/></PARTY_SAFEKEEPING_QUALIFIER>
        <PARTY_NARRATIVE_NAME Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_NAME'/></PARTY_NARRATIVE_NAME>
        <PARTY_NARRATIVE_CURR Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_CURR'/></PARTY_NARRATIVE_CURR>
        <PARTY_NARRATIVE_AMOUNT Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_AMOUNT'/></PARTY_NARRATIVE_AMOUNT>
        <PARTY_NARRATIVE_CONTACT Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_CONTACT'/></PARTY_NARRATIVE_CONTACT>
    </PARTY>
</SWIFT>
'''

MT541_template = '''\
<SWIFT file = 'FSettlementSwiftXMLHooks'>
    <AMOUNT Field="19A M">
        <AMOUNT_QUALIFIER Field="19A M"><acmCode function = 'GetAmountQualifier'/></AMOUNT_QUALIFIER>
        <AMOUNT_SIGN Field="19A M"></AMOUNT_SIGN>
        <AMOUNT_CURRENCY_CODE Field="19A M"><acmCode function = 'GetCurrencyCode'/></AMOUNT_CURRENCY_CODE>
        <AMOUNT_AMOUNT Field="19A M"><acmCode function = 'AMOUNT_AMOUNT'/></AMOUNT_AMOUNT>
    </AMOUNT>
    <DEAL_PRICE Field="90B O"><acmCode function = 'DEAL_PRICE'/></DEAL_PRICE>
    <INDICATOR Field="22F M" acmLoop = "INDICATORS">
        <INDICATOR_QUALIFIER Field="22F M"><acmCode function = 'GetQualifier'/></INDICATOR_QUALIFIER>
        <INDICATOR_INDICATOR Field="22F M"><acmCode function = 'GetIndicator'/></INDICATOR_INDICATOR>
    </INDICATOR>
    <PARTY acmLoop = "GET_PARTY_DETAILS">
        <PARTY_OPTION Field="95A M"><acmCode function = 'PARTY_OPTION'/></PARTY_OPTION>
        <PARTY_QUALIFIER Field="95A M"><acmCode function = 'GetPartyQualifier'/></PARTY_QUALIFIER>
        <PARTY_IDENTIFIER_CODE Field="95A M"><acmCode function = 'GetPartyIdentifierCode'/></PARTY_IDENTIFIER_CODE>
        <PARTY_COUNTRY_CODE Field="95A M"><acmCode function = 'GetPartyCountryCode'/></PARTY_COUNTRY_CODE>
        <PARTY_NAME Field="95A M"><acmCode function = 'PARTY_NAME'/></PARTY_NAME>
        <PARTY_ADDRESS Field="95A M"><acmCode function = 'GetPartyAddress'/></PARTY_ADDRESS>
        <PARTY_DATA_SOURCE_SCHEME Field="95A M"><acmCode function = 'GetDataSourceScheme'/></PARTY_DATA_SOURCE_SCHEME>
        <PARTY_PROPRIETARY_CODE Field="95A M"><acmCode function = 'GetPartyProprietaryCode'/></PARTY_PROPRIETARY_CODE>
        <PARTY_SAFEKEEPING_OPTION Field="97A O"><acmCode function = 'GetPartySafekeepingOptionOverridden'/></PARTY_SAFEKEEPING_OPTION>
        <PARTY_SAFEKEEPING_ACCOUNT Field="97A O"><acmCode function = 'GetPartySafekeepingAccount'/></PARTY_SAFEKEEPING_ACCOUNT>
        <PARTY_SAFEKEEPING_QUALIFIER Field="97A O"><acmCode function = 'GetPartySafekeepingQualifier'/></PARTY_SAFEKEEPING_QUALIFIER>
        <PARTY_NARRATIVE_NAME Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_NAME'/></PARTY_NARRATIVE_NAME>
        <PARTY_NARRATIVE_CURR Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_CURR'/></PARTY_NARRATIVE_CURR>
        <PARTY_NARRATIVE_AMOUNT Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_AMOUNT'/></PARTY_NARRATIVE_AMOUNT>
        <PARTY_NARRATIVE_CONTACT Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_CONTACT'/></PARTY_NARRATIVE_CONTACT>
    </PARTY>
</SWIFT>
'''

MT542_template = '''\
<SWIFT file = 'FSettlementSwiftXMLHooks'>
    <DEAL_PRICE Field="90B O"><acmCode function = 'DEAL_PRICE'/></DEAL_PRICE>
    <INDICATOR Field="22F M" acmLoop = "INDICATORS">
        <INDICATOR_QUALIFIER Field="22F M"><acmCode function = 'GetQualifier'/></INDICATOR_QUALIFIER>
        <INDICATOR_INDICATOR Field="22F M"><acmCode function = 'GetIndicator'/></INDICATOR_INDICATOR>
    </INDICATOR>
    <PARTY acmLoop = "GET_PARTY_DETAILS">
        <PARTY_OPTION Field="95A M"><acmCode function = 'PARTY_OPTION'/></PARTY_OPTION>
        <PARTY_QUALIFIER Field="95A M"><acmCode function = 'GetPartyQualifier'/></PARTY_QUALIFIER>
        <PARTY_IDENTIFIER_CODE Field="95A M"><acmCode function = 'GetPartyIdentifierCode'/></PARTY_IDENTIFIER_CODE>
        <PARTY_COUNTRY_CODE Field="95A M"><acmCode function = 'GetPartyCountryCode'/></PARTY_COUNTRY_CODE>
        <PARTY_NAME Field="95A M"><acmCode function = 'PARTY_NAME'/></PARTY_NAME>
        <PARTY_ADDRESS Field="95A M"><acmCode function = 'GetPartyAddress'/></PARTY_ADDRESS>
        <PARTY_DATA_SOURCE_SCHEME Field="95A M"><acmCode function = 'GetDataSourceScheme'/></PARTY_DATA_SOURCE_SCHEME>
        <PARTY_PROPRIETARY_CODE Field="95A M"><acmCode function = 'GetPartyProprietaryCode'/></PARTY_PROPRIETARY_CODE>
        <PARTY_SAFEKEEPING_OPTION Field="97A O"><acmCode function = 'GetPartySafekeepingOptionOverridden'/></PARTY_SAFEKEEPING_OPTION>
        <PARTY_SAFEKEEPING_ACCOUNT Field="97A O"><acmCode function = 'GetPartySafekeepingAccount'/></PARTY_SAFEKEEPING_ACCOUNT>
        <PARTY_SAFEKEEPING_QUALIFIER Field="97A O"><acmCode function = 'GetPartySafekeepingQualifier'/></PARTY_SAFEKEEPING_QUALIFIER>
        <PARTY_NARRATIVE_NAME Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_NAME'/></PARTY_NARRATIVE_NAME>
        <PARTY_NARRATIVE_CURR Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_CURR'/></PARTY_NARRATIVE_CURR>
        <PARTY_NARRATIVE_AMOUNT Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_AMOUNT'/></PARTY_NARRATIVE_AMOUNT>
        <PARTY_NARRATIVE_CONTACT Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_CONTACT'/></PARTY_NARRATIVE_CONTACT>
    </PARTY>
</SWIFT>
'''

MT543_template = '''\
<SWIFT file = 'FSettlementSwiftXMLHooks'>
    <AMOUNT Field="19A M">
        <AMOUNT_QUALIFIER Field="19A M"><acmCode function = 'GetAmountQualifier'/></AMOUNT_QUALIFIER>
        <AMOUNT_SIGN Field="19A M"></AMOUNT_SIGN>
        <AMOUNT_CURRENCY_CODE Field="19A M"><acmCode function = 'GetCurrencyCode'/></AMOUNT_CURRENCY_CODE>
        <AMOUNT_AMOUNT Field="19A M"><acmCode function = 'AMOUNT_AMOUNT'/></AMOUNT_AMOUNT>
    </AMOUNT>
    <DEAL_PRICE Field="90B O"><acmCode function = 'DEAL_PRICE'/></DEAL_PRICE>
    <INDICATOR Field="22F M" acmLoop = "INDICATORS">
        <INDICATOR_QUALIFIER Field="22F M"><acmCode function = 'GetQualifier'/></INDICATOR_QUALIFIER>
        <INDICATOR_INDICATOR Field="22F M"><acmCode function = 'GetIndicator'/></INDICATOR_INDICATOR>
    </INDICATOR>
    <PARTY acmLoop = "GET_PARTY_DETAILS">
        <PARTY_OPTION Field="95A M"><acmCode function = 'PARTY_OPTION'/></PARTY_OPTION>
        <PARTY_QUALIFIER Field="95A M"><acmCode function = 'GetPartyQualifier'/></PARTY_QUALIFIER>
        <PARTY_IDENTIFIER_CODE Field="95A M"><acmCode function = 'GetPartyIdentifierCode'/></PARTY_IDENTIFIER_CODE>
        <PARTY_COUNTRY_CODE Field="95A M"><acmCode function = 'GetPartyCountryCode'/></PARTY_COUNTRY_CODE>
        <PARTY_NAME Field="95A M"><acmCode function = 'PARTY_NAME'/></PARTY_NAME>
        <PARTY_ADDRESS Field="95A M"><acmCode function = 'GetPartyAddress'/></PARTY_ADDRESS>
        <PARTY_DATA_SOURCE_SCHEME Field="95A M"><acmCode function = 'GetDataSourceScheme'/></PARTY_DATA_SOURCE_SCHEME>
        <PARTY_PROPRIETARY_CODE Field="95A M"><acmCode function = 'GetPartyProprietaryCode'/></PARTY_PROPRIETARY_CODE>
        <PARTY_SAFEKEEPING_OPTION Field="97A O"><acmCode function = 'GetPartySafekeepingOptionOverridden'/></PARTY_SAFEKEEPING_OPTION>
        <PARTY_SAFEKEEPING_ACCOUNT Field="97A O"><acmCode function = 'GetPartySafekeepingAccount'/></PARTY_SAFEKEEPING_ACCOUNT>
        <PARTY_SAFEKEEPING_QUALIFIER Field="97A O"><acmCode function = 'GetPartySafekeepingQualifier'/></PARTY_SAFEKEEPING_QUALIFIER>
        <PARTY_NARRATIVE_NAME Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_NAME'/></PARTY_NARRATIVE_NAME>
        <PARTY_NARRATIVE_CURR Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_CURR'/></PARTY_NARRATIVE_CURR>
        <PARTY_NARRATIVE_AMOUNT Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_AMOUNT'/></PARTY_NARRATIVE_AMOUNT>
        <PARTY_NARRATIVE_CONTACT Field="70C O"><acmCode function = 'GET_PARTY_NARRATIVE_CONTACT'/></PARTY_NARRATIVE_CONTACT>
    </PARTY>
</SWIFT>
'''

commonBlock_template = '''\
<SWIFT file = 'FSettlementSwiftXMLHooks'>
    <RECEIVER_BIC><acmCode function = 'RECEIVER_BIC'/></RECEIVER_BIC>
    <RECEIVER_BIC2><acmCode function = 'RECEIVER_BIC2'/></RECEIVER_BIC2>
    <SENDER_BIC><acmCode function = 'SENDER_BIC'/></SENDER_BIC>
    <TRADING_DESK><acmCode function = 'TRADING_DESK'/></TRADING_DESK>
</SWIFT>
'''


def set_test_bic(txt, index=8):
    if txt != '':
        return txt[:index - 1] + '0' + txt[index:]
    else:
        return ''


def format_number_for_swift(val):
    return str(val).replace('.', ',')


def get_cash_account_from_sor(settlement):
    acquirer_sor_account = settlement.Trade().AdditionalInfo().Demat_Acq_SOR_Ac()
    acc = [a for a in settlement.Acquirer().Accounts() if a.Depository() == acquirer_sor_account]
    return acc


def _get_account(settlement, account_type, settlement_type=None):

    counterparty = settlement.Counterparty()
    settle_instructions = counterparty.SettleInstructions()

    def _return_account(settle_instruction):
        if len(settle_instruction.Rules()) > 0:
            for rule in settle_instruction.Rules():
                if rule.EffectiveTo() != '':
                    continue
                if account_type == 'Cash':
                    return rule.CashAccount()
                elif account_type == 'Cash and Security':
                    return rule.SecAccount()

        return None

    for settle_instruction in settle_instructions:
        if settle_instruction.AccountType() == account_type:
            currency_name = settlement.Currency().Name()
            if currency_name != settle_instruction.QueryAttributeCurrency():
                continue
            if not settle_instruction.QueryFilter():
                continue
            filter_nodes = [node.Value().StringKey() for node in settle_instruction.QueryFilter().AsqlNodes()]
            if settlement_type is None:
                payment_type_node = [node for node in filter_nodes if 'Type = ' in node]
                if not payment_type_node:
                    return _return_account(settle_instruction)
            else:
                payment_type_node = [node for node in filter_nodes if 'Type = ' in node]
                if not payment_type_node:
                    continue
                payment_types = payment_type_node[0].split('= ')[1].split(', ')
                if settlement_type in payment_types:
                    return _return_account(settle_instruction)

    return None


def SENDER_BIC(fobj):
    """
    field 1 in all settlement headers
    """
    sender_address = 'NODESBIC'
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()
        account = settlement.AcquirerAccountRef()
        sender_address = account.Party().Swift()

    if TESTMESSAGES:
        sender_address = set_test_bic(sender_address)
    return sender_address


def RECEIVER_BIC(fobj):
    """
    field 2 in all settlement headers except 202Cov
    """
    destination_address = 'NODESBIC'
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()
        if not is_demat(settlement):
            if settlement.MTMessages() == '202' and settlement.Currency().Name() != 'ZAR':
                destination_address = get_our_curr_nostro_swift(settlement)
            elif settlement.MTMessages() in ('103', '202'):
                accounts = settlement.Counterparty().Accounts()
                for acc in accounts:
                    if acc.Name() == settlement.CounterpartyAccName():
                        destination_address = acc.Bic().Name()
            else:
                destination_address = GetReceiverBic(settlement)
        else:
            if is_demat_initial_settmnt(settlement):
                destination_address = 'SCBLZAJJ'
            else:
                if settlement.AdditionalInfo().ACC_WTH_INSTITUTION():
                    destination_address = settlement.AdditionalInfo().ACC_WTH_INSTITUTION().split(' & ')[0]

    if TESTMESSAGES:
        destination_address = set_test_bic(destination_address)
    return destination_address


def RECEIVER_BIC2(fobj):
    """
    field 2 in 202Cov headers
    """
    destination_address = 'NODESBIC'
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()
        if not is_demat(settlement):
            if settlement.Currency().Name() != 'ZAR':
                destination_address = get_our_curr_nostro_swift(settlement)
            else:
                destination_address = get_corr_bank_curr_corr_bank_SWIFT(settlement)

    if TESTMESSAGES:
        destination_address = set_test_bic(destination_address)
    return destination_address


def ORDERING_INSTITUTION_BIC(settlement):
    if TESTMESSAGES:
        return 'ABSAZAJ0'
    else:
        return 'ABSAZAJJ'


def get_corr_bank_curr_corr_bank_SWIFT(settlement):
    """
    function used in RECEIVER_BIC2 and RECEIVERS_CORRESPONDENT_BIC
    """
    if settlement.TheirCorrBank():
        for acc in acm.FParty[settlement.TheirCorrBank()].Accounts():
            if acc.Currency() == settlement.Currency():
                return acc.CorrespondentBank().Swift()

    return 'NOCORBIC'


def get_corr_bank_curr_corr_bank_account(settlement):
    """
    function used in BENEFICIARY_INSTITUTION_ACCOUNT_COV
    """
    corr_bank_curr_corr_bank_account = 'NOCORBIC'
    if settlement.TheirCorrBank():
        for acc in acm.FParty[settlement.TheirCorrBank()].Accounts():
            if acc.Currency() == settlement.Currency():
                corr_bank_curr_corr_bank_account = acc.Account()
                break
    return corr_bank_curr_corr_bank_account


def ACCOUNT_WITH_INSTITUTION_OPTION(fobj):
    """
    field 57 on MT103COV and MT202
    """
    acc_with_inst_option = "A"
    settlement = fobj.Settlement()
    if not is_demat(settlement):
        account = settlement.CounterpartyAccountRef()
        if settlement.MTMessages() == '202' and settlement.Currency().Name() == 'ZAR':
            if account:
                if not account.Bic2():
                    acc_with_inst_option = ""
    return acc_with_inst_option


def ACCOUNT_WITH_INSTITUTION_BIC(fobj):
    acc_with_inst_bic = ""
    settlement = fobj.Settlement()
    if not is_demat(settlement):
        account = settlement.CounterpartyAccountRef()
        if settlement.MTMessages() == '202' and settlement.Currency().Name() == 'ZAR':
            if account.Bic2():
                acc_with_inst_bic = account.Bic2().Name()
        else:
            if account.Bic():
                acc_with_inst_bic = account.Bic().Name()
    else:
        if is_demat_initial_settmnt(settlement):
            cashAcc = get_cash_account_from_sor(settlement)
            if cashAcc:
                acc_with_inst_bic = cashAcc[0].Bic().Name()
        else:
            acc_with_inst_bic = settlement.AdditionalInfo().ACC_WTH_INSTITUTION().split(' & ')[0]
    if TESTMESSAGES:
        acc_with_inst_bic = set_test_bic(acc_with_inst_bic)

    return acc_with_inst_bic


def ACCOUNT_WITH_INSTITUTION_ACCOUNT(fobj):
    acc_with_inst_account = ""
    settlement = fobj.Settlement()
    if not is_demat(settlement):
        account = settlement.CounterpartyAccountRef()
        if settlement.MTMessages() == '103':
            findSpace = account.Account().find(' ')
            if findSpace != -1:
                acc_with_inst_account = '/ZA' + account.Account()[:findSpace]
        elif settlement.MTMessages() == '402':
            findSpace = account.Account().find(' ')
            if findSpace != -1:
                acc_with_inst_account = '/' + account.Account()[:findSpace]
        elif settlement.MTMessages() == '202' and settlement.Currency().Name() == 'ZAR':
            if not account.Account2().__contains__('DIRECT'):
                findSpace = account.Account2().find(' ')
                if findSpace != -1:
                    acc_with_inst_account = account.Account2()[findSpace + 1:]
                else:
                    acc_with_inst_account = account.Account2()
    else:
        if is_demat_initial_settmnt(settlement):
            acc_with_inst_account = '/ZA730020' #Might change again
        else:
            acc_with_inst_account = '/' + settlement.AdditionalInfo().ACC_WTH_INSTITUTION().split(' & ')[1]
    return acc_with_inst_account


def BENEFICIARY_CUSTOMER_ACCOUNT(fobj):
    """
    For a debit the beneficiary (59) and ordering customer (50) fields swap around
    """
    beneficiary_customer_account = ''
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()
        if not is_demat(settlement):
            if settlement.Amount() > 0:
                beneficiary_customer_account = settlement.AcquirerAccount()
            else:
                beneficiary_customer_account = settlement.CounterpartyAccount()

            findSpace = beneficiary_customer_account.find(' ')
            if findSpace != -1:
                beneficiary_customer_account = beneficiary_customer_account[findSpace+1:]
        else:
            cashAcc = get_cash_account_from_sor(settlement)
            if cashAcc:
                beneficiary_customer_account = cashAcc[0].Account()

    return beneficiary_customer_account


def BENEFICIARY_CUSTOMER_NAME(fobj):
    """
    For a debit the beneficiary (59) and ordering customer (50) fields swap around
    """
    beneficiary_customer_name = ''
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()
        if not is_demat(settlement):
            if settlement.Amount() > 0:
                beneficiary_customer_name = OUR_BANK
            else:
                beneficiary_customer_name = (
                    settlement.Counterparty().Fullname()
                    or settlement.Counterparty().Name()
                    or beneficiary_customer_name
                )
        else:
            cashAcc = get_cash_account_from_sor(settlement)
            if cashAcc:
                beneficiary_customer_name = cashAcc[0].Name()
    return beneficiary_customer_name


def BENEFICIARY_CUSTOMER_OPTION(fobj):
    if fobj.IsKindOf(acm.FSettlement):
        return "NO OPTION"


def BENEFICIARY_INSTITUTION_OPTION(fobj):
    """
    field 58 on MT202
    """
    settlement = fobj.Settlement()
    if not is_demat(settlement):
        return 'A'
    else:
        return 'D'


def BENEFICIARY_INSTITUTION_NAME(fobj):
    settlement = fobj.Settlement()
    if is_demat(settlement):
        return settlement.AdditionalInfo().BENEF_INSTITUTION().split(' & ')[0]

    return ""


def BENEFICIARY_INSTITUTION_BIC(fobj):
    beneficiary_institution_bic = ''
    settlement = fobj.Settlement()
    if not is_demat(settlement):
        account = settlement.CounterpartyAccountRef()
        beneficiary_institution_bic = GetPartyBic(account)
        if beneficiary_institution_bic == '':
            beneficiary_institution_bic = acm.FParty[settlement.TheirCorrBank()].Swift()

    if TESTMESSAGES:
        beneficiary_institution_bic = set_test_bic(beneficiary_institution_bic)
    return beneficiary_institution_bic


def BENEFICIARY_INSTITUTION_ACCOUNT(fobj):
    beneficiary_institution_account = ''
    settlement = fobj.Settlement()
    if not is_demat(settlement):
        beneficiary_institution_account = settlement.CounterpartyAccount()
        if ('DIRECT' in beneficiary_institution_account) or ('direct' in beneficiary_institution_account):
            beneficiary_institution_account = ''
        else:
            find_space = beneficiary_institution_account.find(' ')
            if find_space != -1:
                beneficiary_institution_account = beneficiary_institution_account[find_space+1:]
    else:
        beneficiary_institution_account = settlement.AdditionalInfo().BENEF_INSTITUTION().split(' & ')[1]

    return beneficiary_institution_account


def BENEFICIARY_INSTITUTION_ACCOUNT_COV(fobj):
    """
    field 58 on MT202 Cover
    """
    settlement = fobj.Settlement()
    beneficiary_institution_account = get_corr_bank_curr_corr_bank_account(settlement)
    if ('DIRECT' in beneficiary_institution_account) or ('direct' in beneficiary_institution_account):
        beneficiary_institution_account = ''
    else:
        find_space = beneficiary_institution_account.find(' ')
        if find_space != -1:
            beneficiary_institution_account = beneficiary_institution_account[find_space+1:]
    return beneficiary_institution_account


def DETAILS_OF_CHARGES(fobj):
    return "OUR"


def ORDERING_CUSTOMER_ACCOUNT(fobj):
    """
    For a debit the beneficiary (59) and ordering customer (50) fields swap around
    """
    ordering_customer_account = ''
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()
        if settlement.Amount() > 0:
            ordering_customer_account = settlement.CounterpartyAccount()
        else:
            ordering_customer_account = settlement.AcquirerAccount()

        find_space = ordering_customer_account.find(' ')
        if find_space != -1:
            ordering_customer_account = ordering_customer_account[find_space+1:]
    return ordering_customer_account


def ORDERING_CUSTOMER_NAME(fobj):
    """
    For a debit the beneficiary (59) and ordering customer (50) fields swap around
    """
    ordering_customer_name = ''
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()
        if settlement.Amount() > 0:
            ordering_customer_name = (
                settlement.Counterparty().Fullname()
                or settlement.Counterparty().Name()
                or ordering_customer_name
            )
        else:
            ordering_customer_name = OUR_BANK
    return ordering_customer_name


def ORDERING_INSTITUTION_OPTION(fobj):
    """
    field 52 on an MT103 and MT202
    """
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()
        if ((settlement.MTMessages() == '202' and settlement.Currency().Name() == 'ZAR') or
                settlement.MTMessages() in ('103', '402')):
            return 'A'

    return ""


def CHECK_CP_REF(settlement):
    if settlement.AdditionalInfo().Ext_CP_Ref_Sett():
        return settlement.AdditionalInfo().Ext_CP_Ref_Sett()
    else:
        trade = get_trd_from_possible_nettsettle(settlement)
        if trade and trade.Counterparty().AdditionalInfo().Ext_CP_Ref():
            return trade.Counterparty().AdditionalInfo().Ext_CP_Ref()
    return None


def REMITTANCE_INFO2(fobj):
    """
    Remittance information : field70 --MT103 and 202Cov
    """
    settlement = fobj.Settlement()
    if settlement.Currency().Name() != 'ZAR':
        return REMITTANCE_INFO(fobj)

    return None


def REMITTANCE_INFO(fobj):
    remittance_info = ''
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()

        trade = get_trd_from_possible_nettsettle(settlement)
        cash_flow_oid = ""
        if trade:
            if not is_demat(settlement):
                trade_oid = str(trade.Oid())
                instrument = trade.Instrument()
                if settlement.Acquirer().Name() in ('Funding Desk', 'Money Market Desk'):
                    if instrument.InsType() == "FRN":
                        remittance_info = "FRN"
                    elif instrument.InsType() == "Deposit":

                        if instrument.IsCallAccount():
                            if trade.Quantity() == 1:
                                remittance_info = "CALLDEP"
                            else:
                                remittance_info = "CALLWIT"

                            if settlement.CashFlow():
                                cash_flow_oid = str(settlement.CashFlow().Oid())
                                remittance_info = remittance_info+"/"+cash_flow_oid
                            else:
                                remittance_info = remittance_info+"/"+trade_oid
                        else:
                            if instrument.NominalAmount() > 0:
                                remittance_info = "FIXEDDEP"
                            else:
                                remittance_info = "FIXEDLOAN"

                    seq = (remittance_info, OUR_BANK)
                    remittance_info = GLOBAL_SEPARATOR.join(seq)

                elif settlement.Acquirer().Name() == "Gold Desk":
                    remittance_info = "GLD_9923CC"

                elif settlement.Acquirer().Name() == "Metals Desk":
                    remittance_info = "MET_0319CC"

                elif settlement.Acquirer().Name() == "PRIME SERVICES DESK":
                    remittance_info = "PAYMENT"

                else:
                    if instrument.InsType() != 'Option':
                        remittance_info = instrument.InsType().upper()
                    else:
                        remittance_info = "Premium"
                separator = "_"
                seq = (remittance_info, trade_oid)
                remittance_info = separator.join(seq)
            else:
                remittance_info = 'Settlement Funding ' + str(trade.Oid())

        if CHECK_CP_REF(settlement):
            remittance_info = CHECK_CP_REF(settlement)

    return remittance_info


def RECEIVERS_CORRESPONDENT_BIC(fobj):
    """
    Field 54 on 103 and 57 on 202 for cover payment 402
    """
    corr_bank_curr_corr_bank_SWIFT = 'NOCORBIC'
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()
        corr_bank_curr_corr_bank_SWIFT = get_corr_bank_curr_corr_bank_SWIFT(settlement)

    if TESTMESSAGES:
        corr_bank_curr_corr_bank_SWIFT = set_test_bic(corr_bank_curr_corr_bank_SWIFT)
    return corr_bank_curr_corr_bank_SWIFT


def get_our_curr_nostro_swift(fobj):
    """
    function used in RECEIVER_BIC and SENDERS_CORRESPONDENT_BIC_COV
    """
    our_curr_nostro_swift = ''
    settlement = fobj.Settlement()
    party = acm.FParty[OUR_BANK]
    for acc in party.Accounts():
        if acc.Currency() == settlement.Currency():
            _curr = acc.Currency().Name()
            if _curr != 'ZAR' or (_curr == 'ZAR' and acc.CorrespondentBank().Name() == OUR_BANK):
                our_curr_nostro_swift = acc.CorrespondentBank().Swift()
    return our_curr_nostro_swift


def is_dis_settlmt(settlement):
    """
    function used in SENDERS_CORRESPONDENT_ACCOUNT and YOUR_REFERENCE
    """
    return bool(
        is_dis(settlement) or ('Net' in settlement.RelationType() and is_dis(settlement.Children()[0]))
    )


def SENDERS_CORRESPONDENT_BIC_COV(fobj):
    """
    field53 --MT103 Cov
    """
    our_curr_nostro_swift = ''
    if fobj.IsKindOf(acm.FSettlement):
        our_curr_nostro_swift = get_our_curr_nostro_swift(fobj)

    if TESTMESSAGES:
        our_curr_nostro_swift = set_test_bic(our_curr_nostro_swift)

    return our_curr_nostro_swift


def SENDERS_CORRESPONDENT_BIC(fobj):
    """
    field53 --MT103, MT202
    """
    if TESTMESSAGES:
        return 'SARBZAJ0'
    else:
        if int(time.strftime('%H')) >= 15 and int(time.strftime('%M')) >= 30:
            return 'SARBZAJ2'
        return 'BKSVZAJJ'


def SENDERS_CORRESPONDENT_LOCATION(fobj):
    settlement = fobj.Settlement()
    if is_dis_settlmt(settlement):
        senders_corr_acc = GetSendersCorrespondentAccount(settlement)
        if ' ' in senders_corr_acc:
            senders_corr_acc = senders_corr_acc.split(' ')[1]
        return '/' + senders_corr_acc
    else:
        return '/MMARK'


def SENDERS_CORRESPONDENT_OPTION(fobj):
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()
        if is_demat(settlement) or is_dis_settlmt(settlement):
            return 'B'
        elif ((settlement.MTMessages() == '202' and settlement.Currency().Name() == 'ZAR')
              or settlement.MTMessages() in ('103', '402')):
            return 'A'
    return ""


def get_rec_code_qf_name(settlement):
    """
    function used in SENDER_TO_RECEIVER_INFO
    """
    rec_code_queries = [q.Name() for q in acm.FStoredASQLQuery.Select('') if 'SwiftSenderToReceiver_' in q.Name()]
    for qf in rec_code_queries:
        if acm.FStoredASQLQuery[qf].Query() and acm.FStoredASQLQuery[qf].Query().IsSatisfiedBy(settlement):
            return qf.split('_')[1]
    return ''


def traverse(settlement):
    """
    handle cross trade net structures with sub-net structure that have same rec codes
    """
    if settlement.Children() and not settlement.Trade():
        for child in settlement.Children():
            traverse.code = get_rec_code_qf_name(child)
            if traverse.code:
                traverse.unique_codes.add(traverse.code)
            traverse(child)

    elif settlement.Trade():
        traverse.code = get_rec_code_qf_name(settlement)
        if traverse.code:
            traverse.unique_codes.add(traverse.code)

    if len(traverse.unique_codes) == 1:
        return ''.join(traverse.unique_codes)

    if len(traverse.unique_codes) > 1:
        print len(traverse.unique_codes), traverse.unique_codes
    return traverse.code


def get_rec_code(settlement):
    if settlement.SplitParent():
        settlement = settlement.SplitParent()
    elif settlement.PairOffParent():
        settlement = settlement.PairOffParent()
    elif settlement.PartialParent():
        settlement = settlement.PartialParent()

    traverse.code = ''
    traverse.level = 1
    traverse.unique_codes = set()
    return traverse(settlement)


def acc_type(account_number):
    if re.match('^[0-9]{6}[A-Z,a-z]{3}[0-9]{6}$', account_number):
        if account_number[6:9] == 'ZAR':
            return 'VOS'
        else:
            return 'CFC'
    return 'CHQ'


def SENDER_TO_RECEIVER_INFO2(fobj):
    """
    sender to receiver info --> field 72 on Cov MT202
    """
    sender_receiver_info2 = '/REC/DTBNK '
    return sender_receiver_info2


def SENDER_TO_RECEIVER_INFO(fobj):
    sender_receiver_info = ''
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()

        if settlement.MTMessages() in ('103', '202', '298', '402') and settlement.Currency().Name() == 'ZAR':
            sender_receiver_info = get_rec_code(settlement)
            if 'STCAB' in sender_receiver_info:
                CPL_Agree = AbsaXmlConfigSettings().GetValue(absa_swift_param, 'CplAgreementNumber', True)
                sender_receiver_info += CPL_Agree

            if settlement.MTMessages() == '202':
                if CHECK_CP_REF(settlement):
                    sender_receiver_info += "newline" + CHECK_CP_REF(settlement)

            if settlement.MTMessages() == '298':
                return '/REC/' + sender_receiver_info

            sender_receiver_info = '/REC/' + sender_receiver_info + '/'
            if get_is_internal(settlement):
                sender_receiver_info = get_field72_account_information(settlement, sender_receiver_info)
                return sender_receiver_info

            return sender_receiver_info

        elif settlement.Currency().Name() != 'ZAR':
            if settlement.MTMessages() == '202':
                if REMITTANCE_INFO(settlement) != '':
                    sender_receiver_info += REMITTANCE_INFO(settlement)

                sender_receiver_info = '/BNF/' + sender_receiver_info + '/'
                if get_is_internal(settlement):
                    sender_receiver_info = get_field72_account_information(settlement, sender_receiver_info)
                    return sender_receiver_info

                return sender_receiver_info

            elif settlement.MTMessages() == '103':
                counterparty_account_type = get_account_type(settlement)
                if counterparty_account_type == 'CFC':
                    sender_receiver_info = '/REC/' + sender_receiver_info + '/'
                    if get_is_internal(settlement):
                        sender_receiver_info = get_field72_account_information(settlement, sender_receiver_info)
                        return sender_receiver_info

                    return sender_receiver_info

                return ''

    return sender_receiver_info


def get_field72_account_information(settlement, sender_receiver_info):
    """
    Populates the account information for internal settlements
    """
    account_type = get_account_type(settlement)
    if account_type == 'CFC':
        acquirer_account = GL_Acc(settlement.Currency().Name())
        acquirer_account_type = 'NOS'
    else:
        acquirer_account = settlement.AcquirerAccount()
        acquirer_account_type = acc_type(acquirer_account)

    account_info = 'newlineACCOUNTING-INFO'
    if settlement.Amount() <= 0:
        account_info = account_info + 'newlineDR-' + acquirer_account_type + 'newlineCR-' + account_type
    else:
        account_info = account_info + 'newlineDR-' + account_type + 'newlineCR-' + acquirer_account_type
    sender_receiver_info = sender_receiver_info + account_info
    if acc_type(settlement.CounterpartyAccount()) == 'CFC':
        if settlement.Amount() <= 0:
            sender_receiver_info = sender_receiver_info + 'newlineDRACC-' + acquirer_account
        else:
            sender_receiver_info = sender_receiver_info + 'newlineCRACC-' + acquirer_account

    return sender_receiver_info


def get_account_type(settlement):
    """
    returns account type for Settlement counterparty
    """
    counterparty_account = settlement.CounterpartyAccount()
    counterparty_account_type = acc_type(counterparty_account)

    return counterparty_account_type


def TRADING_DESK(fobj):
    """
    Header for all settlements --> field 108
    DER - Derivatives Desk (= Derivatives cash book)
    MMA - Money Market Desk (= Money Market cash book)
    """
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()
        trade = get_trd_from_possible_nettsettle(settlement)
        if _is_sbl_collateral_settlement(settlement):
            if trade.Portfolio().Name() == 'Call_SBL_Agency_Collateral':
                if settlement.Type() in ('Fixed Amount', 'Call Fixed Rate Adjustable'):
                    return 'MMA'
            return 'SBLCOL'

        if not is_demat(settlement):
            if is_dis_settlmt(settlement):
                return "DIS"
            else:
                if settlement.Acquirer().Name() in ('Funding Desk', 'Money Market Desk', 'COLLATERAL DESK'):
                    if trade.Instrument().InsType() in ('Cap', 'CurrSwap', 'Floor', 'FRA', 'IndexLinkedSwap', 'Swap'):
                        return "DER"
                    return "MMA"
                return "DER"

    return ""


def _is_sbl_collateral_settlement(settlement):
    """
    Checks settlement against SBL Collateral Criteria for MMA trading desk
    """
    trade = get_trd_from_possible_nettsettle(settlement)
    if settlement.Acquirer().Name() != 'PRIME SERVICES DESK':
        return False
    if trade and trade.Instrument().InsType() != 'Deposit':
        return False
    if trade.Instrument().ExternalId1() != trade.Counterparty().AdditionalInfo().SL_G1PartyCode():
        return False

    return True


def get_child_settlement_cashflow(settlement):
    for child in settlement.Children():
        if child.CashFlow():
            return child

    return None


def YOUR_REFERENCE(fobj):
    """
    Related Reference --> field 21-->MT202
    """
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()
        if is_dis_settlmt(settlement):
            if settlement.CashFlow():
                if settlement.CashFlow().AdditionalInfo().Demat_CE_Reference():
                    ref = settlement.CashFlow().AdditionalInfo().Demat_CE_Reference()
                    return ref[0:4] + 'CEB' + ref[4:]

            elif not settlement.CashFlow() and settlement.Payment():
                ref = settlement.Payment().Text()
                return ref[0:4] + 'CEB' + ref[4:]

            elif settlement.RelationType() == 'Net':
                child_set = get_child_settlement_cashflow(settlement)
                if child_set:
                    if child_set.CashFlow().AdditionalInfo().Demat_CE_Reference():
                        ref = child_set.CashFlow().AdditionalInfo().Demat_CE_Reference()
                        return ref[0:4] + 'CEB' + ref[4:]

        elif is_demat(settlement):
            if settlement.AdditionalInfo().Call_Confirmation():
                return settlement.AdditionalInfo().Call_Confirmation()

    return 'NONREF'


def GetTradeDate(fobj):
    if fobj.IsKindOf(acm.FSettlement):
        if fobj.Trade():
            return acm.Time.DateFromTime(fobj.Trade().TradeTime())
    return ''


def GetCounterpartySafeAccount(fobj):
    """
    Get CounterParty Safe Account
    """
    if fobj.IsKindOf(acm.FSettlement):
        if fobj.CounterpartyAccount() != '':
            return fobj.CounterpartyAccount()
    return ''


def _get_euroclear_account(trade, currency_name = None):
    """
    Returns the euroclear cash account to be used.
    """

    def _get_settle_instruction(settle_instruction):
        settle_rule = None
        if len(settle_instruction.Rules()) > 1:
            for rule in settle_instruction.Rules():
                if rule.EffectiveTo() == '':
                    settle_rule = rule
                    break
        elif len(settle_instruction.Rules()) == 1:
            settle_rule = settle_instruction.Rules()[0]
        return settle_rule.CashAccount()

    if currency_name is None:
        currency_name = trade.Currency().Name()

    party = acm.FParty['EUROCLEAR BANK']
    currency_filter = 'Currency = {}'.format(currency_name)
    category_filter = 'Trade Settle Category = Euroclear'
    ssi = None

    for settle_instruction in party.SettleInstructions():
        if not settle_instruction.QueryFilter():
            continue
        filter_nodes = []
        filter_nodes = [node.Value().StringKey() for node in settle_instruction.QueryFilter().AsqlNodes()]

        if category_filter in filter_nodes:
            if not settle_instruction.Currency():
                if currency_filter in filter_nodes:
                    ssi = _get_settle_instruction(settle_instruction)

            elif settle_instruction.Currency().Name() == currency_name:

                if category_filter in filter_nodes:
                    ssi = _get_settle_instruction(settle_instruction)
    return ssi


def GET_NetworkAlias(fobj):
    """
    Returns the Network Alias based on the euroclear account.
    """
    if fobj.Trade() and fobj.Trade().SettleCategoryChlItem():
        if fobj.Trade().SettleCategoryChlItem().Name() == 'Euroclear':
            euroclear_account = _get_euroclear_account(fobj.Trade())
            return euroclear_account.NetworkAlias().Name()
    return ''


def GET_CORES_BANK_BIC(fobj):
    """
    Returns the corresponding bank bic based euroclear account.
    """
    if fobj.IsKindOf(acm.FSettlement):
        if fobj.Trade() and fobj.Trade().SettleCategoryChlItem():
            if fobj.Trade().SettleCategoryChlItem().Name() == 'Euroclear':
                euroclear_account = _get_euroclear_account(fobj.Trade())
                if euroclear_account:
                    return euroclear_account.Bic().Name()
    return ''


def GET_FIELD_56A_FOR_CUSTOM_210(fobj):
    """
    Returns Account Number for all Euroclear currencies but Subnetwork/BIC for EUR
    """
    if fobj.Trade().SettleCategoryChlItem().Name() == 'Euroclear' and fobj.Trade().Currency().Name() == 'EUR':
        euroclear_account = _get_euroclear_account(fobj.Trade())
        if euroclear_account and euroclear_account.SubNetworkChlItem():
            return euroclear_account.SubNetworkChlItem().Name()

    return GET_CORES_BANK_BIC(fobj)


def GET_FIELD_57A_FOR_CUSTOM_202(fobj):
    """
    Returns Account Number for all Euroclear currencies but Subnetwork/BIC for EUR
    """
    currency_name = get_payment_currency_name(fobj)
    euroclear_account = None
    if is_valid_curr_euroclear_payment(fobj) and currency_name in VALID_PAYMENT_CURRENCIES_FOR_222:
        # Trade is used to find the currency which is used to filter out the SSI,
        # not required because currency is provided.
        euroclear_account = _get_euroclear_account(None, currency_name)
        if euroclear_account and euroclear_account.Bic():
            return euroclear_account.Account() # -- Return Account number not BIC

    if fobj.Trade().SettleCategoryChlItem().Name() == 'Euroclear':
        if currency_name == 'EUR':
            euroclear_account = _get_euroclear_account(fobj.Trade(), currency_name)

    if euroclear_account and euroclear_account.SubNetworkChlItem():
        return euroclear_account.SubNetworkChlItem().Name()

    return CP_CODE_CR(fobj)


def _get_settlement_euro_currency(settlement):
    """
    Returns 'EUR' currency from trade or payment.
    """
    trade = settlement.Trade()
    payment = settlement.Payment()

    trade_currency_name = None
    payment_currency = None

    if trade and trade.Currency():
        trade_currency_name = trade.Currency().Name()
    if payment and payment.Currency():
        payment_currency = payment.Currency().Name()
    if "EUR" in [trade_currency_name, payment_currency]:
        return "EUR"
    return None


def GET_VALUE_DATE(fobj):
    """
    Returns Settlement Value Date.
    """
    if fobj.IsKindOf(acm.FSettlement):
        return fobj.ValueDay()
    return ''


def GET_CASH_ACCOUNT_NUMBER(fobj):
    """
    Returns the Account Number based on Euroclear Account.
    """
    if fobj.IsKindOf(acm.FSettlement):
        currency_name = get_payment_currency_name(fobj)
        if is_valid_curr_euroclear_payment(fobj) and currency_name in VALID_PAYMENT_CURRENCIES_FOR_222:
            # Trade is used to find the currency which is used to filter out the SSI,
            # not required because currency is provided.
            euroclear_account = _get_euroclear_account(None, currency_name)
            if euroclear_account and euroclear_account.Bic():
                return euroclear_account.Bic().Name()  # -- Return Account number not BIC

        if fobj.Trade() and fobj.Trade().SettleCategoryChlItem():
            if fobj.Trade().SettleCategoryChlItem().Name() == 'Euroclear':
                return GET_CORES_BANK_BIC(fobj)

            return '/%s'% _get_account(fobj, 'Cash').Account()


def GET_SECURITY_ACCOUNT_NUMBER(fobj):
    """
    Returns Account number based on Trade Settle Category.
    """
    if fobj.IsKindOf(acm.FSettlement):
        if fobj.Trade() and fobj.Trade().SettleCategoryChlItem():
            if fobj.Trade().SettleCategoryChlItem().Name() == 'Euroclear':
                acquirer = fobj.Acquirer()
                for account in acquirer.Accounts():
                    if account.CorrespondentBank().Name() == 'EUROCLEAR BANK':
                        if account.Accounting() == 'Euroclear Custodian':
                            return account.Account()

        return _get_account(fobj, 'Cash', 'Premium').Account()
    return ''


def GET_SENDER_TO_RECEIVER_INFO(fobj):
    """
     Returns account based on currency for euroclear.
    """
    if fobj.IsKindOf(acm.FSettlement):
        if fobj.Currency().Name() != 'ZAR':
            return fobj.AcquirerAccount()
        filter_parms = ['Currency = ZAR', 'Amount >= 0.0']
        payment_type = 'Premium'
        return  GET_EUROCLEAR_SSI(fobj, filter_parms, payment_type).Account()


def GET_EUROCLEAR_SSI(settlement, filter_parms, payment_type):
    """
    Returns account based on the ssi which has to match
    filter parms.
    """
    for settle_instruction in settlement.Acquirer().SettleInstructions():
        filter_nodes = []
        if settle_instruction.QueryFilter():
            filter_nodes = [node.Value().StringKey() for node in settle_instruction.QueryFilter().AsqlNodes()]
            valid_payment = True
            if payment_type:
                type_node = [node.Value().StringKey() for node in settle_instruction.QueryFilter().AsqlNodes() if node.Value().StringKey().__contains__('Type = ')]
                if not str(type_node).__contains__(payment_type):
                    valid_payment = False
            if 'Trade Settle Category = Euroclear' in filter_nodes and valid_payment:
                node_check = set(filter_parms).issubset(set(filter_nodes))
                if node_check:
                    if len(settle_instruction.Rules()) > 1:
                        for rule in settle_instruction.Rules():
                            if rule.EffectiveTo() == '':
                                settle_rule = rule
                                break
                    elif len(settle_instruction.Rules()) == 1:
                        settle_rule = settle_instruction.Rules()[0]
                    return settle_rule.CashAccount()


def GET_ACQUIRER_ACC_NUM(fobj):
    """
    Returns acquirer account number based currency.
    """
    if fobj.IsKindOf(acm.FSettlement):
        if fobj.Currency().Name() !='ZAR':
            return fobj.AcquirerAccount()

        filter_parms = ['Currency = ZAR', 'Amount <= 0.0']
        payment_type = 'Premium'
        return  GET_EUROCLEAR_SSI(fobj, filter_parms, payment_type).Account()


def GET_FUNDING_TYPE(fobj):
    """
    Returns funding type based trade settle category.
    """
    if fobj.IsKindOf(acm.FSettlement):
        if fobj.Trade() and fobj.Trade().SettleCategoryChlItem():
            if fobj.Trade().SettleCategoryChlItem().Name() == 'Euroclear':
                return 'NON REF'
        return 'BOND FUNDING'
    return ''


def DATE(fobj):
    if fobj.IsKindOf(acm.FSettlement):
        value_day = datetime.datetime.strptime(fobj.ValueDay(), '%Y-%m-%d')
        return str(value_day.strftime('%y%m%d'))


def GET_CURRENCY(fobj):
    """
    Returns settlement currency name.
    """
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj
        return settlement.Currency().Name()
    return ''


def AMOUNT(fobj):
    """
    Returns a formatted amount value for a settlement.
    """
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj
        curr = settlement.Currency().Name()
        amount = str(abs(round(settlement.Amount(), 2)))

        if curr in ['UGX', 'JPY']:
            amount = str(abs(round(settlement.Amount(), 0)))
        if len(amount.split('.')) > 1:
            if Decimal(amount.split('.')[1]) == 0:
                amount = amount.split('.')[0] + ','

        val = '%s%s' % (curr, amount.replace('.', ','))
        return val
    return ''


def ALIAS(fobj):
    """
    Returns alias value based on trade settle category.
    """
    if fobj.IsKindOf(acm.FSettlement):
        if fobj.Trade() and fobj.Trade().SettleCategoryChlItem():
            if fobj.Trade().SettleCategoryChlItem().Name() == 'Euroclear':
                acquirer = fobj.Acquirer()
                for account in acquirer.Accounts():
                    if account.CorrespondentBank().Name() == 'EUROCLEAR BANK':
                        if account.Accounting() == 'Euroclear Custodian':
                            return account.NetworkAlias().Name()

        return _get_account(fobj, 'Cash', 'Premium').NetworkAlias().Name()
    return ''


def CP_CODE_DR(fobj):
    """
    Return cp code for debit account base trade settle category.
    """
    if fobj.IsKindOf(acm.FSettlement):
        account = _get_account(fobj, 'Cash')
        if fobj.Trade().SettleCategoryChlItem().Name() == 'Euroclear':
            instrument = fobj.Trade().Instrument()
            currency = instrument.Currency().Name()
            if instrument.InsType() == 'Repo/Reverse' and currency == 'ZAR':
                return CP_CODE_EUROCLER(fobj)
            acquirer = fobj.Acquirer()
            acc_num = fobj.AcquirerAccount()
            euro_account = None
            for account in acquirer.Accounts():
                if account.Account() == acc_num:
                    euro_account = account
                    break
            return euro_account.Bic().Name()
        return account.Bic().Name()
    return ''


def CP_CODE_EUROCLER(fobj):
    """
    Returns cp code for euroclear account based on currency.
     specifically for mt200
    """
    if fobj.IsKindOf(acm.FSettlement):
        if fobj.Currency().Name() == 'ZAR':
            filter_parms = ['Currency = ZAR', 'Amount >= 0.0']
            payment_type = 'Premium'
            return GET_EUROCLEAR_SSI(fobj, filter_parms, payment_type).Bic().Name()

        if fobj.Trade() and fobj.Trade().SettleCategoryChlItem():
            if fobj.Trade().SettleCategoryChlItem().Name() == 'Euroclear':
                euroclear_account = _get_euroclear_account(fobj.Trade())
                if euroclear_account:
                    return euroclear_account.Bic().Name()
    return ''


def CP_CODE_CR(fobj):
    """
    Returns cp code for credit account based
    on trade settle category.
    """
    if fobj.IsKindOf(acm.FSettlement):
        if fobj.Trade() and fobj.Trade().SettleCategoryChlItem():
            if fobj.Trade().SettleCategoryChlItem().Name() == 'Euroclear':
                euroclear_account = _get_euroclear_account(fobj.Trade())
                if euroclear_account:
                    return euroclear_account.Account()
        account = _get_account(fobj, 'Cash', 'Premium')
        return account.Bic().Name()
    return ''


def GET_RECEIVER_BIC(fobj):
    """
    Returns beneficiary bic value based on trade settle category.
    """
    if fobj.IsKindOf(acm.FSettlement):
        if fobj.Trade() and fobj.Trade().SettleCategoryChlItem():
            if fobj.Trade().SettleCategoryChlItem().Name() == 'Euroclear':
                currency_name = fobj.Currency().Name()
                if currency_name != 'ZAR':
                    filter_parms = ['Currency = %s' % currency_name]
                    payment_type = None
                    return  GET_EUROCLEAR_SSI(fobj, filter_parms, payment_type).Bic().Name()

                else:
                    filter_parms = ['Currency = ZAR', 'Amount <= 0.0']
                    payment_type = 'Premium'
                    return  GET_EUROCLEAR_SSI(fobj, filter_parms, payment_type).Bic().Name()

        return CP_CODE_DR(fobj)
    return ''

def INTERMEDIARY_ACCOUNT(fobj):
    """
    field 56 on MT202
    """
    intermediary_account = ''
    if fobj.IsKindOf(acm.FSettlement):
        settlement = fobj.Settlement()
        if settlement.CounterpartyAccountRef():
            intermediary_account = settlement.CounterpartyAccountRef().Account2()
    return intermediary_account


def INDICATORS(settlement):
    """
    field 22f in MT540s
    removed partial settlement check
    """
    indicators = acm.FList()
    # SETR.
    setr_pair = _get_setr_pair(settlement)
    indicators.Add(setr_pair)
    # RTGS.
    rtgs_pair = _get_rtgs_pair(settlement)
    if rtgs_pair:
        indicators.Add(rtgs_pair)
    # STCO.
    stco_pair = _get_stco_pair(settlement)
    if stco_pair:
        indicators.Add(stco_pair)
    # BENE.
    bene_pair = _get_bene_pair(settlement)
    if bene_pair:
        indicators.Add(bene_pair)
    return indicators


def _get_setr_pair(settlement):
    """
    Get the SETR (Type of Settlement Transaction) indicator pair for
    a settlement.
    """
    indicator = _get_setr_indicator(settlement)
    pair = acm.FPair()
    pair.First(acm.FSymbol('SETR'))
    pair.Second(acm.FSymbol(indicator))
    return pair


def _get_setr_indicator(settlement):
    """
    Get the indicator portion of the SETR indicator pair for the
    specified settlement.
    """
    settle_category = _get_trade_settle_category(settlement)
    trad_area = _get_trad_area(settlement)
    if settle_category == 'SA_CUSTODIAN':
        if trad_area in ['Internal Transfer', 'SARB Transfer']:
            # Internal Account Transfer.
            return 'OWNI'
        elif trad_area == 'External Transfer':
            # External Account Transfer.
            return 'OWNE'

    elif settle_category == 'Euroclear':
        # FAOPS-223 If trade category is set to Euroclear then
        # irrespective of instrument type the INDICATOR should
        # be defaulted to TRAD.
        trade_type = settlement.Trade().Type()
        if trad_area == 'External Transfer' and trade_type == 'Security Transfer':
            return 'OWNE'
        return 'TRAD'
    # Fallback on core logic.
    return GetMandatoryIndicator(settlement)


def _get_rtgs_pair(settlement):
    """
    Get the RTGS (Securities Real-Time Gross Settlement) indicator
    pair for a settlement, if applicable.
    """
    indicator = _get_rtgs_indicator(settlement)
    if indicator is None:
        return None
    pair = acm.FPair()
    pair.First(acm.FSymbol('RTGS'))
    pair.Second(acm.FSymbol(indicator))
    return pair


def _get_rtgs_indicator(settlement):
    """
    Get the indicator portion of the RTGS indicator pair for the
    specified settlement.
    """
    if settlement.TheirCorrBank() in ['EUROCLEAR BANK', 'CLEARSTREAM BANKING']:
        if settlement.Trade().AdditionalInfo().RTG():
            # Settle through the RTGS system.
            return 'YRTG'
        # Settle through the non-RTGS system.
        return 'NRTG'
    return None


def _get_stco_pair(settlement):
    """
    Get the STCO (Settlement Transaction Condition) indicator pair
    for a settlement, if applicable.
    """
    indicator = _get_stco_indicator(settlement)
    if indicator is None:
        return None
    pair = acm.FPair()
    pair.First(acm.FSymbol('STCO'))
    pair.Second(acm.FSymbol(indicator))
    return pair


def _get_stco_indicator(settlement):
    """
    Get the indicator portion of the STCO indicator pair for the
    specified settlement.
    """
    settle_category = _get_trade_settle_category(settlement)
    if settle_category == 'SA_CUSTODIAN':
        trad_area = _get_trad_area(settlement)
        if trad_area in ['External Transfer', 'Internal Transfer', 'SARB Transfer']:
            # Tax-exempt.
            return 'CLEN/USTN'
    return None


def _get_bene_pair(settlement):
    """
    Get the BENE (Beneficial Ownership) indicator pair for a
    settlement, if applicable.
    """
    indicator = _get_bene_indicator(settlement)
    if indicator is None:
        return None
    pair = acm.FPair()
    pair.First(acm.FSymbol('BENE'))
    pair.Second(acm.FSymbol(indicator))
    return pair


def _get_bene_indicator(settlement):
    """
    Get the indicator portion of the BENE indicator pair for the
    specified settlement.
    """
    settle_category = _get_trade_settle_category(settlement)
    if settle_category == 'SA_CUSTODIAN':
        trad_area = _get_trad_area(settlement)
        if trad_area in ['External Transfer', 'Internal Transfer', 'SARB Transfer']:
            # No Change of Beneficial Ownership.
            return 'NBEN'
        # Change of Beneficial Ownership.
        return 'YBEN'
    return None


def _get_trade_settle_category(settlement):
    """
    Get the trade settle category for the specified settlement.
    """
    return _get_single_settlement_value(settlement, 'Trade.SettleCategoryChlItem.Name')


def _get_trad_area(settlement):
    """
    Get the trad area for the specified settlement.
    """
    return _get_single_settlement_value(settlement, 'Trade.OptKey1.Name')


def _get_single_settlement_value(settlement, method_chain):
    """
    Get a value for a settlement and the specified method chain that
    is expected to be the same for all related settlements.

    In the case of a single settlement this should always succeed.
    In the case of a netted settlement, it is possible that multiple
    settlements have been netted that have different values for the
    same method chain.  If such a case is encountered, an exception
    will be raised.
    """
    unique_values = _get_unique_settlement_values(settlement, method_chain)
    if len(unique_values) == 1:
        return unique_values.pop()
    exception_message = "Expecting one value for settlement {settlement_oid} and property "
    exception_message += "'{method_chain}'.\n\nThe following values were found:\n"
    exception_message = exception_message.format(
        settlement_oid=settlement.Oid(),
        method_chain=method_chain
    )
    for unique_value in unique_values:
        exception_message += "\n- '{unique_value}'".format(
            unique_value=unique_value
        )
    raise ValueError(exception_message)


def _get_unique_settlement_values(settlement, method_chain):
    """
    Get a distinct set of values from a settlement or, in the case
    of a netted settlement, its children for the specified method
    chain.
    """
    unique_values = set()
    if settlement.Children():
        for child_settlement in settlement.Children():
            unique_values.update(_get_unique_settlement_values(child_settlement, method_chain))
    else:
        method_chain = acm.FMethodChain(acm.FSymbol(method_chain))
        unique_values.add(method_chain.Call([settlement]))
    return unique_values


def AMOUNT_AMOUNT(settlement):
    """
    field 19A in 541 and 543
    """
    amount = settlement.Trade().Premium()
    if settlement.Type() == SettlementType.END_SECURITY and settlement.Trade().Instrument().InsType() == 'Repo/Reverse':
        amount = settlement.Trade().EndCash()

    if settlement.Currency().Name() == 'GHS':
        trade = settlement.Trade()
        if trade:
            for p in trade.Payments():
                if p.Type() == 'Premium':
                    amount += p.Amount()
    return abs(round(amount, 2))


def DEAL_PRICE(settlement):
    """
    field 90B in 541 and 543
    """
    price = ''
    if settlement.Currency().Name() == 'GHS':
        calc = calc_space_tradesheet.CalculateValue(settlement.Trade(), 'cleanPrice')
        calc = round(calc, 4)
        price = 'DEAL//ACTU/GHS' + format_number_for_swift(calc)
    return price


def check_Q_option(party):
    """
    function used in field 95P/Q in 54x
    """
    if GetPartyQualifier(party) in ('SELL', 'BUYR'):
        settlement_oid = party['settlementid']
        settlement = acm.FSettlement[settlement_oid]
        if not settlement.CounterpartyAccountRef().NetworkAlias():
            return True
    return False


def GET_PARTY_DETAILS(settlement):
    """
    field 95P/Q in 54x
    """
    parties = GetPartyDetails(settlement)
    for p in parties:
        p['settlementid'] = settlement.Oid()
    return parties


def PARTY_OPTION(party):
    """
    field 95P/Q in 54x
    FAOps-42 For SSA
    if qualifier in ('SELL', 'BUYR') and not settlement.CounterpartyAccountRef().NetworkAlias() and no DSS:
        option Q
    elif qualifier in ('SELL', 'BUYR') and not settlement.CounterpartyAccountRef().NetworkAlias():
        option R
    """
    if check_Q_option(party):
        settlement_oid = party['settlementid']
        settlement = acm.FSettlement[settlement_oid]
        if not settlement.CounterpartyAccountRef().DataSourceScheme():
            return 'Q'
        else:
            return 'R'
    else:
        settlement_oid = party['settlementid']
        settlement = acm.FSettlement[settlement_oid]
        return GetPartyOption(party, settlement)


def PARTY_NAME(party):
    """
    field 95P/Q in 54x
    """
    if check_Q_option(party):
        settlement_oid = party['settlementid']
        settlement = acm.FSettlement[settlement_oid]
        counterparty = settlement.Counterparty()
        return counterparty.Name()
    else:
        return GetPartyFullName(party)


def get_valid_field70C_payment(party):
    """
    function used in field 70C in 54x
    """
    if GetPartyQualifier(party) in ('SELL', 'BUYR'):
        settlement_oid = party['settlementid']
        settlement = acm.FSettlement[settlement_oid]
        settlement_currency = settlement.Currency().Name()
        if settlement_currency == 'KES':
            trade = settlement.Trade()
            for p in trade.Payments():
                if p.Type() == 'Broker Fee':
                    return p


def GET_PARTY_NARRATIVE_NAME(party):
    """
    field 70C in 54x
    """
    field70C_name = ''
    payment = get_valid_field70C_payment(party)
    if payment:
        field70C_name = payment.Party().Name()
    return field70C_name


def GET_PARTY_NARRATIVE_AMOUNT(party):
    """
    field 70C in 54x
    """
    field70C_amount = ''
    payment = get_valid_field70C_payment(party)
    if payment:
        field70C_amount = abs(round(payment.Amount(), 2))
    return field70C_amount


def GET_PARTY_NARRATIVE_CURR(party):
    """
    field 70C in 54x
    """
    field70C_curr = ''
    payment = get_valid_field70C_payment(party)
    if payment:
        field70C_curr = payment.Currency().Name()
    return field70C_curr


def GET_PARTY_NARRATIVE_CONTACT(party):
    """
    field 70C in 54x
    """
    if GetPartyQualifier(party) in ('SELL', 'BUYR'):
        settlement_oid = party['settlementid']
        settlement = acm.FSettlement[settlement_oid]
        settle_category = _get_trade_settle_category(settlement)
        if settle_category == 'SA_CUSTODIAN':
            trad_area = _get_trad_area(settlement)
            if trad_area in ['External Transfer', 'Internal Transfer', 'SARB Transfer']:
                return 'PACO//CLNTTYPE/30'
    return ''


def GetPartySafekeepingOptionOverridden(party):
    """
    field 97A in 54x
    """
    settlement_oid = party['settlementid']
    settlement = acm.FSettlement[settlement_oid]
    if settlement.TheirCorrBank() in ('EUROCLEAR BANK', 'CLEARSTREAM BANKING'):
        return ''
    else:
        return GetPartySafekeepingOption(party, settlement)


def CAPITAL_EVENT_REFERENCE(settlement):
    """
    Capital Event Reference for field 21
    """
    capital_event_reference = settlement.AdditionalInfo().Call_Confirmation()
    if capital_event_reference:
        return capital_event_reference.replace(':910', '')
    raise ValueError('Could not populate Capital Event Reference, missing Call_Confirmation')


def GET_REC_CODE(settlement):
    """
    Gets rec code for settlement
    """
    return str(get_rec_code(settlement))


def MT298_SENDER_BIC(settlement):
    """
    Gets Sender Bic for MT298 message
    """
    absa_bic = AbsaXmlConfigSettings().GetValue(absa_swift_param, 'LogicalTerminalBic', True)

    return absa_bic


def MT298_RECEIVER_BIC(settlement):

    strate_bic = AbsaXmlConfigSettings().GetValue(strate_swift_param, 'LogicalTerminalBic', True)

    return strate_bic


def MESSAGE_USER_REFERENCE(settlement):

    user_ref_ext = AbsaXmlConfigSettings().GetValue(absa_swift_param, 'UserReferenceExt', True)

    if is_demat(settlement):
        return '108:'+str(int(time.time()*10))[-8:] + 'MS10' + user_ref_ext + '002'

    raise ValueError('Non Demat Settlements not yet supported for MT298 Automation')
