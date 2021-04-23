""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramUpload.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FTradeProgramUpload

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import FUxCore #@UnresolvedImport
import acm
import os
from FTradeProgramTM import FTradeProgramTM
from FParameterSettings import ParameterSettingsCreator
from FTradeProgramMenuItem import TradeProgramActionMenuItem
from FTradeProgramAction import Action, OpenPositionAction
import FTradeProgramUploadEngine
from FIntegratedWorkbenchLogging import logger

try:
    import FReconciliationSpecification
except ImportError:
    uploadAvailable = False
else:
    uploadAvailable = True

@Action
def CreateTradeProgramUploadMenuItem(eii):
    return FTradeProgramUploadMenuItem(eii) 

class FTradeProgramUploadMenuItem(TradeProgramActionMenuItem):
    
    def EnabledFunction(self):
        return uploadAvailable
        
    def Invoke(self, eii):
        shell = eii.Parameter('shell')
        dialogOutput = self.StartDialog(shell)
        if dialogOutput:
            filePath, reconciliationSpecification = dialogOutput
            trades = runUpload(filePath, reconciliationSpecification, self._frame, shell)
            if trades:
                tpUploadTM = FTradeProgramUploadTM(eii, trades)
                tpUploadTM.ExecuteTrades()
        
    def InvokeAsynch(self, _eii):
        raise NotImplementedError
        
    def StartDialog(self, shell):
        dlg = TradeProgramUploadDialog(self._frame)
        return acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)
    
    def Action(self):
        return OpenPositionAction('External')
        

class TradeProgramUploadDialog(FUxCore.LayoutDialog):
    def __init__(self, tradingManagerFrame):
        self.layout = None
        self.dialog = None
        self.tradingManagerFrame = tradingManagerFrame
        self._filePath = None
        self._reconciliationSpecification = None
        
    def ReconiliationSpecification(self):
        return self._reconciliationSpecification
    
    def FilePath(self):
        return self._filePath
        
    def HandleApply(self):
        return (self.FilePath(), self.ReconiliationSpecification())
        
    def HandleCreate(self, dialog, layout):
        self.dialog = dialog
        self.layout = layout
        self.reconSpecCtrl = layout.GetControl('reconSpecCtrl')
        self.filePathCtrl = layout.GetControl('filePathCtrl')
        self.fileBrowserCtrl = layout.GetControl('fileBrowserCtrl')
        self.ok = layout.GetControl('ok')
        self.cancel = layout.GetControl('cancel')
        self.PopulateControls()
        self.InitCallbacks()
        
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('EtchedIn', 'Trade program')
        b. AddOption('reconSpecCtrl', 'Upload specification', 40)
        b. BeginHorzBox()
        b.  AddInput('filePathCtrl', 'File')
        b.  AddButton('fileBrowserCtrl', '...', False, True)
        b. EndBox()
        b. BeginHorzBox()
        b.  AddFill()
        b.  AddButton('ok', 'Ok')
        b.  AddButton('cancel', 'Cancel')
        b. EndBox()
        b.EndBox()
        
        return b
    
    def PopulateControls(self):
        self.ok.Enabled(False)
        uploadSpecifications = sorted(FReconciliationSpecification.GetReconciliationSpecificationNames(True))
        for spec in uploadSpecifications:
            self.reconSpecCtrl.AddItem(spec)
    
    def InitCallbacks(self):
        self.fileBrowserCtrl.AddCallback('Activate', self.OnFileSelectionClicked, None)
        self.filePathCtrl.AddCallback('Changed', self.OnFileSelectionChanged, None)
        self.reconSpecCtrl.AddCallback('Changed', self.OnReconSpecChanged, None)
    
    def OnFileSelectionChanged(self, *args):
        self._filePath = self.filePathCtrl.GetData()
        self.ok.Enabled(self.HasValidOutput())
        
    def OnReconSpecChanged(self, *args):
        self._reconciliationSpecification = self.reconSpecCtrl.GetData()
        self.ok.Enabled(self.HasValidOutput())
        
    def OnFileSelectionClicked(self, *args):
        self.LaunchFileSelector(self.dialog.Shell())
        
    def LaunchFileSelector(self, shell):
        fileFilter = [
            'All Files (*.*)|*.*'
            ]
        if self.ReconciliationSpecificationExists():
            fileType = GetParameterAsString('File Format', self.reconSpecCtrl.GetData()).lower()
            fileFilter = ['{0} format (*.{0})|*.{0}'.format(fileType)] + fileFilter
        path = 'c:\\'
        selection = acm.UX.Dialogs().BrowseForFiles(self.dialog.Shell(), '|'.join(fileFilter), path)
        selectedFile = selection[0] if selection else None
        if selectedFile:
            self.filePathCtrl.SetData(
                    ''.join((
                    str(selectedFile.SelectedDirectory()),
                    str(selectedFile.SelectedFile()))))
        
    def HasValidOutput(self):
        return (self.ReconciliationSpecificationExists() and self.IsValidFilePath())
         
    def ReconciliationSpecificationExists(self):
        recSpec = self.ReconiliationSpecification()
        return bool(recSpec is not None 
                    and recSpec != '')

    def IsValidFilePath(self):   
        return bool(self.FilePath() is not None 
                    and os.path.isfile(self.FilePath()))
    
