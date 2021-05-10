""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/templates/FAccountingParamsTemplate.py"
"""
----------------------------------------------------------------------------
Basic parameters for ATS-setup, logging and accounting processing.

Changes to any of these settings require a restart of the accounting ATS
for them to take affect
----------------------------------------------------------------------------
"""

ambAddress                       = None

receiverMBName                   = None

receiverSource                   = None

detailedLogging                  = False

daysBack                         = 3

daysForward                      = 0

createZeroAmountJournals         = False

setProtectionAndOwnerFromTrade   = False

realTimeAmendmentTriggerTypes    = ["Real Time"]

tradeFilterQueries               = []

settlementFilterQueries          = []

preventJournalCreationQueries    = []

hooks                            = []
