""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsEnums.py"
"""
Module for defining enums as python classes. Do not import anything into this module.
If new values are added to existing enums or new enums are added make sure to update or
add new tests to test this in test_FOperationsEnums.py

"""

#-------------------------------------------------------------------------
class AccountType:
    CASH                            = 'Cash'

#-------------------------------------------------------------------------
class BarrierMonitoring:
    WINDOW                          = 'Window'
    DISCRETE                        = 'Discrete'

#-------------------------------------------------------------------------
class BarrierOptionType:
    DOWN_AND_OUT                    = 'Down & Out'
    DOWN_AND_IN                     = 'Down & In'
    UP_AND_OUT                      = 'Up & Out'
    UP_AND_IN                       = 'Up & In'
    DOUBLE_OUT                      = 'Double Out'
    DOUBLE_IN                       = 'Double In'

#-------------------------------------------------------------------------
class BusinessEventStatus:
    CONFIRMED                       = 'Confirmed'

#-------------------------------------------------------------------------
class BusinessEventType:
    CORRECT_TRADE                   = 'Correct Trade'

#-------------------------------------------------------------------------
class CashFlowType:
    FIXED_AMOUNT                    = 'Fixed Amount'
    FIXED_RATE                      = 'Fixed Rate'
    FLOAT_RATE                      = 'Float Rate'
    CAPLET                          = 'Caplet'
    FLOORLET                        = 'Floorlet'
    DIGITAL_CAPLET                  = 'Digital Caplet'
    DIGITAL_FLOORLET                = 'Digital Floorlet'
    TOTAL_RETURN                    = 'Total Return'
    CREDIT_DEFAULT                  = 'Credit Default'
    CALL_FIXED_RATE                 = 'Call Fixed Rate'
    CALL_FLOAT_RATE                 = 'Call Float Rate'
    REDEMPTION_AMOUNT               = 'Redemption Amount'
    ZERO_COUPON_FIXED               = 'Zero Coupon Fixed'
    RETURN                          = 'Return'
    DIVIDEND                        = 'Dividend'
    FIXED_ADJUSTABLE                = 'Fixed Rate Adjustable'
    INTEREST_REINVESTMENT           = 'Interest Reinvestment'
    CALL_FIXED_RATE_ADJUSTABLE      = 'Call Fixed Rate Adjustable'
    FIXED_RATE_ACCRETIVE            = 'Fixed Rate Accretive'
    POSITION_TOTAL_RETURN           = 'Position Total Return'
    FIXED_PRICE                     = 'Fixed Price'
    FLOAT_PRICE                     = 'Float Price'
    AGGREGATED_FIXED_AMOUNT         = 'Aggregated Fixed Amount'
    AGGREGATED_COUPON               = 'Aggregated Coupon'
    COLLARED_FLOAT                  = 'Collared Float'

#-------------------------------------------------------------------------
class ExerciseType:
    AMERICAN                        = 'American'
    EUROPEAN                        = 'European'

#-------------------------------------------------------------------------
class ExoticEventType:
    BARRIER_DATE                    = 'Barrier date'

#-------------------------------------------------------------------------
class InsType:
    STOCK                           = 'Stock'
    FUTURE_FORWARD                  = 'Future/Forward'
    OPTION                          = 'Option'
    BOND                            = 'Bond'
    FRN                             = 'FRN'
    PROMIS_LOAN                     = 'PromisLoan'
    ZERO                            = 'Zero'
    BILL                            = 'Bill'
    DEPOSIT                         = 'Deposit'
    SWAP                            = 'Swap'
    CURR_SWAP                       = 'CurrSwap'
    CAP                             = 'Cap'
    FLOOR                           = 'Floor'
    CURR                            = 'Curr'
    COMBINATION                     = 'Combination'
    COLLATERAL                      = 'Collateral'
    SECURITY_LOAN                   = 'SecurityLoan'
    REPO_REVERSE                    = 'Repo/Reverse'
    BUY_SELLBACK                    = 'BuySellback'
    INDEX_LINKED_BOND               = 'IndexLinkedBond'
    TOTAL_RETURN_SWAP               = 'TotalReturnSwap'
    DUAL_CURRENCY_BOND              = 'DualCurrBond'
    MBS_ABS                         = 'MBS/ABS'
    BASKET_REPO_REVERSE             = 'BasketRepo/Reverse'
    BASKET_SECURITY_LOAN            = 'BasketSecurityLoan'
    VARIANCE_SWAP                   = 'VarianceSwap'

#-------------------------------------------------------------------------
class LegType:
    FLOAT                           = 'Float'
    TOTAL_RETURN                    = 'Total Return'
    CREDIT_DEFAULT                  = 'Credit Default'
    CALL_FIXED                      = 'Call Fixed'
    CALL_FLOAT                      = 'Call Float'
    CALL_FIXED_ADJUSTABLE           = 'Call Fixed Adjustable'

#-------------------------------------------------------------------------
class OpenEndStatus:
    OPEN_END                        = 'Open End'
    TERMINATED                      = 'Terminated'

