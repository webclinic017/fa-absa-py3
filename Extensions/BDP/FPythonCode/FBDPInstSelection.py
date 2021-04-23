""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FBDPInstSelection.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE

    FBDPInstSelection.py - Instrument selection used in FBDPInstSelectionDialog

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import acm
import ael
import FBDPCommon
import string
import importlib

SEPARATOR = ' | '

class FBDPInstSelection():

    def __init__(self, name, queryFunc):
        self._name = name
        self._queryFunc = queryFunc

    def Name(self):
        return self._name

    def Run(self):
        """
        The main functionality body.
        """
        queryResult = self._queryFunc()
        insNameList = [row[0] for row in queryResult[0]]
        return insNameList

def GetUnTradedInstruments():
    query = 'select instrument.insid FROM instrument \
WHERE NOT EXISTS(SELECT 1 FROM trade where trade.insaddr=instrument.insaddr)'
    return ael.dbsql(query)

def GetExpiredUnTradedInstruments():
    query = 'select instrument.insid FROM instrument \
WHERE NOT EXISTS(SELECT 1 FROM trade where trade.insaddr=instrument.insaddr)\
 and exp_day < GETDATE()'
    return ael.dbsql(query)

def GetArchivedInstruments():
    query = 'select instrument.insid FROM instrument \
WHERE archive_status = 1'
    return ael.dbsql(query)

def GetInstWithArchivedPosition():
    query = "select distinct text1 from trade where type = 16 "
    insList = FBDPCommon.get_result_in_list(ael.dbsql(query))
    if insList:
        query = ('SELECT insid FROM instrument WHERE insid in '
                    '{0}'.format(insList))
        query = string.replace(query, "[", "(")
        query = string.replace(query, "]", ")")
        return ael.dbsql(query)
    else:
        return [[]]

def GetInstSelections():
    instSelectionList = []
    untradeInst = FBDPInstSelection(
        'Untraded Instruments', GetUnTradedInstruments
    )
    instSelectionList.append(untradeInst)

    untradeExpiredInst = FBDPInstSelection(
        'Untraded Expired Instruments', GetExpiredUnTradedInstruments
    )
    instSelectionList.append(untradeExpiredInst)

    archivedInst = FBDPInstSelection(
        'Archived Instruments', GetArchivedInstruments
    )
    instSelectionList.append(archivedInst)

    archivedPositionInst = FBDPInstSelection(
        'Instruments With Archived Positions', GetInstWithArchivedPosition
    )
    instSelectionList.append(archivedPositionInst)

    try:
        import FBDPHook
        importlib.reload(FBDPHook)
    except ImportError:
        return instSelectionList

    try:
        userInstSelection = FBDPHook.get_instrument_selection()
        for s in userInstSelection:
            instSel = FBDPInstSelection(s, userInstSelection[s])
            instSelectionList.append(instSel)
    except AttributeError:
        pass

    return instSelectionList
