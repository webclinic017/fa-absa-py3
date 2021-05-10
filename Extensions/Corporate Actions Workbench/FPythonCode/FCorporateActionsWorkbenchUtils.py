""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCorporateActionsWorkbenchUtils.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FCorporateActionsWorkbenchUtils

DESCRIPTION

-------------------------------------------------------------------------------------------------"""
import acm
import FSheetUtils
import FIntegratedWorkbench
import FBDPCurrentContext
import FBDPCommon
from contextlib import contextmanager
from FSheetPanel import SheetPanel
from FCorpActionsWorkbenchLogger import logger


@contextmanager  
def RegisterElectionGUIUpdater(updater):
    try:
        FBDPCurrentContext.RegisterElectionGUIUpdater(updater)
        yield
    finally:
        FBDPCurrentContext.RegisterElectionGUIUpdater(None)


@contextmanager  
def RegisterChoiceGUIUpdater(updater):
    try:
        FBDPCurrentContext.RegisterChoiceGUIUpdater(updater)
        yield
    finally:
        FBDPCurrentContext.RegisterChoiceGUIUpdater(None)


@contextmanager  
def RegisterPayoutGUIUpdater(updater):
    try:
        FBDPCurrentContext.RegisterPayoutGUIUpdater(updater)
        yield
    finally:
        FBDPCurrentContext.RegisterPayoutGUIUpdater(None)


def makeElection(invokationInfo):

    handler = FIntegratedWorkbench.GetHandlerByName(FIntegratedWorkbench.GetView(invokationInfo.ExtensionObject()), 'CurrentActiveObjects')

    with RegisterElectionGUIUpdater(handler.election_ael_variables_updater):
        acm.RunModuleWithParameters("FNewCorpActionElection", acm.GetDefaultContext())


def deleteElection(invokationInfo):

    handler = FIntegratedWorkbench.GetHandlerByName(FIntegratedWorkbench.GetView(invokationInfo.ExtensionObject()), 'CurrentActiveObjects')
    
    for election in handler.CorporateActionElections():
        election.Delete()
    
    handler.ElectionDeleted()


def AddEntitiestoSheet(sheet, query, folderName):
    folder = acm.FASQLQueryFolder()
    folder.AsqlQuery(query)
    folder.Name(folderName)
    sheet.InsertObject(folder, 'IOAP_LAST')
    FSheetUtils.ExpandTree(sheet)
    sheet.PrivateTestSyncSheetContents()
