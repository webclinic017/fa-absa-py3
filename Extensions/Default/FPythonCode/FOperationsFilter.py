""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsFilter.py"
import acm

from FOperationsUtils import GetStoredQuery
from FOperationsRuleEngine import Rule, QueryCondition, ActionFunction, ActionValue, And

#-------------------------------------------------------------------------
class FilterContainer(object):

    #-------------------------------------------------------------------------
    def __init__(self, filterQueries, defaultFilterQuery, queryClass):
        self.__rules = list()
        self.__actionValueRules = list()
        self.__filterQueries = list()

        for query in filterQueries:
            filterQuery = GetStoredQuery(query, queryClass)
            if filterQuery:
                self.__filterQueries.append(filterQuery.Query())

        if len(self.__filterQueries):
            queryConditions = []
            for fq in self.__filterQueries:
                queryConditions.append(QueryCondition(fq))
            self.__actionValueRules.append(Rule(And(queryConditions), ActionValue(True)))
            self.__rules.append(Rule(And(queryConditions), ActionFunction(FilterContainer.AddAction)))
        else:
            if None != defaultFilterQuery:
                self.__actionValueRules.append(Rule(QueryCondition(defaultFilterQuery), ActionValue(True)))
                self.__rules.append(Rule(QueryCondition(defaultFilterQuery), ActionFunction(FilterContainer.AddAction)))    

    #-------------------------------------------------------------------------
    def GetFilterRules(self):
        return self.__rules
    
    #-------------------------------------------------------------------------
    def GetActionValueFilterRules(self):
        return self.__actionValueRules

    #-------------------------------------------------------------------------
    def GetFilterQueries(self):
        return self.__filterQueries

    #-------------------------------------------------------------------------
    @staticmethod
    def AddAction(obj, objList):
        objList.append(obj)

#-------------------------------------------------------------------------
class Filter(object):

    #-------------------------------------------------------------------------
    def __init__(self, queryClass, queries, defaultQuery, validationCallable = None, selectionCallable = None, queryMandatory=True):
        self.__queryClass = queryClass
        self.__queries = self.GetQueries(queries)
        self.__defaultQuery = defaultQuery
        self.__validationCallable = validationCallable
        self.__selectionCallable = selectionCallable
        self.__queryMandatory = queryMandatory
    
    #-------------------------------------------------------------------------    
    def GetQueries(self, queryNames):
        queries = list()
        for name in queryNames:
            storedQuery = GetStoredQuery(name, self.__queryClass)
            if storedQuery:
                queries.append(storedQuery.Query())
        return queries
    
    #-------------------------------------------------------------------------    
    def IsValidObject(self, obj):
        isValid = True
        
        if self.__validationCallable:
            isValid = self.__validationCallable(obj)
        elif len(self.__queries):
            for query in self.__queries:
                if not query.IsSatisfiedBy(obj):
                    isValid = False
                    break
        elif self.__defaultQuery:
            isValid = self.__defaultQuery.IsSatisfiedBy(obj)
        elif not self.__queryMandatory:
            isValid = False
        else:
            raise Exception('ERROR: No user defined filterQueries or defaultQuery exists for processing %s, check parameter files.' % (obj.ClassName())) 
        
        return isValid

    #-------------------------------------------------------------------------
    def GetObjects(self):
        if self.__selectionCallable:
            return self.__selectionCallable()
        elif len(self.__queries):
            filterQuery = acm.CreateFASQLQuery(self.__queryClass, 'AND')
            filterQuery.AsqlNodes(self.__queries)
            return filterQuery.Select()
        elif self.__defaultQuery:
            return self.__defaultQuery.Select()
        elif not self.__queryMandatory:
            return acm.FArray()
        else:
            raise Exception('ERROR: No user defined filterQueries or defaultQuery exists, check parameter files.')

