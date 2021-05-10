""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingEnums.py"

#-------------------------------------------------------------------------
class AccountingInstructionType:
    NONE                                = 'None'
    MONEY_FLOW                          = 'Money Flow'
    LEG                                 = 'Leg'
    TRADE                               = 'Trade'
    COMBINATION                         = 'Combination'
    SETTLEMENT                          = 'Settlement'

#-------------------------------------------------------------------------
class AccountingPeriodRule:
    NONE                                 = 'None'
    REJECT                               = 'Reject'
    BOUNDARY                             = 'Boundary'
    CURR_PERIOD                          = 'Curr Period'
    IGNORE                               = 'Ignore'

#-------------------------------------------------------------------------
class AccountingPeriodStatus:
    CLOSED                              = 'Closed'
    OPEN                                = 'Open'

#-------------------------------------------------------------------------
class AccountingPeriodType:
    START_OF_FISCAL_YEAR                = 'Start of Fiscal Year'
    END_OF_FISCAL_YEAR                  = 'End of Fiscal Year'

#-------------------------------------------------------------------------
class BusinessDayMethod:
    NONE                                = 'None'
    FOLLOWING                           = 'Following'
    PRECEDING                           = 'Preceding'
    MODIFIED_FOLLOWING                  = 'Mod. Following'
    MODIFIED_PRECEDING                  = 'Mod. Preceding'

#-------------------------------------------------------------------------
class DebitOrCredit:
    DEBIT                               = 'Debit'
    CREDIT                              = 'Credit'

#-------------------------------------------------------------------------
class JournalAggregationLevel:
    TRADE                               = 'Trade'
    CONTRACT_TRADE_NUMBER               = 'Contract Trade Number'
    INSTRUMENT_AND_PORTFOLIO            = 'Instrument and Portfolio'
    MONEYFLOW                           = 'Moneyflow'
    CONTRACT_TRADE_NUMBER_AND_MONEYFLOW = 'Contract Trdnbr and Moneyflow'
    TAX_LOT_CLOSING                     = 'Tax Lot Closing'

#-------------------------------------------------------------------------
class JournalCategory:
    STANDARD                            = 'Standard'
    BALANCE                             = 'Balance'
    FX_REVALUATION                      = 'FX Revaluation'
    END_OF_FISCAL_YEAR                  = 'End of Fiscal Year'

#-------------------------------------------------------------------------
class JournalTriggerType:
    REAL_TIME                           = 'Real Time'
    END_OF_DAY                          = 'End of Day'

#-------------------------------------------------------------------------
class JournalType:
    REVERSAL                            = 'Reversal'
    REVERSED                            = 'Reversed'
    PERIODIC_REVERSAL                   = 'Periodic Reversal'
    PERIODIC_REVERSED                   = 'Periodic Reversed'
    LIVE                                = 'Live'
    REALLOCATION_REVERSED               = 'Reallocation Reversed'
    REALLOCATION_REVERSAL               = 'Reallocation Reversal'
    SIMULATED                           = 'Simulated'

#-------------------------------------------------------------------------
class ReallocationStatus:
    NONE                                = 'None'
    REALLOCATED                         = 'Reallocated'
    TO_BE_REALLOCATED                   = 'To be reallocated'

#-------------------------------------------------------------------------
class ReportingClass:
    SUMMARY                             = 'Summary'
    TACCOUNT                            = 'TAccount'

#-------------------------------------------------------------------------
class ReversalExclusion:
    NONE                                = 'None'
    LAST_DAY_OF_MONTH                   = 'Last day of month'
    LAST_DAY_OF_YEAR                    = 'Last day of year'
    ALWAYS                              = 'Always'

#-------------------------------------------------------------------------
class ReversalFrequency:
    NONE                                = 'None'
    DAILY                               = 'Daily'
    WEEKLY                              = 'Weekly'
    MONTHLY                             = 'Monthly'
    YEARLY                              = 'Yearly'

#-------------------------------------------------------------------------
class ReversalType:
    PERIODIC_REVERSAL                   = 0
    NON_PERIODIC_REVERSAL               = 1
    REALLOCATION_REVERSAL               = 2

#-------------------------------------------------------------------------
class ReversalMethod:
    NONE                                = 'None'
    INCREMENTAL                         = 'Incremental'
    REVERSE_AND_REPLACE                 = 'Reverse and Replace'
    DEFAULT                             = 'Default'
