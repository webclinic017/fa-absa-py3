""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionArchiveContainers.py"
"""----------------------------------------------------------------------------
MODULE
    FCorpActionArchiveContainers - Archive container classes for corporate action
                                   related objects.

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""

import acm
import FBDPCommon

from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary

class CorpActionArchiveContainer:

    def __init__(self, action, includeDividendEstimate, beforeDate):
        self.__action = action
        self.__includeDividendEstimate = includeDividendEstimate
        self.__beforeDate = beforeDate
        self.__entities = self.__getEntities() 
        
    def __getEntities(self):
        entities = acm.FList()
        entities.Add(self.__action)
        #TODO archive the choices when there is archive_status field being added to it.
        #entities.AddAll(choices)
        choices = self.__action.CaChoices()
        for c in choices:
            entities.AddAll(c.CaPayouts())
            entities.AddAll(c.CaElections())

        if self.__includeDividendEstimate:
            divEst= acm.FDividendEstimate.Select('description={0}'.format(self.__action.Name()))
            for i in divEst:
                divStream = i.DividendStream()
                entities.Add(divStream)
                entities.Add(i)

        return entities.AsList()

    def GetEntities(self):
        return self.__entities
        
    def IsValidToArchive(self):
        if not self.__action:
            return False

        beforeDate = FBDPCommon.toDate(self.__beforeDate)
        exDate = self.__action.ExDate() 
        recordDate = self.__action.RecordDate()
        return beforeDate > exDate and beforeDate > recordDate
