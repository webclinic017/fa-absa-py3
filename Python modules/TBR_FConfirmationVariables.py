""" Compiled: 2009-10-14 04:19:36 """

"""----------------------------------------------------------------------------
MODULE
    FConfirmationVariables - Module with customer specific variables.

    (c) Copyright 2005 by Front Capital Systems AB. All rights reserved.

DESCRIPTION    

RENAME this module to FConfirmationVariables
----------------------------------------------------------------------------"""
# A list of trade statuses that confirmations will be generated for.
valid_trade_statuses = ['BO Confirmed', 'BO-BO Confirmed', 'Terminated']

# Level of information that will be logged. Values are from 0 to 5 where
# 0 means that only critical logging will be performed.
log_level = 1

# Integer that indicate the level of debug trace information that will be
# generated in the ATS log. Values are from 0 to 5 where 0 means no tracing.
trace_level = 1

# Arena Message Broker, server:port

amb_login = '127.0.0.1:9300'
print amb_login

# Print recieved AMBA messages to ats logfile, 1 means print.
print_mode = 1

# FConfirmationAMB is executed by the ATS. ATS in it's turn connects to AMB.
# Therefore the system table in the AMB database must contain this receiver
# name.
RECEIVER_MB_NAME = 'CONF_ATS_PROD_RECEIVER'

# Equal to the value of -sender_source configured in the amba.ini file.
RECEIVER_SOURCE = 'CONF_PROD'

# Default values for sedning chasers. These apply if chaser cutoff information
# cannot be found for the counterparty.  If
# default_chaser_cutoff_method_business_days is 1 the value of
# default_chaser_cutoff_days is interpreted as business days, otherwise as
# calendar days.
default_chaser_cutoff_days = 3
default_chaser_cutoff_method_business_days = 1

# If this parameter is set to 1 the Cancellation event occurs when the trade is
# set to status Confirmed Void, instead of status Void.
cancel_on_confirmed_void = 0

#If this parameter is set to Confirmed barrier crossing confirmations will be 
#generated when the barrier crossed status is set to Confirmed. 
#If this parameter is set to Crossed barrier crossing confirmation will be 
#generated when the the barrier crossed status is set to Confirmed or Crossed.
barrier_crossed_creation_status = "Confirmed"
