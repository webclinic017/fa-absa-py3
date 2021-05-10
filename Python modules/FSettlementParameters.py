"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FSettlementParameters.

DESCRIPTION
    This module contains parameters used to configure settlement functionality
    within Front Arena.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2011-05-28      662927          Heinrich Cronje        Miguel da Silva          SND implementation
2011-11-17      828039          Heinrich Cronje        Enhancement              Reading integration parameters from a config file.
2011-12-08      852496          Willie van der Bank    Miguel da Silva          Bringing online of new desks
2012-02-28      XXXXXX          Heinrich Cronje        Enhancement              Sybase Exodus. Determine the environment first to
                                                                                get the correct settings to use.
2012-08-08      396485          Heinrich Cronje        Ross Wood                PRIME SERVICES DESK Implementation
2013-10                         Willie van der Bank    2013 Upgrade             Added additional parameters
2015-03-31      ABITFA-3499     Lawrence Mucheka       Van Schalkwyk, Willie    Enable Settlements gen. for ABCAP CRT desk
2015-03-31      ABITFA-3731     Manan Ghosh            Nicolette Burger         Enable Settlements  for Africa Desk. Changes to
                ABITFA-3166                                                     Credit Derivatives, Metals and Abcap_CRT desk  rules
2015-03-31      ABITFA-3822     Manan Ghosh            Willie Van Schalwyk      Enable Settlements  for BAGL and Syndicate Trading Desk.
2015-11-02      ABITFA-3691     Lawrence Mucheka       Willie Van Schalwyk      Enable Settlements  for Collateral Desk.
2016-04-19      ABITFA-4174     Gabriel Marko          Linda Breytenbanch       Enable Settlements on Deposits for Primary Markets Desk.
2016-07-20      CHNG0003821295  Willie van der Bank                             Created a user split for the new OpsDoc ATS as per
                                                                                Sungard's suggestion to resolve the prod issue of
                                                                                settlements not Ack'ing after Ack has been received
2016-08-19      CHNG0003744247  Willie van der Bank                             MM Demat project go-live
2017-03-28      ABITFA-4481     Vojtech Sidorin                                 Register the SettlementModification hook.
2017-06-06      CHNG0004636076  Willie van der Bank                             Enable settlements for UHAMBO
2017-08-26      2017 Upgrade    Willie van der Bank                             Added preventAutomaticNetting parameter and removed
                                                                                LogTrace as part of 2017 upgrade
2017-12-07      CHNG0005212731  Willie vd Bank                                  Enable Settlements for NON ZAR IRD.
2017-12-11      CHNG0005220511  Willie van der Bank                             Added Settmnt_Prvnt_GRP_TREASURY
2018-04-10      CHG1000343600   Willie vd Bank                                  Set detailedLogging = False to improve EOD run time
2018-05-11      CHG1000406751   Willie van der Bank                             Added Settmnt_Prvnt_Trade_Status
2018-06-19      CHG1000570523   Willie vd Bank                                  Added internal settlements
2018-07-17      CHG1000676036   Willie vd Bank                                  Added Settmnt_Prvnt_ALCODESKISSUER
2018-11-23                      Cuen Edwards                                    Refactored out environment parameter lookup to
                                                                                EnvironmentFunctions and reformatted.
2019-02-15      CHG1001408723   Jaysen Naicker                                  Refactored trade filter queries into one query so
                                                                                loading is faster
2019-04-23      Upgrade         Jaysen Naicker                                  Add missing paramter defaultPartialSettlementType
22-03-2020      FAOPS-659       Joash Moodley           Kgomotso Gumbo          Generate MT202's for SSA MT54x securities Funding
2020-01-29      PCGDEV-231      Bhavnisha Sarawan                               Add missing paramter defaultPartialSettlementType
28-05-2020      FAOPS-683       Joash Moodley           Kgomotso Gumbo          EuroClear Custody Funding (MT210 & MT222(custom 202))
28-05-2020      FAOPS-740       Joash Moodley           Kgomotso Gumbo          EuroClear Custody Funding (MT200)

-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
import EnvironmentFunctions
from FOperationsHook import CustomHook
import FSettlementSwiftDefaultXML as SwiftDefaultXML
import FSettlementSwiftXMLHooks

ambAddress = '{amb_host}:{amb_port}{amb_login}'.format(
    amb_host=EnvironmentFunctions.get_settlement_parameter('Host'),
    amb_port=EnvironmentFunctions.get_settlement_parameter('Port'),
    amb_login=EnvironmentFunctions.get_settlement_parameter('Login')
)

