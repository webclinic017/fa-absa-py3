""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementParametersTemplate.py"
"""----------------------------------------------------------------------------
Basic paramaters for ATS-setup, logging and settlement processing.

Changes to any of these settings require a restart of the settlement ATS
for them to take affect
----------------------------------------------------------------------------"""

from FOperationsHook import CustomHook
import FSettlementSwiftDefaultXML as SwiftDefaultXML

ambAddress                       = ''

receiverMBName                   = 'settlement_RECEIVER'

receiverSource                   = 'BO'

maximumDaysBack                  = 10

maximumDaysForward               = 10

alternativeCouponHandling        = False

considerResetsForTRSDividends    = True

detailedLogging                  = False

forwardEarlyTermination          = True

updateVoidedSettlement           = True

setProtectionAndOwnerFromTrade   = True

confirmationEventHandling        = False

preventSettlementCreationQueries = []

preventSettlementDeletionQueries = []

preventAutomaticNetting          = []

tradeFilterQueries               = []

tradeAmendmentQueries            = []

correctTradePayNetQueries        = []

hooks                            = []

MTMessageToXMLMap                = [('ALL', SwiftDefaultXML.documentSettlementSWIFT )]

defaultPartialSettlementType     = 'NPAR'
