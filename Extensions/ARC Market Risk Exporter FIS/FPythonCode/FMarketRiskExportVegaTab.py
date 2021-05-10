""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportVegaTab.py"
from collections import namedtuple

import acm
import FRunScriptGUI
from FMarketRiskExportColumnSelection import MarketRiskExportColumnSelection

tab_name = "_Vega"

AELVariable = namedtuple('AELVariable', ['variable', 'display', 'type',
    'values', 'default', 'required', 'multiple', 'description',
    'callback', 'enabled'])


class MarketRiskExportVegaTab(MarketRiskExportColumnSelection):

    ttColumnNames = ('The names of the columns from which values are obtained')
    ttVegaFile = ('Output file name for vega.')

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
                AELVariable('runVegaReports', 'Run reports{0}'.format(
                    tab_name), 'int', [0, 1], 0,
                    True, False, 'Run vega report',
                    self._enable, True),
                AELVariable("vega_file",
                        'Vega output file{0}'.format(
                            tab_name),
                        'string', None, 'Vega',
                        False, False,
                        MarketRiskExportVegaTab.ttVegaFile,
                        None, False),
                ]

        MarketRiskExportColumnSelection.__init__(self, variables,
                                    __name__, tab_name,
                                    'Portfolio Vega')


def getAelVariables():
    outtab = MarketRiskExportVegaTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
