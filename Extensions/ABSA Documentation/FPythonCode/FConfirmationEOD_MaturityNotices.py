"""---------------------------------------------------------------------------------------------------------------------
MODULE
    FConfirmationEOD_MaturityNotices

DESCRIPTION
    RunScript used to run EOD task that will select trades related to Maturity Notices and generate these confirmation
    documents.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
2019-05-17      FAOPS-453       Hugo Decloedt           Wandile Sithole         Initial implementation
------------------------------------------------------------------------------------------------------------------------
"""

import time

# pylint: disable=import-error
import acm
import FOperationsUtils as Utils
import FConfirmationUnderlyingObject as UnderlyingObject

from FOperationsExceptions import UpdateCollisionException, CommitException
from FConfirmationEngine import FConfirmationEngine as ConfirmationEngine
from FConfirmationEventFactory import FConfirmationEventFactory as ConfirmationEventFactory
from FConfirmationParameters import tradeFilterQueries


# Default name of the Query Folder used to select trades related to Maturity Notices
MATURITY_FOLDER = 'ConfirmationEOD_Maturities'


try:
    import FConfirmationParameters as ConfirmationParameters
except ImportError as error:
    import FConfirmationParametersTemplate as ConfirmationParameters
    Utils.LogAlways("Failed to import FConfirmationParameters, " + str(error))


def _SatisfiesTradeFilters(trade):
    for qfName in tradeFilterQueries:
        qf = acm.FStoredASQLQuery[qfName]
        if qf:
            if not qf.Query().IsSatisfiedBy(trade):
                return False
    return True


def EndOfDay(dictionary):
    """
    End of Day Processing for Confirmations
    """
    Utils.LogAlways('End of Day Process for Confirmations...STARTED %s' % time.asctime(time.localtime()))

    folder = dictionary['Trade_QF']
    tradeResultSet = folder.Query().Select()
    confirmationEngine = ConfirmationEngine()
    totalNumberOfTrades = tradeResultSet.Size()
    counter = 0
    for trade in tradeResultSet:
        if _SatisfiesTradeFilters(trade):
            try:
                Utils.LogVerbose("Processing trade %d" % trade.Oid())
                confirmationEngine.Create(UnderlyingObject.CreateUnderlyingObject(trade),
                                          ConfirmationEventFactory.GetConfirmationEvents())
            except UpdateCollisionException as err:
                Utils.LogAlways('%s: %s' % (EndOfDay.__name__, str(err)))
            except CommitException as err:
                Utils.LogAlways('%s: %s' % (EndOfDay.__name__, str(err)))

        counter += 1
        Utils.LogAlways("%.2f%% completed" % (float(counter) / totalNumberOfTrades * 100))

    Utils.LogAlways('End of Day Process for Confirmations...FINISHED %s' % time.asctime(time.localtime()))


ael_variables = [['Trade_QF', 'Trade QueryFolder', acm.FStoredASQLQuery, None, acm.FStoredASQLQuery[MATURITY_FOLDER],
                  1, 0, 'Choose Query Folder', None, 1]]


def ael_main(dictionary):
    """
    Main function for RunScriptCMD
    :param dictionary: FDictionary
    """
    Utils.InitFromParameters(ConfirmationParameters)
    EndOfDay(dictionary)
