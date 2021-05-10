""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskMarketDataTab.py"
from collections import namedtuple

import acm
import FRunScriptGUI
import FBDPGui

tab_name = '_Market Data'

AELVariable = namedtuple('AELVariable', ['variable', 'display', 'type',
    'values', 'default', 'required', 'multiple', 'description',
    'callback', 'enabled'])

qSelectIns = FBDPGui.insertInstruments(
    instype=('Stock', 'Commodity', 'Curr'))

def getTimeBuckets():
    return sorted([s.Name() for s in acm.FStoredTimeBuckets.Select("")])
    
class FMarketRiskMarketDataTab(FRunScriptGUI.AelVariablesHandler):

    def _enable(self, index, fieldValues):
        if fieldValues[index] == '1':
            for i in range(1, len(self)):
                self[i].enable(True)
            if self.ExportBenchmarkPrice.isEnabled():
                self.timebucket_name_MarketData.enable(0, \
                    "Only available for exporting the yield curve points")
        else:
            for i in range(1, len(self)):
                self[i].enable(False)
            
        return fieldValues

    def _exportBenchmarkPriceCB(self, index, fieldValues):
        enable = 0 if fieldValues[index] == '1' else 1
        #self.[len(self)-1].enable(enable, \
        #    "Only available for exporting the yield curve points")
        self.timebucket_name_MarketData.enable(enable, \
            "Only available for exporting the yield curve points")
        
        return fieldValues

    def __init__(self):
        ttFileName = ('Output file name')
        ttYieldCurves = ('Names of yield curves to be exported for its market data.')
        ttVolatility = ('Name of the volatility to be exported for its market data.')
        ttInstrument = ('Name of the selected intruments for the market price')
        ttExportBenchmarkPrice = ("Export benchmark instrument MtM price for the selected Benchmark curve")
        ttTimeBuckets = ('Define the time bucket grid based upon which the interest rate yield curve will be exported from.')
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['runMarketDataReport',
                    'Run reports{0}'.format(tab_name), 'int', [0, 1], 0, True,
                    False, 'PL Explain Report', self._enable, True],
                ['rateFileOutputName',
                    'Rate File Name{0}'.format(tab_name), 'string', None, 'Rate', 0,
                    False, 'Default rate file name', None, True],
                ["Instruments_MarketData",
                        "Instruments" + tab_name,
                        'FInstrument', 
                        None,
                        qSelectIns, False, True,
                        ttInstrument,
                        None, False],
                ["volatility_MarketData",
                        "Volatility Structure" + tab_name,
                        "FVolatilityStructure", [], 
                        None, False, True,
                        ttVolatility,
                        None, False],
                ["yieldCurve_MarketData",
                        "Yield Curves" + tab_name,
                        'FYieldCurve',
                        [],
                        None,
                        False, True,
                        ttYieldCurves,
                        None, False],
                ['ExportBenchmarkPrice',
                        'Export based upon Benchmark Instrument Price' + tab_name,
                        'int', [1, 0], 1,
                        1, 0, ttExportBenchmarkPrice, self._exportBenchmarkPriceCB],
                ["timebucket_name_MarketData",
                        "Time buckets for the tenor of the exported yield curves" + tab_name,
                        "string", getTimeBuckets(),
                        '', False, False,
                        ttTimeBuckets,
                        None, False],
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)

def getAelVariables():
    outtab = FMarketRiskMarketDataTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
