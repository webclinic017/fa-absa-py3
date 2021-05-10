""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementEnums.py"
'''
Module for defining enums as python classes. Do not import anything into this module.
If new values are added to existing enums or new enums are added make sure to update or
add new tests to test this in test_FSettlementEnums.py
'''

class SettlementStatus:
    NONE                  = 'None'
    NEW                   = 'New'
    EXCEPTION             = 'Exception'
    MANUAL_MATCH          = 'Manual Match'
    HOLD                  = 'Hold'
    VOID                  = 'Void'
    AUTHORISED            = 'Authorised'
    RELEASED              = 'Released'
    ACKNOWLEDGED          = 'Acknowledged'
    NOT_ACKNOWLEDGED      = 'Not Acknowledged'
    PENDING_CLOSURE       = 'Pending Closure'
    CLOSED                = 'Closed'
    NON_RECEIPT           = 'Non Receipt'
    INCORRECT_RECEIPT     = 'Incorrect Receipt'
    UNEXPECTED_CREDIT     = 'Unexpected Credit'
    NON_PAYMENT           = 'Non Payment'
    INCORRECT_PAYMENT     = 'Incorrect Payment'
    UNEXPECTED_DEBIT      = 'Unexpected Debit'
    UPDATED               = 'Updated'
    RECALLED              = 'Recalled'
    AWAITING_CONFIRMATION = 'Awaiting Confirmation'
    PENDING_CANCELLATION  = 'Pending Cancellation'
    PENDING_AMENDMENT     = 'Pending Amendment'
    CANCELLED             = 'Cancelled'
    SETTLED               = 'Settled'
    REPLACED              = 'Replaced'
    AWAITING_CANCELLATION = 'Awaiting Cancellation'
    PAIRED_OFF            = 'Paired Off'

class StatusExplanation:
    NONE                                   = 0
    MESSAGE_VALIDATION_FAILED              = 1
    SWIFT_NAK                              = 2
    CANCELLED_BY_US                        = 3
    CANCELLED_BY_THE_COUNTERPARTY          = 4
    MISSING_SETTLEMENT_INSTRUCTIONS        = 5
    HISTORIC_VALUE_DATE                    = 6
    MISSING_DATA                           = 7
    UNDETERMINED_AMOUNT                    = 8
    CHANGE_TO_SOURCE_DATA                  = 9
    RECALLED_DATA                          = 10
    LATE_PAYMENT_MANUALLY_AUTHORISED       = 11
    CURRENCY_DIFFERS_FROM_ACCOUNT_CURRENCY = 12
    INSUFFICIENT_MESSAGE_DATA              = 13
    MISSING_CONFIRMATION_INSTRUCTION       = 14
    MISSING_ADDRESS                        = 15
    DOCUMENT_GENERATION_INTERFACE_FAILURE  = 16
    DOCUMENT_GENERATION_FAILED             = 17
    DOCUMENT_GENERATION_SYSTEM_ERROR       = 18
    CHANGE_TO_INTERMEDIARY_DATA            = 19
    ACCOUNT_PARTY_UPDATE                   = 20
    TRADE_INSTRUMENT_UPDATE                = 21
    SHORT_POSITION                         = 22
    VALUE_DAY_CHECK_IGNORED                = 23
    AMENDMENT_PROCESS                      = 24

class RelationType:
    NONE                    = 'None'
    NET                     = 'Net'
    AD_HOC_NET              = 'Ad Hoc Net'
    CLOSE_TRADE_NET         = 'Close Trade Net'
    COUPON_NET              = 'Coupon Net'
    REDEMPTION_NET          = 'Redemption Net'
    DIVIDEND_NET            = 'Dividend Net'
    GOOD_VALUE              = 'Good Value'
    FAIR_VALUE              = 'Fair Value'
    COMPENSATION_PAYMENT    = 'Compensation Payment'
    COMPENSATION_CLAIM      = 'Compensation Claim'
    FUNDS_TRANSFER          = 'Funds Transfer'
    ADJUSTED                = 'Adjusted'
    UPDATED                 = 'Updated'
    SPLIT                   = 'Split'
    CANCELLATION            = 'Cancellation'
    SECURITIES_DVP_NET      = 'Securities DvP Net'
    CANCEL_CORRECT          = 'Cancel Correct'
    VALUE_DAY_ADJUSTED      = 'Value Day Adjusted'
    STORED_FOR_ACCOUNTING   = 'Stored for Accounting'