#-------------------------------------------------------------------------
class Operations:
    EDIT_SETTLEMENTS                = 'Edit Settlements'
    STANDALONE_SETTLEMENT           = 'Standalone Settlement'
    VOID_SETTLEMENT                 = 'Void Settlement'
    AUTHORISE_SETTLEMENT            = 'Authorise Settlement'
    RELEASE_SETTLEMENT              = 'Release Settlement'
    CLOSE_SETTLEMENT                = 'Close Settlement'
    AUTHORISE_LATE_SETTLEMENT       = 'Authorise Late Settlement'
    ACCEPT_SETTLEMENT_UPDATES       = 'Accept Settlement Updates'
    INSTRUCT_TO_CANCEL_SETTLEMENT   = 'Instruct To Cancel Settlement'
    INSTRUCTED_TO_CANCEL_SETTLEMENT = 'Instructed To Cancel Settlement'
    COMPENSATION_CLAIM              = 'Compensation Claim'
    COMPENSATION_PAYMENT            = 'Compensation Payment'
    FUND_TRANSFER                   = 'Fund Transfer'
    MANUALLY_ADJUST_SETTLEMENT      = 'Manually Adjust Settlement'
    PAY_GOOD_VALUE                  = 'Pay Good Value'
    PAY_FAIR_VALUE                  = 'Pay Fair Value'
    REVERT_TO_UNADJUSTED_PAYMENT    = 'Revert to Unadjusted Payment'
    SPLIT_PAYMENT                   = 'Split Payment'
    UNSPLIT_PAYMENT                 = 'Un-Split Payment'
    NET_PAYMENTS                    = 'Net Payments'
    UNNET_SETTLEMENT                = 'Un-Net Payments'
    RESUBMIT_PAYMENT                = 'Resubmit Payment'
    SUPPRESS_PAYMENTS_MESSAGE       = 'Suppress Payments Message'
    REGENERATE_SETTLEMENT           = 'Regenerate Settlement'
    RESUBMIT_NAK                    = 'Resubmit NAK'
    REGENERATE_PAYMENTS_FOR_TRADE   = 'Regenerate Payments For Trade'
    SUPPRESS_PAYMENT_MESSAGE_ACK    = 'Suppress Payment Message Ack'
    INSTRUCT_TO_CORRECT_SETTLEMENT  = 'Instruct To Correct Settlement'    
    SET_PARTIAL_SETTLEMENT          = 'Set Partial Settlement'
    PARTIAL_SETTLEMENT              = 'Partial Settlement'
    UNDO_PARTIAL_SETTLEMENT         = 'Undo Partial Settlement'
    PAIR_OFF_SETTLEMENTS            = 'Pair Off Settlements'
    UNDO_PAIR_OFF_SETTLEMENTS       = 'Undo Pair Off Settlements'
    ADJUST_VALUE_DAY                = 'Adjust Value Day'

    SPLIT_JOURNAL                   = 'Split Journal'
    ADJUST_JOURNAL                  = 'Adjust Journal'
    ADJUST_DR_CR_PAIR               = 'Adjust Journal DR CR Pair'
    CREATE_STANDALONE_JOURNALS      = 'Create Standalone Journal'
    EDIT_SIMULATED_JOURNALS         = 'Edit Simulated Journal'

    RELEASE_CONFIRMATION            = 'Release Confirmation'
    MATCH_CONFIRMATION              = 'Match Confirmation'
    REGENERATE_CONFIRMATION         = 'Regenerate Confirmation'
    RESEND_CONFIRMATION             = 'Resend Confirmation'
    HOLD_CONFIRMATION               = 'Hold Confirmation'
    SEND_CHASER                     = 'Send Confirmation Chaser'
    MODIFY_CHASER                   = 'Modify Chaser'
    AUTHORISE_MANUAL_MATCH          = 'Authorise Manual Match'

#-------------------------------------------------------------------------
class QuotationType:
    PER_UNIT                        = 'Per Unit'

#-------------------------------------------------------------------------
class SettleType:
    PHYSICAL_DELIVERY               = 'Physical Delivery'
    CASH                            = 'Cash'

#-------------------------------------------------------------------------
class SignOffStatus:
    PENDING_APPROVAL                = 'Pending Approval'

#-------------------------------------------------------------------------
class TradeStatus:
    SIMULATED                       = 'Simulated'
    FO_CONFIRMED                    = 'FO Confirmed'
    BO_CONFIRMED                    = 'BO Confirmed'
    BO_BO_CONFIRMED                 = 'BO-BO Confirmed'
    VOID                            = 'Void'
    TERMINATED                      = 'Terminated'
    CONFIRMED_VOID                  = 'Confirmed Void'

#-------------------------------------------------------------------------
class TradeType:
    NORMAL                          = 'Normal'
    EXCERCISE                       = 'Exercise'
    CLOSING                         = 'Closing'
    CASH_POSTING                    = 'Cash Posting'

#-------------------------------------------------------------------------
class PartyType:
    NONE                            = 'None'
    COUNTERPARTY                    = 'Counterparty'
    CLIENT                          = 'Client'
    INTERN_DEPT                     = 'Intern Dept'
    BROKER                          = 'Broker'
    MARKET                          = 'Market'
    MTM_MARKET                      = 'MtM Market'
    ISSUER                          = 'Issuer'
    DEPOT                           = 'Depot'
    CLEARING_HOUSE                  = 'Clearing House'
    MIDDLEWARE                      = 'Middleware'
    REPOSITORY                      = 'Repository'
