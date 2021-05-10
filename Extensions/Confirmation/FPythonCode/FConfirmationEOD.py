""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationEOD.py"
import acm, time

import FOperationsUtils as Utils
import FConfirmationUnderlyingObject as UnderlyingObject

from FOperationsExceptions import UpdateCollisionException, CommitException, InvalidHookException
from FConfirmationTradeFilter import ConfirmationEODTradeFilterHandler
from FConfirmationEngine import FConfirmationEngine as ConfirmationEngine
from FConfirmationCreator import FConfirmationCreator as ConfirmationCreator
from FConfirmationCommitter import Committer
from FConfirmationEventFactory import FConfirmationEventFactory as ConfirmationEventFactory
from FConfirmationHelperFunctions import FConfirmationHelperFunctions as HelperFunctions
from FConfirmationEnums import ConfirmationStatus

def CreateChasers(today = acm.GetFunction('dateToday', 0)()):
    confirmations = acm.FConfirmation.Select('status = "%s"' % ConfirmationStatus.PENDING_MATCHING)

    ##Fetch chaser comment from extension value
    chaserCommentExits = False
    chaserComment = acm.GetDefaultContext().GetExtension('FExtensionValue', 'FConfirmation', 'chaserComment')
    if (chaserComment != None and len(chaserComment.Value()) > 0):
        chaserCommentExits = True

    for confirmation in confirmations:
        if not confirmation.ChaserCutoff():
            Utils.LogVerbose("Confirmation %d is missing chaser cutoff date. Chaser will not be created." % confirmation.Oid())
            continue
        chasers = acm.FConfirmation.Select('chasingConfirmation = %d' % confirmation.Oid())
        if len(chasers) == 0:
            if (today >= confirmation.ChaserCutoff() and HelperFunctions.IsApplicableForChaserGeneration(confirmation)):
                confirmationList = list()
                if confirmation.IsApplicableForSWIFT():
                    if chaserCommentExits:
                        sendChaser = acm.FSendChaser([[confirmation], chaserComment.Value()])
                        sendChaser.Execute()
                        result = sendChaser.CommitResult()
                        newConfirmation = result.InsertedConfirmations()[0]
                    else:
                        Utils.LogVerbose("Could not create chaser for Confirmation %d. chaserComment ExtensionValue is missing." % confirmation.Oid())
                        continue
                else:
                    sendChaser = acm.FSendChaser([[confirmation], ''])
                    sendChaser.Execute()
                    result = sendChaser.CommitResult()
                    newConfirmation = result.InsertedConfirmations()[0]
                ConfirmationCreator.AppendIfValidConfirmation(newConfirmation, confirmationList)
                for _confirmation in confirmationList:
                    try:
                        Committer(_confirmation).Commit()
                        Utils.LogVerbose("Created chaser for confirmation %d" % confirmation.Oid())
                    except UpdateCollisionException as updateCollisionException:
                        Utils.LogAlways('%s: %s' % (CreateChasers.__name__, str(updateCollisionException)))
                    except CommitException as commitException:
                        Utils.LogAlways('%s: %s' % (CreateChasers.__name__, str(commitException)))

def ChangeConfirmationStatusToMatching():
    '''
    Changes status of confirmations to status Matched,
    according to query changeConfirmationStatusToMatchedQuery
    defined in FConfirmationParameters.
    '''
    import FConfirmationParameters as ConfirmationParameters

    Utils.LogVerbose("Changing status to Matched on confirmations matching query changeConfirmationStatusToMatchedQuery in FConfirmationParameters")
    changeStatusStr = ConfirmationParameters.changeConfirmationStatusToMatchedQuery
    if changeStatusStr:
        storedQuery = Utils.GetStoredQuery(changeStatusStr, acm.FConfirmation)
        if storedQuery:
            query = storedQuery.Query()
            confirmations = query.Select()
            for confirmation in confirmations:
                if(confirmation.IsNewestInConfirmationChain()):
                    Utils.LogAlways("Changing status of confirmation %d from status %s to status Matched" % (confirmation.Oid(), confirmation.Status()))
                    clone = confirmation.Clone()
                    clone.Status(ConfirmationStatus.MATCHED)
                    confirmation.Apply(clone)
                    try:
                        confirmation.Commit()
                    except Exception as e:
                        Utils.LogAlways("Error: Failed to set status of confirmation %d. %s" % (confirmation.Oid(), str(e)))
    else:
        Utils.LogVerbose("Parameter changeConfirmationStatusToMatchedQuery: %s in FConfirmationParameters undefined, no confirmations updated" %
        changeStatusStr)

def EndOfDay(dictionary):
    '''
    End of Day Processing for Confirmations
    '''
    Utils.LogAlways('End of Day Process for Confirmations...STARTED %s' % time.asctime(time.localtime()))

    regenerateConfirmations = dictionary['regenerateConfirmations']

    if regenerateConfirmations == True:
        eodTradeFilterHandler = ConfirmationEODTradeFilterHandler()
        tradeResultSet = eodTradeFilterHandler.GetObjects()
        tradeResultSet.SortByProperty('Oid', True)
        confirmationEngine = ConfirmationEngine()
        totalNumberOfTrades = tradeResultSet.Size()
        counter = 0
        for trade in tradeResultSet:
            try:
                counter += 1
                Utils.LogVerbose("Processing trade %d (%d of %d)" % (trade.Oid(), counter, totalNumberOfTrades))
                confirmationEngine.Create(UnderlyingObject.CreateUnderlyingObject(trade), ConfirmationEventFactory.GetConfirmationEvents())
            except UpdateCollisionException as err:
                Utils.LogAlways('%s: %s' % (EndOfDay.__name__, str(err)))
            except CommitException as err:
                Utils.LogAlways('%s: %s' % (EndOfDay.__name__, str(err)))
            except InvalidHookException as err:
                Utils.LogAlways('%s: %s' % (EndOfDay.__name__, str(err)))

    CreateChasers()
    ChangeConfirmationStatusToMatching()

    Utils.LogAlways('End of Day Process for Confirmations...FINISHED %s' % time.asctime(time.localtime()))

ael_variables = [('regenerateConfirmations', 'Regenerate confirmations', 'bool', [False, True], True)]

def ael_main(dictionary):
    import FConfirmationParameters as ConfirmationParameters

    Utils.InitFromParameters(ConfirmationParameters)
    EndOfDay(dictionary)

