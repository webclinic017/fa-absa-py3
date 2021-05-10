""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExport.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FMarketRiskExport - Run Script GUI

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
import FRunScriptGUI

import FMarketRiskAddContentTab
import FMarketRiskExportMVTab
import FMarketRiskExportThetaTab
import FMarketRiskExportVaRTab
import FMarketRiskExportStressTab
import FMarketRiskExportPnLTab
import FMarketRiskExportLogSettingsTab
import FMarketRiskExportOutputSettingsTab
import FMarketRiskExportStressGridTab
import FMarketRiskExportInterestRatesTab
import FMarketRiskExportVegaTab
import FMarketRiskExportCreditTab
import FMarketRiskExportCustomTab
import FMarketRiskExportRiskFactorTab
import FMarketRiskExporters

from FMarketRiskExporters import FMarketRiskPnLExporter
from FMarketRiskExporters import FMarketRiskMVExporter
from FMarketRiskExporters import FMarketRiskThetaExporter
from FMarketRiskExporters import FMarketRiskVaRExporter
from FMarketRiskExporters import StressGridExporter
from FMarketRiskExporters import FMarketRiskStressExporter
from FMarketRiskExporters import IRDeltaExporter
from FMarketRiskExporters import VegaExporter
from FMarketRiskExporters import CreditDeltaExporter
from FMarketRiskExporters import IRBucketDeltaExporter
from FMarketRiskExporters import IRTwistDeltaExporter
from FMarketRiskExporters import CustomExporter
from FMarketRiskExporters import RiskFactorExporter

class MarketRiskExport(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):
        FRunScriptGUI.AelVariablesHandler.__init__(self, [])
        #add other tabs
        self.extend(FMarketRiskAddContentTab.getAelVariables())
        self.extend(FMarketRiskExportMVTab.getAelVariables())
        self.extend(FMarketRiskExportPnLTab.getAelVariables())
        self.extend(FMarketRiskExportInterestRatesTab.getAelVariables())
        self.extend(FMarketRiskExportThetaTab.getAelVariables())
        self.extend(FMarketRiskExportVegaTab.getAelVariables())
        self.extend(FMarketRiskExportCreditTab.getAelVariables())
        self.extend(FMarketRiskExportVaRTab.getAelVariables())
        self.extend(FMarketRiskExportStressTab.getAelVariables())
        self.extend(FMarketRiskExportStressGridTab.getAelVariables())
        self.extend(FMarketRiskExportCustomTab.getAelVariables())
        self.extend(FMarketRiskExportRiskFactorTab.getAelVariables())
        self.extend(FMarketRiskExportOutputSettingsTab.getAelVariables())
        self.extend(FMarketRiskExportLogSettingsTab.getAelVariables())

ael_gui_parameters = {"windowCaption":__name__}
ael_variables = MarketRiskExport()
ael_variables.LoadDefaultValues(__name__)


def ael_main(ael_params):
    # Initialize the logger, should go _first_ of all initalizations
    world = FMarketRiskExportLogSettingsTab.logger_setup(ael_params)

    world.logStart(None)
    world.logInfo("Exporting Market Risk Values")

    ael_params['ExportFormats'] = 'Adaptiv Memory Cube'
    # Create exporters
    exports = (('runVaRReports', FMarketRiskVaRExporter(ael_params, world)),
                ('runVegaReports', VegaExporter(ael_params, world)),
                ('runCreditReport', CreditDeltaExporter(ael_params, world)),
                ('runStressReports', FMarketRiskStressExporter(
                    ael_params, world)),
                ('runStressGridReports', StressGridExporter(ael_params, world)),
                ('runIRReports', IRDeltaExporter(ael_params, world)),
                ('runIRReports', IRBucketDeltaExporter(ael_params, world)),
                ('runIRReports', IRTwistDeltaExporter(ael_params, world)),
                ('runCustomReports', CustomExporter(ael_params, world)),
                ('runRiskFactorReports', RiskFactorExporter(ael_params, world)),)

    if FMarketRiskExporters.do_run_bulk_exports(ael_params, world):
        FMarketRiskExporters.run_createBulkExporters(ael_params, world)

    # Export data
    for flag, exporter in exports:
        if ael_params.get(flag, False):
            if exporter.validateParameters():
                exporter.export()
                world.logInfo("{0}: Done.".format(exporter.__class__.__name__))
            else:
                world.logInfo("Invalid Parameters: Skipping '%s'" % exporter.__class__.__name__)
        else:
            world.logInfo("Skipping '{0}'".format(exporter.__class__.__name__))

    world.summarySummarise()
    world.logFinish(None)
    del world
