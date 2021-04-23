""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FArtiQMarketRiskExport.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FArtiQMarketRiskExport - Run Script GUI

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import FRunScriptGUI
import datetime
import time

import FArtiQMarketRiskAddContentTab
import FArtiQMarketRiskExportVaRTab
import FArtiQMarketRiskExportStressTab
import FMarketRiskExportPnLTab
import FMarketRiskExportLogSettingsTab
import FArtiQMarketRiskExportOutputSettingsTab
import FMarketRiskExportStressGridTab
import FMarketRiskExportCreditTab
import FMarketRiskExportCustomTab
import FMarketRiskExportRiskFactorTab
import FMarketRiskExporters
import FMarketRiskExportBucketShiftSensitivityTab
import FMarketRiskExportParallelShiftSensitivityTab
import FMarketRiskExportTwistSensitivityTab
import FMarketRiskExportGreeksTab
import FMarketRiskExportPLExplainTab
import FMarketRiskMarketDataTab
import FBookAndTradeTagTab

from FMarketRiskExporters import FMarketRiskPnLExporter
from FMarketRiskExporters import FMarketRiskMVExporter
from FMarketRiskExporters import FMarketRiskThetaExporter
from FMarketRiskExporters import FMarketRiskVaRExporter
from FMarketRiskExporters import StressGridExporter
from FMarketRiskExporters import FMarketRiskStressExporter
from FMarketRiskExporters import VegaExporter
from FMarketRiskExporters import CreditDeltaExporter
from FMarketRiskExporters import IRBucketShiftExporter
from FMarketRiskExporters import IRTwistShiftExporter
from FMarketRiskExporters import IRParallelShiftDeltaExporter
from FMarketRiskExporters import CustomExporter
from FMarketRiskExporters import RiskFactorExporter
from FMarketRiskExporters import GreeksExporter
from FMarketRiskExporters import PLExplainExporter
from FMarketRiskExporters import MarketDataExporter
from FMarketRiskExporters import BookTradeTagsExporter

class FArtiQMarketRiskExport(FRunScriptGUI.AelVariablesHandler):
    def __init__(self):
        FRunScriptGUI.AelVariablesHandler.__init__(self, [])
        #add other tabs
        self.extend(FArtiQMarketRiskAddContentTab.getAelVariables())
        self.extend(FBookAndTradeTagTab.getAelVariables())
        self.extend(FMarketRiskExportPnLTab.getAelVariables())
        self.extend(FMarketRiskExportParallelShiftSensitivityTab.getAelVariables())
        self.extend(FMarketRiskExportBucketShiftSensitivityTab.getAelVariables())
        self.extend(FMarketRiskExportTwistSensitivityTab.getAelVariables())
        self.extend(FMarketRiskExportGreeksTab.getAelVariables())
        self.extend(FMarketRiskExportPLExplainTab.getAelVariables())
        self.extend(FMarketRiskMarketDataTab.getAelVariables())
        self.extend(FMarketRiskExportCreditTab.getAelVariables())
        self.extend(FArtiQMarketRiskExportVaRTab.getAelVariables())
        self.extend(FArtiQMarketRiskExportStressTab.getAelVariables())
        self.extend(FMarketRiskExportStressGridTab.getAelVariables())
        self.extend(FMarketRiskExportCustomTab.getAelVariables())
        self.extend(FMarketRiskExportRiskFactorTab.getAelVariables())
        self.extend(FArtiQMarketRiskExportOutputSettingsTab.getAelVariables())
        self.extend(FMarketRiskExportLogSettingsTab.getAelVariables())

ael_gui_parameters = {"windowCaption":__name__}
ael_variables = FArtiQMarketRiskExport()
ael_variables.LoadDefaultValues(__name__)


def ael_main(ael_params):
    # Initialize the logger, should go _first_ of all initalizations
    world = FMarketRiskExportLogSettingsTab.logger_setup(ael_params)

    world.logStart(None)
    world.logInfo("Exporting Market Risk Values to ArtiQ")
    
    ael_params['ExportFormats'] = 'Adaptiv ArtiQ Cube' 
    
    # Create exporters
    exports = (('runVaRReports', FMarketRiskVaRExporter(ael_params, world)),
                ('runVegaReports', VegaExporter(ael_params, world)),
                ('runCreditReport', CreditDeltaExporter(ael_params, world)),
                ('runStressReports', FMarketRiskStressExporter(ael_params, world)),
                ('runGreekReports', GreeksExporter(ael_params, world)),
                ('runPLExplainReport', PLExplainExporter(ael_params, world)),
                ('runMarketDataReport', MarketDataExporter(ael_params, world)),
                ('runStressGridReports', StressGridExporter(ael_params, world)),
                ('runParallelShiftReports', IRParallelShiftDeltaExporter(ael_params, world)),
                ('runBucketShiftReports', IRBucketShiftExporter(ael_params, world)),
                ('runTwistReports', IRTwistShiftExporter(ael_params, world)),
                ('runCustomReports', CustomExporter(ael_params, world)),
                ('runRiskFactorReports', RiskFactorExporter(ael_params, world)),
                ('runBookAndTrdTagReports', BookTradeTagsExporter(ael_params, world)),)

    if FMarketRiskExporters.do_run_bulk_exports(ael_params, world):
        FMarketRiskExporters.run_createBulkExporters(ael_params, world)

    # Export data
    for flag, exporter in exports:
        if ael_params.get(flag, False):
            if exporter.validateParameters():
                exporter.export()
                world.logInfo("{0}: Done.".format(exporter.__class__.__name__))
            else:
                world.logError("Invalid Parameters: Skipping '%s', No export file generated." % exporter.__class__.__name__)
        else:
            world.logInfo("Skipping '{0}'".format(exporter.__class__.__name__))

    world.summarySummarise()
    world.logFinish(None)
    del world
    print(('Total Clock-Time: ' + str(datetime.timedelta(seconds=time.clock()))))