class SettlementDeliveryType:
    NONE                            = 'None'
    DELIVERY_VERSUS_PAYMENT         = 'Delivery versus Payment'
    DELIVERY_FREE_OF_PAYMENT        = 'Delivery Free of Payment'

class NettingRuleType:
    NONE                            = 'None'
    NET                             = 'Net'
    CLOSE_TRADE_NET                 = 'Close Trade Net'
    SECURITIES_DVP_NET              = 'Securities DvP Net'

class PartialSettlementType:
    NONE                            = 'None'
    NPAR                            = 'NPAR'
    PART                            = 'PART'
    PARC                            = 'PARC'
    PARQ                            = 'PARQ'

class SettlementType:
    NONE                            = 'None'
    PREMIUM                         = 'Premium'
    DIVIDEND                        = 'Dividend'
    PAYMENT_PREMIUM                 = 'Payment Premium'
    ASSIGNEMENT_FEE                 = 'Assignment Fee'
    PAYMENT_CASH                    = 'Payment Cash'
    FIXED_AMOUNT                    = 'Fixed Amount'
    FIXED_RATE                      = 'Fixed Rate'
    FLOAT_RATE                      = 'Float Rate'
    CAPLET                          = 'Caplet'
    FLOORLET                        = 'Floorlet'
    DIGITAL_CAPLET                  = 'Digital Caplet'
    DIGITAL_FLOORLET                = 'Digital Floorlet'
    CALL_FIXED_RATE                 = 'Call Fixed Rate'
    CALL_FLOAT_RATE                 = 'Call Float Rate'
    REDEMPTION_AMOUNT               = 'Redemption Amount'
    SECURITY_NOMINAL                = 'Security Nominal'
    STAND_ALONE_PAYMENT             = 'Stand Alone Payment'
    FEE                             = 'Fee'
    END_CASH                        = 'End Cash'
    PREMIUM_2                       = 'Premium 2'
    COUPON                          = 'Coupon'
    COUPON_TRANSFER                 = 'Coupon transfer'
    END_SECURITY                    = 'End Security'
    AGGREGATE_SECURITY              = 'Aggregate Security'
    FIXED_RATE_ADJUSTABLE           = 'Fixed Rate Adjustable'
    CASHFLOW_DIVIDEND               = 'Cashflow Dividend'
    REDEMPTION                      = 'Redemption'
    PAYOUT                          = 'Payout'
    DIVIDEND_TRANSFER               = 'Dividend Transfer'
    CALL_FIXED_RATE_ADJUSTABLE      = 'Call Fixed Rate Adjustable'
    INTEREST_REINVEST               = 'Interest Reinvestment'
    COMMISSION                      = 'Commission'
    INTEREST_ACCRUED                = 'Interest Accrued'
    FIXED_RATE_ACCRETIVE            = 'Fixed Rate Accretive'
    RECOVERY                        = 'Recovery'
    FIXED_AMOUNT_TRANSFER           = 'Fixed Amount Transfer'
    RECOVERY_REBATE                 = 'Recovery Rebate'
    ACCOUNT_TRANSFER                = 'Account Transfer'
    SECURITY_DVP                    = 'Security DvP'
    PAIR_OFF_PAYMENT                = 'Pair Off Payment'
    CAPLET_TRANSFER                 = 'Caplet transfer'
    FLOORLET_TRANSFER               = 'Floorlet transfer'
    REDEMPTION_SECURITY             = 'Redemption Security'