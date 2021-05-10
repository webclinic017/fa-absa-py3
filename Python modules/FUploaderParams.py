"""----------------------------------------------------------------------------------------------
MODULE
    FUploaderParams

DESCRIPTION
    Date                : 2021-01-15
    Purpose             : 
    Department and Desk : PCG and Prime Services
    Requester           : Helen Comninos
    Developer           : Qaqamba Ntshobane

HISTORY
==================================================================================================
Date            Change no       Developer               Description
2021-01-15      PCGDEV-656      Qaqamba Ntshobane       Initial implementation

ENDDESCRIPTION
-----------------------------------------------------------------------------------------------"""

import acm

TODAY = acm.Time.DateToday()
CALENDAR = acm.FCalendar["ZAR Johannesburg"]
ENV = acm.FDhDatabase['ADM'].InstanceName()

TABLE_HEADINGS = 'Subaccount', 'Instrument Name', 'Trade', 'Status', 'Margin Uploaded', 'Comment'
REPORT_HEADING_ITAC = 'ITAC Initial Margin'
REPORT_HEADING_YIELDX = 'YieldX Initial Margin'
REPORT_HEADING_AGRIS = 'Agris Initial Margin'

EMAIL_SENDER = 'ABCapITRTBAMFrontAre@absa.africa'

EMAIL_SUBJECT_ITAC = 'ITAC Initial Margin Upload Report %s - [{}]'.format(ENV)
EMAIL_SUBJECT_YIELDX = 'YieldX Initial Margin Upload Report %s - [{}]'.format(ENV)
EMAIL_SUBJECT_AGRIS = 'Agris Initial Margin Upload Report %s - [{}]'.format(ENV)

SUBACCOUNT_INDEX = 0
MEMBER_MARGIN_INDEX = 4
CLIENT_MARGIN_INDEX = 5
FUNDING_INTEREST_INDEX = 8
TOTAL_DIV_INDEX = 11

PAYMENT_TYPE = 'Cash'
FUNDING_TEXT = 'Funding Interest'
DIVIDEND_TEXT = 'Dividend Amount'

REPORT_STATUS = {
                "success_status": "Success",
                "failure_status": "Failed",
                "skipped_status": "Skipped",
                "updated_status": "Updated",
                "zero_margin": "Margin is zero",
                "amount_error": "Amount is an invalid number",
                "status_error": "This trade is in Void/Simulated status",
                "file_error": "There's no source file for this date",
                "booking_error": "Booking error. Check if call account details are correct",
                "externalId_error": "No instrument with this subaccount",
                "missing_trade_error": "No live trade with this subaccount",
                "duplicate_moneyflow": "Cashflow already exists",
                "trade_error": "Trade number does not exist",
                "margin_updated": "Margin adjusted from %s to (see Margin Uploaded)",
                }
