""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCorporateActionsWorkbenchMenuItem.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCorporateActionsWorkbenchMenuItem


DESCRIPTION

-------------------------------------------------------------------------------------------------------"""


import acm
import FBDPCommon
import FUxCore
import FCASuggestedTasks
import FIntegratedWorkbench
import FProcessCorpActions
import FCorpActionCalculatePositions
import FBDPCurrentContext
import FStartRollback
import FCorpActionUtils
import FCorpActionInstrumentExclusion
#import FMarkitCorporateActionsImport

from contextlib import contextmanager
from FIntegratedWorkbenchMenuItem import IntegratedWorkbenchMenuItem
from FCAWorkbenchCurrentActiveObjects import CurrentActiveObjects
from FCorpActionsWorkbenchLogger import logger
from FCorporateActionsWorkbenchUtils import RegisterElectionGUIUpdater
from FCorporateActionsWorkbenchUtils import RegisterChoiceGUIUpdater
from FCorporateActionsWorkbenchUtils import RegisterPayoutGUIUpdater


def UpdateRunParameters(taskDict):
    argDict = {'Logmode':2,
            'LogToConsole':1,
            'LogToFile':0,
            'Logfile':'BDP.log',
            'SendReportByMail':0,
            'ReportMessageType':'Full log',
            'MailList':''}
    taskDict.update(argDict)


def CreateCorporateActionChoice(corpAction):
    caChoice = acm.FCorporateActionChoice()
    caChoice.CorpAction(corpAction)
    caChoice.Commit()


def CreateCorporateActionPayout(corpActionChoice):
    chPayout = acm.FCorporateActionPayout()
    chPayout.CaChoice(corpActionChoice);
    chPayout.Commit()


class CorporateActionsWorkbenchMenuItem(IntegratedWorkbenchMenuItem):

    def __init__(self, extObj):
        super(CorporateActionsWorkbenchMenuItem, self).__init__(extObj, 'CorporateActionsWorkbenchView')
        self._settings = None

    def CorporateAction(self):
        return self.CurrentActiveObjectHandler().CorporateAction()
        
    def CorporateActions(self):
        return self.CurrentActiveObjectHandler().CorporateActions()

    def CorporateActionElections(self):
        item = self.CurrentActiveObjectHandler().CorporateActionElection()
        if not item:
            return []
        if item.IsKindOf(acm.FCorporateActionElectionMultiItem):
            return item.Elections()
        return [item]

    def Portfolio(self):
        return self.CurrentActiveObjectHandler().Portfolio()
        
    def Trade(self):
        return self.CurrentActiveObjectHandler().Trade()

    def CurrentActiveObjectHandler(self):
        return FIntegratedWorkbench.GetHandler(self.View(), CurrentActiveObjects)

    def Settings(self):
        if not self._settings:
            self._settings = self.CurrentActiveObjectHandler().Settings()
        return self._settings
        
    def RunTaskGUI(self):
        if hasattr(self.Settings(), 'RunTaskGUI'):
            return self.Settings().RunTaskGUI()
        return 0

    def election_ael_variables_updater(self, ael_variables):
        self.CurrentActiveObjectHandler().election_ael_variables_updater(ael_variables)

    def choice_ael_variables_updater(self, ael_variables):
        self.CurrentActiveObjectHandler().choice_ael_variables_updater(ael_variables)

    def payout_ael_variables_updater(self, ael_variables):
        self.CurrentActiveObjectHandler().payout_ael_variables_updater(ael_variables)


class ImportCorporateActionsMenuItem(CorporateActionsWorkbenchMenuItem):
        
    def Invoke(self, eii):
        acm.RunModuleWithParameters("FMarkitCorporateActionsImport", acm.GetDefaultContext())
        
        
class GenerateElectionsMenuItem(CorporateActionsWorkbenchMenuItem):
        
    def Invoke(self, eii):
        corporateAction = self.CorporateAction().Name() if self.CorporateAction() else ''
        if self.RunTaskGUI():
            paramsText = FCASuggestedTasks.GENERATEELECTIONS_PARAMETERS_TEXT.format(corporateAction)
            FCASuggestedTasks.startSuggestTask('GenerateElection_Suggest', FCASuggestedTasks.GENERATEELECTIONS_MODULE_NAME, paramsText)
        else:
            argDict = {'CorpActions':[self.CorporateAction()], 
                    'PortfolioGrouper':None,
                    'Testmode':0}
            UpdateRunParameters(argDict)
            FCorpActionCalculatePositions.ael_main(argDict)
        
class ProcessElectionsMenuItem(CorporateActionsWorkbenchMenuItem):
        
    def Invoke(self, eii):
        corporateAction = self.CorporateAction().Name() if self.CorporateAction() else ''
        
        if self.RunTaskGUI():
            paramsText = FCASuggestedTasks.PROCESSELECTIONS_PARAMETERS_TEXT.format(corporateAction) 
            FCASuggestedTasks.startSuggestTask('ProcessElection_Suggest', FCASuggestedTasks.PROCESSELECTIONS_MODULE_NAME, paramsText)
        else:
            argDict = {'CorpActions':[self.CorporateAction()],
                    'Testmode':0}
            UpdateRunParameters(argDict)
            FProcessCorpActions.ael_main(argDict)


class RollbackElectionsMenuItem(CorporateActionsWorkbenchMenuItem):
        
    def Invoke(self, eii):

        corporateAction = self.CorporateAction() if self.CorporateAction() else ''
        elections = self.CorporateActionElections()
        if self.RunTaskGUI():
            rollbackNames = ''
            for e in elections:
                rollbackName = FBDPCommon.GetAdditionalInfoValue(e, 'CorpActionElection', 'RollbackElection') + ','
                if rollbackName:
                    rollbackNames += rollbackName
            if rollbackNames:
                rollbackNames = rollbackNames[0:-1]
            paramsText = FCASuggestedTasks.ROLLBACKPROCESSEDELECTIONS_PARAMETERS_TEXT.format(rollbackNames)
            FCASuggestedTasks.startSuggestTask('RollBackElection_Suggest', FCASuggestedTasks.ROLLBACKPROCESSEDELECTIONS_MODULE_NAME, paramsText)
        elif elections:
            for e in elections:
                self.RollbackElection(e)
        elif corporateAction:
            for choice in corporateAction.CaChoices():
                for election in choice.CaElections():
                    self.RollbackElection(election)
    
    def RollbackAction(self):
        if hasattr(self.Settings(), 'RollbackAction'):
            return self.Settings().RollbackAction()
        return 'Delete'

    def RollbackElection(self, election):
        rollbackName = FBDPCommon.GetAdditionalInfoValue(election, 'CorpActionElection', 'RollbackElection')
        if rollbackName is None:
            rollbackName = ''
        else:
            rollbackSpec = acm.FRollbackSpec[rollbackName]
            if (rollbackSpec != None):
                argDict = {'rollbackSpec':[rollbackSpec], 'instruments':[], 'void':self.RollbackAction()}
                UpdateRunParameters(argDict)
                FStartRollback.ael_main(argDict)
                

class NewCorporateActionMenuItem(CorporateActionsWorkbenchMenuItem):
        
    def Invoke(self, eii):
        acm.RunModuleWithParameters("FNewCorpAction", acm.GetDefaultContext())


class NewCorporateActionChoiceMenuItem(CorporateActionsWorkbenchMenuItem):

    def EnabledFunction(self):
        if self.CorporateAction():
            return True
        return False

    def Invoke(self, eii):
        if self.RunTaskGUI():
            with RegisterChoiceGUIUpdater(self.choice_ael_variables_updater):
                acm.RunModuleWithParameters("FNewCorpActChoice", acm.GetDefaultContext())
        else:
            CreateCorporateActionChoice(self.CorporateAction())


class NewCorporateActionElectionMenuItem(CorporateActionsWorkbenchMenuItem):
        
    def Invoke(self, eii):
        with RegisterElectionGUIUpdater(self.election_ael_variables_updater):
            acm.RunModuleWithParameters("FNewCorpActionElection", acm.GetDefaultContext())

        
class NewCorporateActionPayoutMenuItem(CorporateActionsWorkbenchMenuItem):

    def EnabledFunction(self):
        current = self.CurrentActiveObjectHandler().TreeItem()
        if current.IsKindOf(acm.FCorporateActionChoice):
            return True
        return False
        
    def Invoke(self, eii):
        if self.RunTaskGUI():
            with RegisterPayoutGUIUpdater(self.payout_ael_variables_updater):
                acm.RunModuleWithParameters("FNewCorpActionPayout", acm.GetDefaultContext())
        else:
            currentChoice = self.CurrentActiveObjectHandler().TreeItem()
            CreateCorporateActionPayout(currentChoice)


class NewCorporateActionPayoutFromTreeViewMenuItem(CorporateActionsWorkbenchMenuItem):
        
    def Invoke(self, eii):
        if self.RunTaskGUI():
            acm.RunModuleWithParameters("FNewCorpActionPayout", acm.GetDefaultContext())
        else:
            currentChoice = self.CurrentActiveObjectHandler().TreeItem()
            CreateCorporateActionPayout(currentChoice)


class NewCorporateActionChoiceFromTreeViewMenuItem(CorporateActionsWorkbenchMenuItem):
        
    def Invoke(self, eii):
        if self.RunTaskGUI():
            with RegisterChoiceGUIUpdater(self.choice_ael_variables_updater):
                acm.RunModuleWithParameters("FNewCorpActChoice", acm.GetDefaultContext())
        else:
            currentCA = self.CurrentActiveObjectHandler().TreeItem()
            CreateCorporateActionChoice(currentCA)


class StartCorporateActionsWorkbenchMenuItem(FUxCore.MenuItem, object):

    def Invoke(self, eii):
        FIntegratedWorkbench.LaunchView('CorporateActionsWorkbenchView')
        

class FreezePositionMenuItem(CorporateActionsWorkbenchMenuItem):

    def EnabledFunction(self):
        fCount, uCount = FCorpActionInstrumentExclusion.FrozenAndUnFrozenInstrumentsCount(self.CorporateActions())
        if uCount > 0:
            return True
        return False

    def Invoke(self, eii):
	for ca in self.CorporateActions():
            FCorpActionInstrumentExclusion.AddInstrumentToPageGroups(ca)


class UnFreezePositionMenuItem(CorporateActionsWorkbenchMenuItem):

    def EnabledFunction(self):
        fCount, uCount = FCorpActionInstrumentExclusion.FrozenAndUnFrozenInstrumentsCount(self.CorporateActions())
        if fCount > 0:
            return True
        return False
        
    def Invoke(self, eii):
	for ca in self.CorporateActions():
            FCorpActionInstrumentExclusion.RemoveInstrumentFromPageGroups(ca)
            
        
def CreateImportCorporateActionsMenuItem(eii):
    return ImportCorporateActionsMenuItem(eii)


def CreateGenerateElectionsMenuItem(eii):
    return GenerateElectionsMenuItem(eii)

    
def CreateProcessElectionsMenuItem(eii):
    return ProcessElectionsMenuItem(eii)


def CreateRollbackElectionsMenuItem(eii):
    return RollbackElectionsMenuItem(eii)


def CreateNewCorporateActionMenuItem(eii):
    return NewCorporateActionMenuItem(eii)

    
def CreateNewCorporateActionChoiceMenuItem(eii):
    return NewCorporateActionChoiceMenuItem(eii)

    
def CreateNewCorporateActionElectionMenuItem(eii):
    return NewCorporateActionElectionMenuItem(eii)

    
def CreateNewCorporateActionPayoutMenuItem(eii):
    return NewCorporateActionPayoutMenuItem(eii)

    
def CreateStartCorporateActionsWorkbenchMenuItem(eii):
    return StartCorporateActionsWorkbenchMenuItem()


def CreateNewCorporateActionChoiceFromTreeViewMenuItem(eii):
    return NewCorporateActionChoiceFromTreeViewMenuItem(eii)


def CreateNewCorporateActionPayoutFromTreeViewMenuItem(eii):
    return NewCorporateActionPayoutFromTreeViewMenuItem(eii)
    
    
def CreateFreezePositionMenuItem(eii):
    return FreezePositionMenuItem(eii)


def CreateUnFreezePositionMenuItem(eii):
    return UnFreezePositionMenuItem(eii)
    
    
    
    
