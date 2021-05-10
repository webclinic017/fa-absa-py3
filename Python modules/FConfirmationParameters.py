"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FConfirmationParameters.

DESCRIPTION
    This module contains parameters used to configure confirmation functionality
    within Front Arena.

NOTES:
    All ConfirmationEventDefinition with upper case are custom made the rest are
    all core functions from Sungard.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2012-01-12      873236          Tshepo Mabena           IT                      Reading integration parameters from a
                                                                                config file in an environment which is
                                                                                currently being run.
2012-01-19      882466          Heinrich Cronje         Miguel Da Silva         Added Conf_Is_New_Trade_Event as the
                                                                                New Trade Confirmation event function.
2012-02-28      XXXXXX          Heinrich Cronje         IT                      Sybase Exodus. Determine the environment first to
                                                                                get the correct settings to use.
2012-05-23      C209780         Heinrich Cronje         IT                      Added prevention queries.
2012-07-20      C335236         Willie van der Bank     Ops                     Added exclusion queries.
2013-10         XXXXXXX         Willie van der Bank     2013 Upgrade            Added additional parameters
2014-05-19      XXXXXXX         Sanele Macanda          Adaptiv Requirements    Added:Confirmmation Events
                                                                                CONF_NEW_TRADE_EVENT,
                                                                                CONF_NEW_TRADE_EVENT_CALL,
                                                                                CONF_ISPLEDGE_FROZEN,
                                                                                IsAdjustDepositEvent (Core Functionality)
                                                                                IsRateFixingEvent    (Core Functionality)
                                                                                CONF_ISNOVATED
                                                                                CONF_NOTICE_TO_DISREGARD
                                                                                CONF_MATURITY_NOTICE
2016-03-22      Abitfa 4170     Willie van der Bank     Elaine Visagie          Auto Match query folder added. Confos which
                                                                                are not Matched run the risk of being resend
                                                                                if there are any changes to the underlying objects.
2016-07-20      CHNG0003821295  Willie van der Bank                             Updated IsAdjustDepositEvent to take cash flow pay date
                                                                                into consideration as well
2016-08-19      CHNG0003744247  Manan Ghosh                                     Added:Confirmmation Events
                                                                                MATCH_DEMAT_TRADE,
                                                                                IsPreSettlementEvent,
                                                                                IsPreSettleApprovalEvent,
                                                                                IsSettlementEvent
                                                                                into consideration as well
2016-11-03      ABITFA-4285     Evgeniya Baskaeva       Elaine Visagie          Trade Loans acquirers to be included
                                                                                within the automated MM Adaptive confirmations
2017-02-11      CHNG0004099366  Willie van der Bank                             Added COLLATERAL DESK for depos
                                                                                Removed Conf_Prvnt_FundingDesk_ADHOC because it is
                                                                                obsolete with the addition of Amba filtering
2017-08-26                      Willie van der Bank                             Removed ConfirmationCoustomXMLTemplates import and
                                                                                LogTrace as part of 2017 upgrade
2017-12-11      CHNG0005220511  Willie van der Bank                             Added Conf_Prvnt_BAGL, Conf_Prvnt_GRP_TREAUSRY and
                                                                                Conf_Prvnt_DIS
2018-05-15      FAOPS-127       Cuen Edwards            Elaine Visagie          Addition of Term Statement functionality.
2018-06-05      FAOPS-97        Adelaide Davhana        Kgomotso Gumbo          Added Loan Rate Notice functionality.
2018-08-14      FAOPS-167       Cuen Edwards            Elaine Visagie          Addition of Call Statement functionality.
2018-08-28      FAOPS-61        Stuart Wilson           Capital Markets         Addition of Broker Note functionality.
2018-11-19      FAOPS-288       Stuart Wilson           Loan Ops                Addition of multiTradeEventNames.
2018-10-25      FAOPS-226       Cuen Edwards            Letitia Carboni         Addition of Trade Affirmation functionality.
2018-11-23                      Cuen Edwards                                    Refactored out environment parameter lookup to
                                                                                EnvironmentFunctions and reformatted.
