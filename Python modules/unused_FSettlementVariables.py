""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementVariables - Module with variables needed by the FSettlementEOD
    and the FSettlementAMB script.

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    In this module customers can do their own customization for the settlement
    generation scripts.    
     
RENAME this module to FSettlementVariables.

----------------------------------------------------------------------------"""

import ael

# Accounting currency used for detecting banking day.
# acc_curr = 'EUR'
acc_curr = ael.used_acc_curr()

# The number of banking days from today and backwards. Settlements with value_day
# within this time intervall will be generated.
#days_back = 10
days_back = 7

# The number of days from today that settlements should be generated for.
# Days are specified per currency. New currencies can be added here.
#days_curr = {'AUD':10,
#             'CAD':10,
#             'CHF':10,
#             'DKK':10,
#             'EUR':10,
#             'GBP':10,
#             'JPY':10,
#             'LUF':10,
#             'NOK':10,
#             'NZD':10,
#             'SEK':10,
#             'SGD':10,
#            'USD':10,
#             'ZAR':10}
days_curr = {'ZAR':7}

# A list of trade status levels to generate settlements for.
# Note that this list should also include user defined trade status(es)
#status = ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']
status = ['BO Confirmed', 'BO-BO Confirmed']

# Level of information that will be logged. Values are from 0 to 5 where 0
# means that only critical logging will be performed.
#verbosity = 0
verbosity = 5

# Arena Message Broker, server:port
#amb_login = 'sun52:10000'
amb_login = '127.0.0.1:9300'

# Print recieved AMBA messages to ATS log file, 1 means print.
print_mode = 1

# ATS_SINGLE_PROD is a receiver and therefore this name must be added to the
# system table in the AMB database.
#RECEIVER_MB_NAME = 'BO_RECEIVER'
RECEIVER_MB_NAME = 'STLM_PROD_RECEIVER'

# Equal to the value of -sender_source configured in the amba.ini file.
#RECEIVER_SOURCE = 'BO'
RECEIVER_SOURCE = 'STLM_AMBA_PROD'

# The variable handle_combination_cash_flows determines how cash flows for
# instruments of type Combination should be handled. If the variable is set
# to 0 (default) only non cash flow settlement records such as Premium will 
# be created. If the variable is 1, settlement records for all combination 
# cash flows will be created. 
handle_combination_cash_flows = 0

# Default Instrument types that are supported
# In order to exclude some Instrument types you are allowed to 
# reduce a number of items in this list (do not add anything)
#valid_instrument_types = ['BasketRepo/Reverse', 'BasketSecurityLoan', 'Bill',
#                          'Bond', 'BuySellback', 'Cap', 'CD', 'CFD', 
#                          'Combination', 'CreditDefaultSwap', 'Curr', 'CurrSwap', 
#                          'Deposit', 'DualCurrBond', 'EquityIndex', 'EquitySwap', 
#                          'Floor', 'FRA', 'FreeDefCF', 'FRN', 'Future/Forward',
#                          'FxSwap', 'IndexLinkedBond', 'IndexLinkedSwap', 'MBS/ABS', 'Option',
#                          'PromisLoan', 'Repo/Reverse', 'SecurityLoan', 'Stock', 
#                          'Swap', 'TotalReturnSwap', 'VarianceSwap', 'Warrant', 'Zero']
valid_instrument_types = ['Deposit', 'EquitySwap', 'Future/Forward', 'Option', 'VarianceSwap', 'Zero', 'FRN', 'CD']

# The different statuses in this list decide which settlements that will not
# be deleted if keep_old_settlements_when_void = 1 and corresponding trade
# is voided (see also variable recall_if_trade_status_is_void further bellow). 
# Note that you can only remove settlement status from the list, do not add any status!
keep_status = ['New', 'Recalled', 'Updated', 'Exception', 'Manual Match',\
                 'Hold', 'Void', 'Authorised', 'Not Acknowledged']

# When voiding a trade, old settlements in status in the keep status list should not be
# deleted if keep_old_settlements_when_void = 1. Default value is 0.
keep_old_settlements_when_void = 0                      

# valid_instrument_types_accrued_interest is a list of instrument types for
# which settlement records for accrued interest are created. Such settlement
# records are created when "close trade" is done on a trade. The record is of
# type Fixed Rate but it does not have any cash flow reference. Note that the
# amount is based on the quantity and value day of the closing trade. Also
# note that a trade that is closed via several closing trades will result in
# one settlement record for accrued interest for each closing trade.
# As of SPR271883 'CreditDefaultSwap' and 'TotalReturnSwap' are not supported any more
#valid_instrument_types_accrued_interest = ['EquitySwap', 'Swap']
valid_instrument_types_accrued_interest = []

# Un-net action in the Settlement Manager can result that settlements are netted again
# because netting rule is still active. Set this flag to zero (net_after_unnet = 0) 
# if you want to be able to un-net and preserve settlements in that way. 
# Note that when un-netting the keyword net0 should be written in the settlement diary. 
# If you want the settlement to be nettable later on the keyword net1 should be used. 
# Hence the latest keyword (net0 or net1) in the settlement diary decides.
net_after_unnet = 1

# round_net_amount toggles whether the amount of netted settlements should be rounded or not
round_net_amount = 0

# Switch if the coupon handling should be treated in the alternative way or not. Default is 0.
# Alternative way is for customers that prefer having one single coupon settlement row 
# then multiple ones (in case of different accounts and portfolios in trades in the same 
# instrument with the same counterparty). Amount of the coupon becomes a sum of all instrument 
# positions per account where accounts are fetched from closed security nominals.
# Note that switching alternative_coupon_handling from default 0 to 1 will affect future 
# coupon and redemption updates especially if there are more then one settlement row 
# per security instrument.
alternative_coupon_handling = 0

# If trades with certain acquirers shall be excluded from settlement record creation, add the
# names of those acquirers in the following list. The names have to be enclosed with quotation marks
# like this 'ACQUIRER NAME'. Every name has to be separated by a comma. By default this list is empty.
#exclude_acq = []
exclude_acq = ['Funding Desk', 'EQ Derivatives Desk', 'Money Market Desk']

# If trades with certain portfolios shall be excluded from settlement record creation, add the
# names of those portfolios in the following list. The names have to be enclosed with quotation marks
# like this 'PORTFOLIO NAME'. Every name has to be separated by a comma. By default this list is empty.
exclude_portfolio = []

# Settlements in status 'Void' shall, if applicable, be updated. If a settlement record
# in status void is updated, a new settlement record will be created, referencing the voided settlement.
# The referencing settlement record will get status 'Updated'. Settlement records that are part of netting are
# are not affected by this variable. The default is set to 1. If set to 0, no updates will be reflected on the
# settlement record.
update_void = 1

# Variable special_otc_instrument_handling is used for handling settlement record creation for OTC-instruments
# special_otc_instrument_handling shall have one of the following values:
# 0 = No special treatment. Create settlement records for all instruments (Default).
# 1 = Create settlement records ONLY for otc-instruments.
# 2 = Create settlement records ONLY for NON otc-instruments.
# If special_otc_instrument_handling has a value not equal to one of the above, it will be treated as if
# it is set to the default i.e. 0.
#special_otc_instrument_handling = 0
special_otc_instrument_handling = 1

# The consider_resets_for_eq_swap_dividends-variable is used when creating 
# dividend settlement records for equity swap trades.
# When set to 1 (default), a dividend settlement records is created if 
# the Ex Div Day of the dividend is later than the 
# earliest reset day, and earlier or at the same day as the latest reset day.
# I.e. earliest reset day < Ex Div Day <= latest reset day.
# If consider_resets_for_eq_swap_dividends is set to 0, a dividend settlement 
# record will be created if the value day of the trade is earlier or at the 
# same day as the Ex Div Day. I.e. value day <= Ex Div Day. Resets are not 
# considered when consider_resets_for_eq_swap_dividends is set to 0. 
#consider_resets_for_eq_swap_dividends = 1
consider_resets_for_eq_swap_dividends = 0

# Should the variable 'recall_if_trade_status_is_void' be set to 1, settlement 
# records belonging to a trade in status 'Void', 'Confirmed Void', 'Terminated'
# or 'Simulated' will be recalled. Note that settlement statuses defines criteria 
# for recalling settlements (see variable keep_status).
# If 'recall_if_trade_status_is_void' is set to 0, settlement records belonging 
# to a trade in status 'Void'  will NOT be recalled. Only settlements records 
# belonging to a trade in status 'Confirmed Void', 'Terminated' or 'Simulated' 
# will be recalled. The default is set to 1.
recall_if_trade_status_is_void = 1

# If variable update_recalled is set to 0, settlements in status 
# Recalled will not be updated.
update_recalled = 1

# Variable to decide if the payout on an early terminated cash/physical settled forward should be paid 
# on the value day of the close trade, or if it should be paid on the instrument expiry day + spot days.
# If forward_early_termination is set to 0 a payout settlement will be created on the value day of the closing trade.
# If set to 1 payout settlement for the closing trade will be created on expiry date and value day will be set to 
# expiry day + spot days.
# Default is 0
forward_early_termination = 0

# If variable invert_exclude_acq is set to 1, trades with acquirers set in exclude_acq-list
# are eligible for settlement processing, whereas trades with acquirers NOT in the exclude_acq-list
# will NOT be eligible for settlement processing. Default value for invert_exclude_acq is 0.
#invert_exclude_acq = 0
invert_exclude_acq = 1

# If variable invert_excluded_portfolio is set to 1, trades with portfolios set in exclude_portfolio-list
# are eligible for settlement processing, whereas trades with portfolios NOT in the exclude_portfolio-list
# will NOT be eligible for settlement processing. Default value for invert_exclude_portfolio is 0.
invert_exclude_portfolio = 0

# This variable is used to allow the event_cb to wait for related events after an instrument update 
# event before work_cb kicks in. CALL_BACK_SLEEP = 2 would mean 2 seconds sleep but default is 0.5 seconds.
# This was done to solve SPR 286116 that solved duplicate fixed amount settlements rarely created for Call Deposits
#CALL_BACK_SLEEP = 0.5
CALL_BACK_SLEEP = 2.0

# List containing the names and values of additional infos on a cash flow record. Used for preventing
# creation of settlemetn records. The names and values, both of type string, have to be entered as tuple pairs.
# Example:  cash_flow_additional_infos = [('MyAdditionalInfo1', 'Exclude'), ('MyAdditionalInfo2', 'Prevent')]
cash_flow_additional_infos = []

# For open ended call deposits with a rolling period, the user can now set how many business days a head
# of the end of the rolling period for the interest settlement record (Call Fixed Rate, Call Fixed Rate Adjustable
# and Call Float Rate) to be created. Default value is 1 day. All historic cashflows will generate settlements.
# If the value is set to -1 the previous behaviour will be used and no new ATS version (1.1.2.hotfix33 or later)
# is needed.
# Example: Rolling period is "1m" and starting on 2009-01-01. If the 31:th of January is on a Monday the
# settlement record will be created on Friday if the variable is set to 1.
# Setting the variable to:
# -1, means old behaviour and no new ATS version is needed
# 0, settlement will be created on the same say as the end_day
# 1, settlement will be created one business day before end_day
# N, settlement will be created N business days before end_day
#days_forward_for_call_account = 1
days_forward_for_call_account = -1


