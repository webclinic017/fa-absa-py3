""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/BDExport/./etc/FSingleExportIdentifier.py"
""" Compiled: 2017-08-02 17:42:32 """

#__src_file__ = "extensions/export/./etc/FSingleExportIdentifier.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSingleExportIdentifier

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    See ExportBaseReadMe.py for more information about this module

-------------------------------------------------------------------------------------------------------"""
import acm


class FSingleExportIdentifier():
    """
    Class that represents the key identifier for a report. Different keys will
    represent different files/reports. Basically it consists of the answer to
    'what is this'? and 'to whom is this sent'? 

    """
    def __init__(self, exportProcess, partyId, sheetTemplateId):
        assert(exportProcess), "AFSingleExportIdentifier must contain an export process"
        assert(partyId), "A FSingleExportIdentifier must contain a partyId"
        assert(sheetTemplateId), "A FSingleExportIdentifier must contain a sheetTemplateId"
        self._exportProcess = exportProcess
        self._partyId = partyId
        self._sheetTemplateId = sheetTemplateId

    def ExportProcess(self):
        return self._exportProcess

    def Integration(self):
        return self._exportProcess.Integration()

    def PartyId(self):
        return self._partyId

    def SheetTemplateId(self):
        return self._sheetTemplateId

    def Party(self):
        return acm.FParty[self.PartyId()]

    def SheetTemplate(self):
        return acm.FTradingSheetTemplate[self.SheetTemplateId()]

    def KeyValue(self):
        return self.PartyId() + "-" + self.SheetTemplateId()