2018-08-21      FAOPS-168       Tawanda Mukhalela       Vusi Phungula           Addition of IRS Reset Advices functionality
2018-11-22      FAOPS-160       Stuart Wilson           Loan Ops                Addition of repayment notice functionality
2019-03-27                      Tawanda Mukhalela                               Refactored Reset Advice Hooks to take reset subtype
2019-04-12      FAOPS-483       Cuen Edwards            Kgomotso Gumbo          Disabled confirmation auto-matching by FConfirmationEOD
                                                                                as this function is already performed intra-day by the
                                                                                Operations STP ATS.
2019-04-30      FAOPS-461       Cuen Edwards            Letitia Carboni         Changes for Swap Trade Affirmations.
2019-05-06      Upgrade2018     Jaysen Naicker                                  Remove reference to ConfirmationEventDefinition
2019-09-05      FAOPS-530       Joash Moodley           Kgomotso Gumbo          Add Loan Ops Commitment Fee
2019-06-14      FAOPS-439       Cuen Edwards            Letitia Carboni         Addition of Trade Confirmation functionality.
                                Tawanda Mukhalela
2020-02-10      FAOPS-725       Cuen Edwards            Kgomotso Gumbo          Some minor refactoring of Broker Notes.
2020-02-20      FAOPS-708       Tawanda Mukhalela       Mashishimise Ndivhuho	Addition of 10B10 Confirmations.
2020-03-10      FAOPS-763       Cuen Edwards            Kgomotso Gumbo          Addition of creation prevention query
                                                                                for PRIME SERVICES DESK.
2020-04-20      FAOPS-708       Tawanda Mukhalela       Mashishimise Ndivhuho	Changed event name from 10B10 New Trade
                                                                                Confirmation to 10B10 Confirmation
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import Adaptiv_XML_Templates
import BrokerNoteConfirmationXML
import CallStatementConfirmationXML
import EnvironmentFunctions
from FConfirmationCancellationXMLHook import ConfirmationCancellationXMLHook as CancellationXMLHook
import FConfirmationDefaultXMLTemplates as defaultXMLTemplates
from FConfirmationEventHook import ConfirmationEventHook as EventHook
import FConfirmationSwiftDefaultXML as SwiftDefaultXML
import FCustomMT564
import FCustomMT598
from FOperationsHook import CustomHook
import LoanNoticeConfirmationXML
import LoanRepaymentNoticeXML
import LoanBalanceStatementXML
import ResetAdviceXML
import TermStatementConfirmationXML
import TradeAffirmationConfirmationXML
import LoanOpsCommitmentFeeXML
import TradeConfirmationXML
import ASUSNewTradeConfirmationXML


ambAddress = '{amb_host}:{amb_port}{amb_login}'.format(
    amb_host=EnvironmentFunctions.get_confirmation_parameter('Host'),
    amb_port=EnvironmentFunctions.get_confirmation_parameter('Port'),
    amb_login=EnvironmentFunctions.get_confirmation_parameter('Login')
)

receiverMBName = EnvironmentFunctions.get_confirmation_parameter('ReceiverName')

receiverSource = EnvironmentFunctions.get_confirmation_parameter('ReceiverSource')

