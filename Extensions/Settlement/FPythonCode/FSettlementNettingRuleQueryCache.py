""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementNettingRuleQueryCache.py"
import acm

class SettlementNettingRuleQueryCache(object):

    def __init__(self):
        self.__nettingQueryCache = dict()
    
    def ServerUpdate(self, sender, aspect, parameter):        
        self.__nettingQueryCache.pop(sender.Name(), None)

    def GetNettingQuery(self, name):
        return self.GetNettingQueryPrivate(name)

    def GetNettingQueryPrivate(self, name):
        query = self.__nettingQueryCache.get(name)
        if not query:
            query = self.ReadQuery(name)
            if query:
                self.__nettingQueryCache[name] = query
            
        return query
            
    def ReadQuery(self, name):    
        query = None
        storedQuery = acm.FStoredASQLQuery.Select01("name = '{}' and subType = 'nettingMapping'".format(name), "Too many queries")
        
        if storedQuery:
            storedQuery.AddDependent(self)
            query = storedQuery.Query()
            
        return query

