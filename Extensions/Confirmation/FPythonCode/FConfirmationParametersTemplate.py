""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationParametersTemplate.py"
"""----------------------------------------------------------------------------
MODULE
    FConfirmationParametersTemplate

DESCRIPTION
    Changes to any of these settings require a restart of the
    confirmation ATS for the changes to take affect. Changes that
    affect the XML also require the documentation ATS to be restarted
----------------------------------------------------------------------------"""

from FConfirmationEventHook import ConfirmationEventHook as Hook
from FOperationsHook import CustomHook
import FConfirmationSwiftDefaultXML as SwiftDefaultXML
import FConfirmationDefaultXMLTemplates as defaultXMLTemplates

ambAddress                                      = ''

receiverMBName                                  = ''

receiverSource                                  = ''

confirmationEvents                              = [("Adjust Deposit", "IsNewTradeEvent", "Cash Flow", Hook("FConfirmationDefaultEventHooks", 'IsAdjustDepositEvent')),
                                                    ("Deposit Maturity", Hook("FConfirmationDefaultEventHooks", "IsDepositMaturityEvent")),
                                                    ("Barrier Crossed", Hook("FConfirmationDefaultEventHooks", 'IsBarrierCrossedEvent')),
                                                    ("Close", Hook("FConfirmationDefaultEventHooks", 'IsCloseEvent')),
                                                    ("Exercise", Hook("FConfirmationDefaultEventHooks", 'IsExerciseEvent')),
                                                    ("New Trade", Hook("FConfirmationDefaultEventHooks", "IsNewTradeEvent")),
                                                    ("New Deal Package", Hook("FConfirmationDefaultEventHooks", "IsNewDealPackageEvent")),
                                                    ("Partial Close", Hook("FConfirmationDefaultEventHooks", 'IsPartialCloseEvent')),
                                                    ("Rate Fixing", "IsNewTradeEvent", "Reset", Hook("FConfirmationDefaultEventHooks", 'IsRateFixingEvent')),
                                                    ("Weighted Rate Fixing", "IsNewTradeEvent", "Reset", Hook("FConfirmationDefaultEventHooks", 'IsWeightedRateFixingEvent'))
                                                  ]

templateToXMLMap                                = []

defaultXMLTemplate                              = defaultXMLTemplates.document

detailedLogging                                 = False

tradeFilterQueries                              = []

preventConfirmationCreationQueries              = []

preventConfirmationCancellationQueries          = []

preventConfirmationAmendmentQueries             = []

changeConfirmationStatusToMatchedQuery          = None

defaultChaserCutoffMethodBusinessDays           = False

defaultDays                                     = 10

cancelPreReleasedConfirmations                  = False

cancellationAndNewInsteadOfAmendmentSWIFT       = False

cancellationAndNewInsteadOfAmendmentFreeForm    = False

setProtectionAndOwnerFromTrade                  = False

hooks                                           = []

MTMessageToXMLMap                               = [('ALL', SwiftDefaultXML.documentConfirmationSWIFT)]