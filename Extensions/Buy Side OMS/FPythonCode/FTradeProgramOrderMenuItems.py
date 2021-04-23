""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FTradeProgramOrderMenuItems.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FTradeProgramOrderMenuItems

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    This module contains right click buttons for the order sheet to inspect Trade Program details
-------------------------------------------------------------------------------------------------"""
import acm
import FUxCore
import FTradeProgram
from FAssetManagementUtils import logger
from FComplianceCheckReport import SETTINGS
try:
    from FRiskComplianceViewMenuItem import StartWorkbenchMenuItem
    RC_MODULE_IMPORTED = True
except ImportError:
    RC_MODULE_IMPORTED = False

def OpenBusinessProcessDetails(eii):
    return OpenBusinessProcessDetailsMenuItem(eii)

def OpenReservedTrade(eii):
    return OpenReservedTradeMenuItem(eii)

def OpenComplianceCheckReport(eii):
    return OpenComplianceCheckReportMenuItem(eii)

def OpenInRiskAndComplianceView(eii):
    return OpenInRiskAndComplianceViewMenuItem(eii)

class InspectTradeProgramMenuItem(FUxCore.MenuItem):
    
    def __init__(self, eii):
        self._frame = eii
    
    @staticmethod
    def _Sheet(eii):
        return eii.Parameter('sheet')
    
    @classmethod
    def _OrderProgramId(cls, eii): 
        order = cls._Sheet(eii).Selection().SelectedRowObjects()[0]
        return order.OrderProgramId()
    
    def _SelectedOrder(self, eii):
        order = self._Sheet(eii).Selection().SelectedRowObjects()[0]
        if not order.IsKindOf(acm.FOrderProgram):
            return order
    
    def _BusinessProcess(self, eii):
        dealPackage = acm.FDealPackage[self._OrderProgramId(eii)]
        stateChart = FTradeProgram.TradeProgramWorkflowClass().StateChart()
        bps = acm.BusinessProcess.FindBySubjectAndStateChart(dealPackage, stateChart)
        if len(bps) == 1:
            return bps[0]
        else:
            self._ShowErrorMessage(eii)
    
    def _ShowErrorMessage(self, eii):
        msg = 'No Business Process found for Order Program with id {0}'.format(self._OrderProgramId(eii))
        acm.UX.Dialogs().MessageBoxInformation(self._frame.Shell(), msg)
    
    def Invoke(self, _eii):
        raise NotImplementedError

class OpenBusinessProcessDetailsMenuItem(InspectTradeProgramMenuItem):

    def Invoke(self, eii):
        businessProcess = self._BusinessProcess(eii)
        if businessProcess:
            acm.StartApplication("Business Process Details", businessProcess)
            
            
class OpenReservedTradeMenuItem(InspectTradeProgramMenuItem):

    def Invoke(self, eii):
        order = self._SelectedOrder(eii)
        if order:
            reservedTrade = acm.FTrade[order.OrderId()]
            if reservedTrade:
                acm.StartApplication("Instrument Definition", reservedTrade)            
            else:
                acm.UX.Dialogs().MessageBoxInformation(self._frame.Shell(), 'No reserved trade found')


class OpenInRiskAndComplianceViewMenuItem(InspectTradeProgramMenuItem):
    
    def Invoke(self, eii):
        if RC_MODULE_IMPORTED:
            businessProcess = self._BusinessProcess(eii)
            if businessProcess:
                button = StartRiskAndComplianceWithBP(None, businessProcess)
                button.Invoke(None)
        else:
            msg = 'Must have module "Risk & Compliance View" in order to open Risk & Compliance View'
            acm.UX.Dialogs().MessageBoxInformation(self._frame.Shell(), msg)

if RC_MODULE_IMPORTED:
    class StartRiskAndComplianceWithBP(StartWorkbenchMenuItem):
        
        def __init__(self, _extObj, businessProcess):
            super(StartRiskAndComplianceWithBP, self).__init__(_extObj)
            self._businessProcess = businessProcess
        
        def _SetDefaultContent(self, appl):
            sheet = appl.ActiveSheet()
            sheet.InsertObject(self._businessProcess, 0)
            self.GoToRow(sheet, self._businessProcess)
        
        @staticmethod
        def GoToRow(sheet, businessProcess):
            sheet.PrivateTestSyncSheetContents()
            sheet.NavigateTo(businessProcess)


class OpenComplianceCheckReportMenuItem(InspectTradeProgramMenuItem):

    def Invoke(self, eii):
        businessProcess = self._BusinessProcess(eii)
        if businessProcess:
            dlg = ComplianceCheckReportDialog(businessProcess)
            builder = dlg.CreateLayout()
            acm.UX().Dialogs().ShowCustomDialogModal(self._frame.Shell(), builder, dlg)


def OnCreateViewComplianceCheckReportButton(eii):
    return True

def OnActionViewComplianceCheckReportButton(eii):
    try:
        button = OpenComplianceCheckReportMenuItem(eii.ExtensionObject())
        button.Invoke(eii)
    except Exception as e:
        logger.info(e)
    
    
class ComplianceCheckReportDialog(FUxCore.LayoutDialog):

    def __init__(self, businessProcess):
        self.m_sheet = None
        self.m_fuxDlg = None
        self._businessProcess = businessProcess
    
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Compliance Check Report')
        self.m_sheet = layout.GetControl('sheet').GetCustomControl()
        self.InsertContent()
    
    def InsertContent(self):
        params = self.GetComplianceCheckParameters()
        if params:
            contents = acm.FDictionary()
            contents.AtPut('service', self.CreateDefinition(params))
            self.m_sheet.SheetContents(contents)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddCustom('sheet', 'sheet.FThinSheet', 1000, 200)
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b
    
    def GetComplianceCheckParameters(self):
        step = self._businessProcess.CurrentStep()
        while step and not 'Report' in step.DiaryEntry().Parameters().Keys():
            step = step.PreviousStep()
        if step:
            return step.DiaryEntry().Parameters()
    
    @staticmethod
    def CreateDefinition(params):
        definition = acm.FDictionary()
        report = params.At('Report', None)
        if report is not None:
            storage = params.At('Storage', None)
            if storage == "ADS":
                definition.AtPut(acm.FSymbol('XmlReport'), acm.FLimitCheckReport[report])
            else:
                reportPath = os.path.join(SETTINGS.ReportDir(), report)
                if os.path.isfile(reportPath):
                    definition.AtPut(acm.FSymbol('FileName'), acm.FSymbol(reportPath))
                else:
                    logger.warn('Did not find limit report file "%s"'%reportPath)
        else:
            logger.warn('Could not retrieve report reference from business process')
        return definition