confirmationEvents = [
    ("Close", EventHook("FConfirmationDefaultEventHooks", 'IsCloseEvent')),
    ("New Trade Call", EventHook("FConfirmationHooks", 'CONF_NEW_TRADE_EVENT_CALL')),
    ("New Trade", EventHook('FConfirmationHooks', 'CONF_NEW_TRADE_EVENT')),
    ("Partial Close", EventHook("FConfirmationHooks", 'IsPartialCloseEvent')),
    ("Account Ceded", EventHook("FConfirmationHooks", 'CONF_ISPLEDGE_FROZEN')),
    ("Adjust Deposit", "Conf_Valid_Adjustment", "Cash Flow", EventHook("FConfirmationHooks", 'IsAdjustDepositEvent')),
    ("Rate Fixing Call", "Conf_Valid_Trade", "Reset", EventHook("FConfirmationHooks", 'CONF_CALL_RATE_FIXING')),
    ("Novation", EventHook("FConfirmationHooks", 'CONF_ISNOVATED')),
    ("Maturity Notice", EventHook("FConfirmationHooks", 'CONF_MATURITY_NOTICE')),
    ("Prolong Deposit", EventHook("FConfirmationHooks", 'CONF_PROLONG_DEPOSIT')),
    ("Demat Match Request", EventHook("StrateHooks", 'MATCH_DEMAT_TRADE')),
    ("Demat PreSettle Conf", "Conf_Valid_Demat_Pre_Settle", "Cash Flow", EventHook("StrateHooks", 'IsPreSettlementEvent')),
    ("Term Statement", EventHook("TermStatementConfirmationEventHooks", 'CONF_TERM_STATEMENT')),
    ("Rate Notice", EventHook("LoanNoticeConfirmationEventHooks", 'CONF_RATE_NOTICE')),
    ("Call Statement", EventHook("CallStatementConfirmationEventHooks", 'CONF_CALL_STATEMENT')),
    ("Broker Note", EventHook("BrokerNoteConfirmationEventHooks", 'CONF_BROKER_NOTE')),
    ("Trade Affirmation", EventHook("TradeAffirmationConfirmationEventHooks", 'CONF_TRADE_AFFIRMATION')),
    ("Reset Advice", EventHook("ResetAdviceEventHooks", 'RESET_ADVICE_TRADES'), "Reset", EventHook("ResetAdviceEventHooks", 'RESET_ADVICE_HOOK')),
    ("Reset Confirmation", EventHook("ResetConfirmationEventHooks", 'VALID_TRADE'), "Reset", EventHook("ResetConfirmationEventHooks", 'PRIME_FIXING_HOOK')),
    ("Repayment Notice", EventHook("LoanRepaymentNoticeEventHooks", 'LOAN_REPAYMENT_NOTICE_EVENT')),
    ("Loan Balance Statement", EventHook("LoanBalanceStatementEventHooks", 'LOAN_BALANCE_STATEMENT_EVENT')),
    ("Loan Ops Commitment Fee", EventHook("LoanOpsCommitmentFeeXMLHooks", 'COMMITMENT_FEE')),
    ("Loan Ops Commitment Fee Future Date", EventHook("LoanOpsCommitmentFeeXMLHooks", 'COMMITMENT_FEE')),
    ("Loan Ops Commitment Fee Amendment", EventHook("LoanOpsCommitmentFeeXMLHooks", 'COMMITMENT_FEE_AMENDMENT')),
    ("Loan Balance Statement", EventHook("LoanBalanceStatementEventHooks", 'LOAN_BALANCE_STATEMENT_EVENT')),
    ("Trade Confirmation", EventHook("TradeConfirmationEventHooks", 'CONF_TRADE_CONFIRMATION')),
    ("10B10 Confirmation", EventHook("ASUSNewTradeConfirmationEventHooks", 'ASUS_NEW_TRADE_EVENT'))
]

eventToConfirmationOwnerTradeStrategyMap = [
    ('Trade Confirmation', 'Trx Trade Or Event Trade'),
    ('10B10 Confirmation', 'Trx Trade Or Event Trade')
]

templateToXMLMap = [
    ('SWIFT', SwiftDefaultXML.documentConfirmationSWIFT),
    ('ABSA_Deposit_Main', Adaptiv_XML_Templates.xml_Deposit_template),
    ('ABSA_Deposit_Adjust_Main', Adaptiv_XML_Templates.xml_Deposit_Adjust_template),
    ('ABSA_Call_Deposit_Opening_Main', Adaptiv_XML_Templates.xml_Call_Deposit_Opening_template),
    ('ABSA_Deposit_Cede_Main', Adaptiv_XML_Templates.xml_Deposit_Cede_template),
    ('ABSA_Rate_Fixing_Main', Adaptiv_XML_Templates.xml_Rate_Fixing_Main_template),
    ('ABSA_Deposit_Close', Adaptiv_XML_Templates.xml_Deposit_Close_template),
    ('ABSA_Maturity_Notice', Adaptiv_XML_Templates.xml_Maturity_Notice_template),
    ('ABSA_FI_Generic_Main', Adaptiv_XML_Templates.xml_FI_Generic_template),
    ('ABSA_Term_Statement', TermStatementConfirmationXML.xml_template),
    ('ABSA_RateNotice_Loan', LoanNoticeConfirmationXML.xml_template),
    ('ABSA_Call_Statement', CallStatementConfirmationXML.xml_template),
    ('ABSA_Broker_Note', BrokerNoteConfirmationXML.xml_template),
    ('ABSA_Trade_Affirmation', TradeAffirmationConfirmationXML.xml_template),
    ('ABSA_IRS_Presettlement', ResetAdviceXML.xml_template),
    ('ABSA_RepaymentNotice_Loan', LoanRepaymentNoticeXML.xml_template),
    ('ABSA_BalanceStatement_Loan', LoanBalanceStatementXML.xml_template),
    ('ABSA_Commitment_Fee_Invoice', LoanOpsCommitmentFeeXML.xml_template),
    ('ABSA_Trade_Confirmation', TradeConfirmationXML.xml_template),
    ('ABSA_10B10_New_Trade_Confirmation', ASUSNewTradeConfirmationXML.xml_template)
]

