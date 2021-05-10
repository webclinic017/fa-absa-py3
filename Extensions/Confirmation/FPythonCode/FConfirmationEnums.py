""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationEnums.py"
"""
Module for defining enums as python classes. Do not import anything into this module.
If new values are added to existing enums or new enums are added make sure to update or
add new tests to test this in test_FConfirmationEnums.py
"""

#-------------------------------------------------------------------------
class ConfirmationStatus:
    NONE                            = 'None'
    NEW                             = 'New'
    AUTHORISED                      = 'Authorised'
    EXCEPTION                       = 'Exception'
    MANUAL_MATCH                    = 'Manual Match'
    PENDING_DOCUMENT_GENERATION     = 'Pending Document Generation'
    PENDING_APPROVAL                = 'Pending Approval'
    RELEASED                        = 'Released'
    ACKNOWLEDGED                    = 'Acknowledged'
    NOT_ACKNOWLEDGED                = 'Not Acknowledged'
    HOLD                            = 'Hold'
    PENDING_MATCHING                = 'Pending Matching'
    PARTIAL_MATCH                   = 'Partial Match'
    MATCHED                         = 'Matched'
    VOID                            = 'Void'
    MATCHING_FAILED                 = 'Matching Failed'
    REJECTED_SIGN_OFF               = 'Rejected - Sign Off'

#-------------------------------------------------------------------------
class ConfirmationType:
    CANCELLATION                    = 'Cancellation'
    AMENDMENT                       = 'Amendment'
    CHASER                          = 'Chaser'
    RESEND                          = 'Resend'
    DEFAULT                         = 'Default'

#-------------------------------------------------------------------------
class DatePeriodMethod:
    CALENDAR_DAYS                   = 'Calendar Days'
    BUSINESS_DAYS                   = 'Business Days'
    DEFAULT                         = 'Default'

#-------------------------------------------------------------------------
class EventType:
    NEW_TRADE                       = 'New Trade'
    NEW_TRADE_AMENDMENT             = 'New Trade Amendment'
    NEW_TRADE_CANCELLATION          = 'New Trade Cancellation'
    NEW_TRADE_CHASER                = 'New Trade Chaser'
    NEW_TRADE_CLOSE                 = 'New Trade Close'
    NEW_TRADE_DUPLICATE             = 'New Trade Duplicate'
    NEW_TRADE_RESEND                = 'New Trade Resend'
    DEPOSIT_MATURITY                = 'Deposit Maturity'
    DEPOSIT_MATURITY_AMENDMENT      = 'Deposit Maturity Amendment'
    NEW_DEAL_PACKAGE                = 'New Deal Package'
    CLOSE                           = 'Close'
    PARTIAL_CLOSE                   = 'Partial Close'
    RATE_FIXING                     = 'Rate Fixing'