receiverSource = EnvironmentFunctions.get_settlement_parameter('ReceiverSource')

if acm.UserName() == 'ATS_OPSDOC_STLM':
    receiverMBName = EnvironmentFunctions.get_settlement_parameter('ReceiverNameOPSDOC')
else:
    receiverMBName = EnvironmentFunctions.get_settlement_parameter('ReceiverName')

traceLevel = 0

alternativeCouponHandling = False

considerResetsForTRSDividends = False

detailedLogging = True

doCloseTradeNetting = False

forwardEarlyTermination = False

updateVoidedSettlement = True

maximumDaysForward = 10

maximumDaysBack = 7

hooks = [
    CustomHook('FSettlementHooks', 'SettlementModification'),
    CustomHook('FSettlementHooks', 'GetMTMessage'),
    CustomHook('FSettlementHooks', 'ExcludeTrade'),
    CustomHook('SettlementSplitHook', 'SplitSettlement')
]

tradeFilterQueries = [
    'SettlementEOD_filter'
]

preventSettlementCreationQueries = [
    'Settmnt_Prvnt_ForexDesk',
    'Settmnt_Prvnt_ZZZDONOTUSEIRPFXD',
    'Settmnt_Prvnt_SwapsDesk',
    'Settmnt_Prvnt_REPODesk',
    'Settmnt_Prvnt_NonLinearDerivDes',
    'Settmnt_Prvnt_NLDDesk',
    'Settmnt_Prvnt_LIQUIDASSETDesk',
    'Settmnt_Prvnt_FORWARDSDesk',
    'Settmnt_Prvnt_BONDSDesk',
    'Settmnt_Prvnt_Zero_Amounts',
    'Settmnt_Prvnt_EQDerivativesDesk',
    'Settmnt_Prvnt_MoneyMarketDesk',
    'Settmnt_Prvnt_FundingDesk',
    'Settmnt_Prvnt_IRDDesk',
    'Settmnt_Prvnt_CreditDerivDesk',
    'Settmnt_Prvnt_StructNotesDesk',
    'Settmnt_Prvnt_GoldDesk',
    'Settmnt_Prvnt_MetalsDesk',
    'Settmnt_Prvnt_Metal_Currencies',
    'Settmnt_Prvnt_PrimeServicesDesk',
    'Settmnt_Prvnt_CreditDerivDeskNo',
    'Settmnt_Prvnt_IrdDeskNoncsa',
    'Settmnt_Prvnt_ACQStructDerivDes',
    'Settmnt_Prvnt_TWC_SF',
    'Settmnt_Prvnt_TWC_DT',
    'Settmnt_Prvnt_TWC_FIT',
    'Settmnt_Prvnt_TWC_NON',
    'Settmnt_Prvnt_TWC_STCF',
    'Settmnt_Prvnt_ABCAP_CRT',
    'Settmnt_Prvnt_AfricaDesk',
    'Settmnt_Prvnt_BAGL',
    'Settmnt_Prvnt_Syndicate',
    'Settmnt_Prvnt_CollateralDesk',
    'Settmnt_Prvnt_PrimaryMarkets',
    'Settmnt_Prvnt_Demat',
    'Settmnt_Prvnt_Impume',
    'Settmnt_Prvnt_UHAMBO',
    'Settmnt_Prvnt_NON_ZAR_IRD',
    'Settmnt_Prvnt_GRP_TREASURY',
    'Settmnt_Prvnt_Trade_Status',
    'Settmnt_Prvnt_Internals',
    'Settmnt_Prvnt_ALCODESKISSUER',
    'Settmnt_Prvnt_LCH_Booking_fee',
    'Settmnt_Prvnt_AfricaDeskSecNom',
    'Settmnt_Prvnt_SECURITYLENDINGSDESK',
    'Settmnt_Prvnt_Euroclear',
]

preventSettlementDeletionQueries = [
    'Settlement_Terminated'
]

MTMessageToXMLMap = [
    ('ALL', SwiftDefaultXML.documentSettlementSWIFT),
    ('200', FSettlementSwiftXMLHooks.MT200_custom_template),
    ('210', FSettlementSwiftXMLHooks.MT210_custom_template),
    ('222', FSettlementSwiftXMLHooks.MT202_custom_template),
    ('298', FSettlementSwiftXMLHooks.MT298_custom_template)
]

confirmationEventHandling = False

correctTradePayNetQueries = []

setProtectionAndOwnerFromTrade = True

tradeAmendmentQueries = []

preventAutomaticNetting = ['Coupon', 'Redemption']

defaultPartialSettlementType = 'NPAR'

