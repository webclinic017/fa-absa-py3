""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationUnderlyingObject.py"
import acm

class UnderlyingObject(object):
    def IsSettlement(self):
        pass
    def IsTrade(self):
        pass
    def GetObject(self):
        pass


class UnderlyingSettlement(UnderlyingObject):
    def __init__(self, settlement):
        self.__settlement = settlement
    def IsSettlement(self):
        return True
    def IsTrade(self):
        return False
    def GetObject(self):
        return self.__settlement
    def GetTrade(self):
        return self.__settlement.Trade()


class UnderlyingTrade(UnderlyingObject):
    def __init__(self, trade):
        self.__trade = trade
    def IsSettlement(self):
        return False
    def IsTrade(self):
        return True
    def GetObject(self):
        return self.__trade
    def GetTrade(self):
        return self.__trade

def CreateUnderlyingObject(fObject):
    if fObject.IsKindOf(acm.FSettlement):
        return UnderlyingSettlement(fObject)
    if fObject.IsKindOf(acm.FTrade):
        return UnderlyingTrade(fObject)
    return None

