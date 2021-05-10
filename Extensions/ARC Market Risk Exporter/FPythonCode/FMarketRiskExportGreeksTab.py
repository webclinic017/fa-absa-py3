""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportGreeksTab.py"
from collections import namedtuple

import acm
import FRunScriptGUI
from FMarketRiskExportColumnSelection import MarketRiskExportColumnSelection

tab_name = "_Greeks"

AELVariable = namedtuple('AELVariable', ['variable', 'display', 'type',
    'values', 'default', 'required', 'multiple', 'description',
    'callback', 'enabled'])


class FMarketRiskExportGreeksTab(MarketRiskExportColumnSelection):

    ttColumnNames = ('The names of the columns from which values are obtained')
    ttGreeksFile = ('Output file name for greeks calculation.')
    ttMeasures =("The measures of the calculation.")
    
    def _enable(self, index, fieldValues):
        if fieldValues[index] == '1':
            for i in range(1, len(self)):
                self[i].enable(True)
        else:
            for i in range(1, len(self)):
                self[i].enable(False)
        return fieldValues

    def __init__(self):
        variables = [
                AELVariable('runGreekReports', 'Run reports{0}'.format(
                    tab_name), 'int', [0, 1], 0,
                    True, False, 'Run greeks report',
                    self._enable, True),
                AELVariable("greeks_file",
                        'Output file{0}'.format(
                            tab_name),
                        'string', None, 'Greeks',
                        0, False,
                        FMarketRiskExportGreeksTab.ttGreeksFile,
                        None, False),
                 AELVariable("measures_Greeks",
                        'Measures{0}'.format(
                            tab_name),
                        'string', ['Risk Delta', 'Risk Gamma', 'Risk Theta', 'Risk Vega'], 'Delta',
                        0, True,
                        FMarketRiskExportGreeksTab.ttMeasures,
                        None, False),
                ]

        MarketRiskExportColumnSelection.__init__(self, variables,
                                    __name__, tab_name,
                                    'Portfolio Delta')


def getAelVariables():
    outtab = FMarketRiskExportGreeksTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
