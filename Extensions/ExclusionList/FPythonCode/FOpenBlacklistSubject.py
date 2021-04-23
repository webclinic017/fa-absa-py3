""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/ExclusionList/etc/FOpenBlacklistSubject.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FOpenBlacklistSubject

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import FUxCore

class OpenBlacklistSubjectMenuItem(FUxCore.MenuItem):

    BLACKLIST_APPL_MAP = {'ExclusionListInstrumentQuery': None,\
                            'PageGroupBlacklist': 'Page Definition',\
                            'PartyGroupBlacklist': 'Party Groups',\
                            'InstrumentIdentifierExclusionList': 'Extension Editor',\
                            'IssuerIdentifierExclusionList': 'Extension Editor'}
    
    def __init__(self, frame):
        self.Frame = frame

    def Application(self):
        return self.Frame.CustomLayoutApplication()

    def LimitTarget(self):
        return self.Application().LimitTarget()

    def ColumnParameters(self):
        config = self.LimitTarget().CalculationSpecification().Configuration()
        if config and config.ParamDict().At('columnParameters'):
            return config.ParamDict().At('columnParameters')
        
    def ApplicationName(self):
        return self.BLACKLIST_APPL_MAP.get(self.BlacklistParameter())
        
    def BlacklistParameter(self):
        try:
            for parameter in self.ColumnParameters().Keys():
                if str(parameter) in list(self.BLACKLIST_APPL_MAP.keys()):
                    return str(parameter)
        except AttributeError:
            return None
            
    def Blacklist(self):
        parameter = self.BlacklistParameter()
        if parameter:
            return self.ColumnParameters().At(parameter)
    
    def Applicable(self):
        try:
            return self.Application().__class__.__name__ == "LimitApplication"
        except AttributeError:
            return False
        
    def Enabled(self):
        return bool(self.Blacklist())
        
    def Invoke(self, eii):
        acm.StartApplication(self.ApplicationName(), self.Blacklist())

def CreateMenuItem(frame):
    return OpenBlacklistSubjectMenuItem(frame)