templateSWIFTEventToXMLMap = []

defaultXMLTemplate = defaultXMLTemplates.document

eventToFreeFormCancellationXMLHookMap = [
    ('Trade Affirmation', CancellationXMLHook('TradeAffirmationConfirmationXMLHooks',
                                              'get_cancellation_confirmation_xml')),
    ('Trade Confirmation', CancellationXMLHook('TradeConfirmationXMLHooks',
                                               'get_cancellation_confirmation_xml')),
    ('10B10 Confirmation', CancellationXMLHook('ASUSNewTradeConfirmationXMLHooks',
                                               'get_cancellation_confirmation_xml'))
]

traceLevel = 5

detailedLogging = True

tradeFilterQueries = [
    'Conf_Valid_Trade',
    'Conf_Valid_InsType',
    'Conf_Valid_Acquirer'
]

preventConfirmationCreationQueries = [
    'Conf_Prvnt_New_Trade_Creation',
    'Conf_Prvnt_MoneyMarketDesk',
    'Conf_Prvnt_FundingDesk',
    'Conf_Prvnt_NLDDesk',
    'Conf_Prvnt_AfricaDesk',
    'Conf_Prvnt_Old_Confos',
    'Conf_Prvnt_OptionBank',
    'Conf_Prvnt_Impume',
    'Conf_Prvnt_AcqStructDerivDesk',
    'Conf_Prvnt_Demat',
    'Conf_Prvnt_DIS',
    'Conf_Prvnt_TWC_SF',
    'Conf_Prvnt_TWC_DT',
    'Conf_Prvnt_TWC_FIT',
    'Conf_Prvnt_TWC_NON',
    'Conf_Prvnt_TWC_STCF',
    'Conf_Prvnt_CollDesk',
    'Conf_Prvnt_BAGL',
    'Conf_Prvnt_GRP_TREASURY',
    'Conf_Prvnt_Primary_Markets',
    'Conf_Prvnt_PrimeServicesDesk',
    'Conf_Prvnt_FICC_ZAG_Broker_Note',
    'Conf_Prvnt_Access_Deposit_Notes',
    'Conf_Prvnt_SND_Deposits',
    'Conf_Prvnt_Confirmation_Creation'
]

preventConfirmationCancellationQueries = [
    'Conf_Prvnt_Cancellation',
    'Conf_Prvnt_Statement_Cancellation',
    'Conf_Prvnt_Loan_Notice_Cancellation',
    'Conf_Prvnt_Affirmation_Cancellation',
    'Conf_Prvnt_PreSettlement_Cancellation',
    'Conf_Prvnt_Cancellation_Amendment_Repayment_Notice',
    'Conf_Prvnt_Broker_Note_Cancellation',
    'Conf_Prvnt_Confirmation_Cancellation'
]

preventConfirmationAmendmentQueries = [
    'Conf_Prvnt_Amendment',
    'Conf_Prvnt_Statement_Amendment',
    'Conf_Prvnt_PreSettlement_Amendment',
    'Conf_Prvnt_Cancellation_Amendment_Repayment_Notice'
]

defaultChaserCutoffMethodBusinessDays = False

cancelPreReleasedConfirmations = False

defaultDays = 10

cancellationAndNewInsteadOfAmendmentSWIFT = False

cancellationAndNewInsteadOfAmendmentFreeForm = False

changeConfirmationStatusToMatchedQuery = None

setProtectionAndOwnerFromTrade = False

hooks = [
    CustomHook('FCustomSWIFT', 'GetMTMessage')
]

MTMessageToXMLMap = [
    ('ALL', SwiftDefaultXML.documentConfirmationSWIFT),
    ('598', FCustomMT598.MT598_template),
    ('564', FCustomMT564.MT564_template)
]