def runUpload(filePath, uploadSpecification, tradingManagerFrame, shell):

    path = acm.FFileSelection()
    path.SelectedFile(filePath)
    fileName = str(path.SelectedFile())

    try:
        reconSpec = FReconciliationSpecification.FReconciliationSpecification(uploadSpecification)
        engine = FTradeProgramUploadEngine.FTradeProgramUploadEngine(fileName, reconSpec)
        engine.Run()
    except StandardError as e:
        logger.error('Failed to load data upload specification "%s": %s', \
                     uploadSpecification, e)
        ErrorInUploadMessage(e, shell)
        return None 
    
    reconInstance = engine.ReconciliationInstance()
    if reconInstance:
        logger.info('Processed %d item(s) for this file', reconInstance.ReconciliationDocument().ProcessedItemCount())

        trades = []
        for (i, wf) in enumerate(reconInstance.Workflows()):
            if wf.ErrorMessage():
                acm.UX().Dialogs().MessageBoxInformation(shell, 'Error in Upload on row %d: %s'%(i, wf.ErrorMessage()))
                return None
            if wf.BusinessObjectValidationMessage():
                acm.UX().Dialogs().MessageBoxInformation(shell, 'Error in Validation on row %d: %s'%(i, wf.BusinessObjectValidationMessage()))
                return None
            trades.append(wf.ACMObject())
        sheet = tradingManagerFrame.ActiveSheet()
        if sheet.SheetClass() == acm.FPortfolioSheet:
            portfolios = set()
            portfoliosToAdd = set()
            for row in sheet.GetAllOfType(acm.FPortfolioInstrumentAndTrades):
                portfolios.add(row.Portfolio().Name())
            for t in trades:
                if not t.Portfolio().Name() in portfolios:
                    portfoliosToAdd.add(t.Portfolio().Name())
            if portfoliosToAdd != set():
                acm.UX().Dialogs().MessageBoxInformation(shell, 'Warning: All portfolios in the trade program file are not present in the portfolio sheet. These will be added automatically.')
                for p in portfoliosToAdd:
                    sheet.InsertObject(acm.FPhysicalPortfolio[p], 'IOAP_LAST')
        logger.info('Adding trades to new trade program')       
    logger.info('Data upload processing complete')
    return trades
    
class FTradeProgramUploadTM(FTradeProgramTM):
    
    def __init__(self, eii, trades):
        self._trades = trades
        self.settings = ParameterSettingsCreator.FromRootParameter('ExternalSettings')
        FTradeProgramTM.__init__(self, eii, action=OpenPositionAction(self.settings.Action()), name='External')
        
    def ExecuteTrades(self):
        FTradeProgramTM.Execute(self, self._trades)


def GetParameterAsString(parameter, category):
    extension = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', category)
    try:
        return extension.Value().At(parameter).Text()
    except AttributeError:
        try:
            return extension.Value().At(parameter)
        except AttributeError:
            return None

def ErrorInUploadMessage(e, shell):
    acm.UX().Dialogs().MessageBoxInformation(shell, 'Error in Upload: %s'%(e))