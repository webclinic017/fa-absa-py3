
"""-------------------------------------------------------------------------------------------------------
MODULE
    SanpshotColumnCreator - 

    (c) Copyright 2013 by Sungard FRONT ARENA. All rights reserved.

-------------------------------------------------------------------------------------------------------"""

import acm
import FLogger
from ColumnCreator import ColumnCreator


class SnapshotColumnCreator(ColumnCreator):

    LABEL = 'Snap'
    PARAMETERS = 'SnapshotColumns'
    LOGGER = FLogger.FLogger(__name__)
    NAMESPACE = 'Snapshot'
    TEMPLATE = [
        'value(%s)',
        ]

    def __init__(self, eii):
        self.shell = None
        self.activeSheet = None
        self.column = None
        self.context = None
        self.columnId = None
        self.module = None
	self.attrs = None
        ColumnCreator.__init__(self, eii)
        
    def CreateExtensionAttribute(self, extensionId, attr):
        attributeDefintion = ''.join(self.TEMPLATE) % attr
        attribute = [
            '%s:' % 'FInstrumentAndTrades',
            '%s=' % extensionId,
            '%s' % attributeDefintion
            ]
	self.attrs.append(''.join(attribute))


def Snapshot(eii):        
    creator = SnapshotColumnCreator(eii)
    if creator.IsValidColumn():
        creator.CreateColumn()

