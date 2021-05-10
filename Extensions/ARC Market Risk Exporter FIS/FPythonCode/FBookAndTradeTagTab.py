""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FBookAndTradeTagTab.py"
"""----------------------------------------------------------------------------
MODULE
    FBookAndTradeTagTab - 

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    This is a GUI tab in the FMarketRiskExport GUI which contains settings
    for the P&L export.

----------------------------------------------------------------------------"""


import acm


import FRunScriptGUI


tab_name = "_Book and Trade Tags"
ttPositionSpec = ('Used to define the positions and specifies the book node.')

class BookAndTradeTagTab(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):
        ttBookTagsFileName = ('Name of the Book tags file.')
        ttTradeTagsFileName = ('Name of the Trade tags file.')
        variables = [
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['runBookAndTrdTagReports', 'Run reports{0}'.format(tab_name),
                    'int', [0, 1], 0, True, False,
                    'Export Book and Trade tags', self._enable, True],
                ['positionSpecForBookTags',
                    'Position specification for book node' + tab_name,
                    acm.FPositionSpecification, None, None,
                    0, 0, ttPositionSpec],
                ['BookTagsFile',
                    'Book Tags file name' + tab_name,
                    'string', None, 'Book Tags.csv',
                    0, 0, ttBookTagsFileName, None, False],
                ['TradeTagsFile',
                    'Trade Tags file name' + tab_name,
                    'string', None, 'Trade Tags.aap',
                    0, 0, ttTradeTagsFileName, None, False]
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables, __name__)

    def _enable(self, index, fieldValues):
        if fieldValues[index] == '1':
            for i in range(1, len(self)):
                self[i].enable(True)
        else:
            for i in range(1, len(self)):
                self[i].enable(False)
        return fieldValues


def getAelVariables():

    outtab = BookAndTradeTagTab()
    outtab.LoadDefaultValues(__name__)
    return outtab
