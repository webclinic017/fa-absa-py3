""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/RiskCompliance/etc/FRiskComplianceLimitsReportPanel.py"
"""--------------------------------------------------------------------------
MODULE
    FRiskComplianceLimitsReportPanel

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Panel for showing the limit report in the risk compliance view

-----------------------------------------------------------------------------"""

import acm
import os
import FEvent
import FLimitSettings
from FSheetPanel import SheetPanel
from FSheetUtils import SheetContents
from FRiskComplianceLogging import logger

class ThinSheetContents(SheetContents):

    def SheetSetup(self):
        setup = super(ThinSheetContents, self).SheetSetup()
        setup.ServiceDefinition(acm.FRemoteSheetServiceDefinition())
        return setup


class RiskComplianceLimitsReportPanel(SheetPanel):

    CHECKING_LIMITS = "Checking Limits"

    def SettingsContents(self):
        return ThinSheetContents(self.Settings()).ForControl()

    def InitCustomControls(self, layout):
        self.Sheet().Sheet().RowHeaderCaption(self.Caption())

    @FEvent.EventCallback
    def OnBusinessProcessSelected(self, event):
        contents = acm.FDictionary()
        businessProcess = event.BusinessProcess()
        if businessProcess:
            params = self.GetLimitCheckParameters(businessProcess)
            if params:
                contents.AtPut('service', self.CreateDefinition(params))
                self.Sheet().Sheet().SheetContents(contents)
            else:
                self.Sheet().InsertObject(None)
        else:
            self.Sheet().InsertObject(None)

    def GetLimitCheckParameters(self, businessProcess):
        step = businessProcess.CurrentStep()
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
                reportPath = os.path.join(FLimitSettings.ReportDir(), report)
                if os.path.isfile(reportPath):
                    definition.AtPut(acm.FSymbol('FileName'), acm.FSymbol(reportPath))
                else:
                    logger.warn('Did not find limit report file "%s"'%reportPath)
        else:
            logger.warn('Could not retrieve report reference from business process')
        return definition

def OnDoubleClick(eii):
    try:
        sheet = eii.Parameter( "sheet" )
        limitKey = sheet.Selection().SelectedCell().RowObject().StringKey()
        limit = acm.FLimit[limitKey]
        if limit:
            acm.StartApplication("Limit", limit)
    except AttributeError:
        pass
